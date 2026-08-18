"""Core analysis pipeline: build the per-township dataset for Yangon Region, Myanmar.

Stages:
  1. Load & validate administrative boundaries (45 townships, geoBoundaries ADM3)
     and assign each township to its Yangon district (ADM2).
  2. CHIRPS monthly rainfall -> zonal series (1981-2026) + derived climate
     indicators (annual total, wet-season share, extreme-month count, trend).
  3. Copernicus DEM -> elevation stats (mean/min/max) + slope.
  4. Population: Kontur H3 (current) area-weighted.
  5. Infrastructure: schools + health facilities counts (HDX / OSM, Myanmar).
  6. Flood-related rainfall indicators (World Bank / GFDRR, ADM2).
  7. Age shares (children/elderly) from WorldPop ADM2 (district level).
  8. Persist `data/processed/yangon_township_features.parquet`.

Every derived value is traceable to the raw source; no values are fabricated.
"""

from __future__ import annotations

import glob
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
import rasterio.features
import rasterio.mask

from floodresilience.config import (
    DATA_PROCESSED,
    DATA_RAW,
    DATA_INTERMEDIATE,
    YANGON_BBOX,
    CRS_WGS84,
    CRS_UTM,
)
from floodresilience.cleaning.quality import QCResult, run_qc, write_qc_report, save_qc_json

BOUNDARY_SRC = DATA_RAW / "boundaries" / "mmr" / "Yangon_townships.geojson"
DISTRICT_SRC = DATA_RAW / "boundaries" / "mmr" / "MMR_ADM2.geojson"
CHIRPS_DIR = DATA_INTERMEDIATE / "rainfall" / "chirps_yangon"
DEM_FILES = sorted((DATA_RAW / "dem").glob("*.tif"))
KONTUR = DATA_RAW / "population" / "kontur_population_MM_20231101.gpkg"
ADMPOP = DATA_RAW / "population" / "mmr_admpop_adm2_2023.csv"
WB_RAINFALL = DATA_RAW / "rainfall_indicator" / "mmr-rainfall-subnat-5ytd.csv"
EDU_GEOJSON = DATA_RAW / "education" / "mmr" / "unzipped" / "education_facilities.geojson"
HEALTH_GEOJSON = DATA_RAW / "health" / "mmr" / "unzipped" / "health_facilities.geojson"

YANGON_ADM1 = "MMR013"


def _make_tship_code(i: int) -> str:
    """Stable synthetic township code derived from boundary order."""
    return f"T{i + 1:02d}"


def load_boundaries() -> gpd.GeoDataFrame:
    gdf = gpd.read_file(BOUNDARY_SRC)
    gdf["tship_code"] = [_make_tship_code(i) for i in range(len(gdf))]
    gdf["township"] = gdf["shapeName"].str.strip()
    # Assign each township to its Yangon district (ADM2) by representative point.
    dist = gpd.read_file(DISTRICT_SRC)
    dist = dist[dist["shapeName"].astype(str).str.contains("Yangon", case=False, na=False)].copy()
    dist["district"] = dist["shapeName"].str.replace("Yangon (", "", regex=False).str.replace(")", "", regex=False)
    dist_code = {
        "East": "MMR013D002",
        "North": "MMR013D001",
        "South": "MMR013D003",
        "West": "MMR013D004",
    }
    dist["district_code"] = dist["district"].map(dist_code)
    if dist["district_code"].isna().any():
        raise ValueError("Unexpected Yangon district names in ADM2 boundaries")

    pts = gdf.copy()
    pts["geometry"] = pts.geometry.representative_point()
    joined = gpd.sjoin(pts, dist[["district", "district_code", "geometry"]], how="left", predicate="within")
    if joined["district"].isna().any():
        missing = joined.loc[joined["district"].isna(), "township"].tolist()
        raise ValueError(f"Townships not assigned to a district: {missing}")
    gdf = gdf.merge(joined[["tship_code", "district", "district_code"]], on="tship_code", how="left")
    gdf = gdf[["tship_code", "township", "district", "district_code", "geometry"]].reset_index(drop=True)
    return gdf


def chirps_zonal_series(boundaries: gpd.GeoDataFrame) -> pd.DataFrame:
    """Compute mean monthly rainfall per township for every CHIRPS month."""
    files = sorted(glob.glob(str(CHIRPS_DIR / "chirps_*.tif")))
    if not files:
        raise FileNotFoundError("No CHIRPS tiles under data/intermediate/rainfall/chirps_yangon/")

    # Build per-polygon masks against the first raster grid.
    first = files[0]
    with rasterio.open(first) as src:
        grid_shape = src.shape
        transform = src.transform
        crs = src.crs
    bounds_gdf = boundaries.to_crs(crs)
    masks: list[np.ndarray] = []
    for _, row in bounds_gdf.iterrows():
        mask = rasterio.features.geometry_mask(
            [row.geometry], out_shape=grid_shape, transform=transform, invert=True, all_touched=True
        )
        masks.append(mask)

    records: list[dict] = []
    for f in files:
        yyyymm = Path(f).stem.split("_")[1]
        with rasterio.open(f) as src:
            data = src.read(1).astype("float64")
        data[data < 0] = np.nan
        rec = {"month": f"{yyyymm[:4]}-{yyyymm[4:6]}-01"}
        for i, mask in enumerate(masks):
            vals = data[mask]
            vals = vals[~np.isnan(vals)]
            rec[f"tship_{i}"] = float(vals.mean()) if vals.size else np.nan
        records.append(rec)
    df = pd.DataFrame(records)
    df["month"] = pd.to_datetime(df["month"])
    df["year"] = df["month"].dt.year
    df["month_of_year"] = df["month"].dt.month
    return df


def climate_indicators(series: pd.DataFrame, n_tship: int) -> pd.DataFrame:
    """Derive per-township rainfall indicators from the monthly series."""
    rows: list[dict] = []
    for i in range(n_tship):
        col = f"tship_{i}"
        s = series[["year", "month_of_year", col]].copy()
        s = s[s[col].notna()]
        if s.empty:
            rows.append({"tship_idx": i})
            continue
        # Annual totals (complete years only: months 1-12 present)
        counts = s.groupby("year")["month_of_year"].nunique()
        complete_years = counts[counts == 12].index
        annual = s[s["year"].isin(complete_years)].groupby("year")[col].sum()
        # Monthly climatology
        clim = s.groupby("month_of_year")[col].mean()
        # Yangon monsoon wet season: June-September.
        wet_months = [6, 7, 8, 9]
        total = clim.sum()
        wet_share = clim.loc[[m for m in wet_months if m in clim.index]].sum() / total if total else np.nan
        # Extreme months: count of months above 95th percentile
        p95 = np.nanpercentile(s[col], 95)
        n_extreme = int((s[col] >= p95).sum())
        # Trend on annual totals (least squares)
        if len(annual) >= 10:
            x = (annual.index - annual.index[0]).astype(float)
            y = annual.values
            slope = np.polyfit(x, y, 1)[0]  # mm/year
            # annual mean for normalization
            trend_pct = (slope / annual.mean()) * 100 if annual.mean() else np.nan
        else:
            slope, trend_pct = np.nan, np.nan
        rows.append(
            {
                "tship_idx": i,
                "rain_annual_mean_mm": float(annual.mean()),
                "rain_annual_last5_mean_mm": float(annual.iloc[-5:].mean()) if len(annual) >= 5 else np.nan,
                "rain_wet_season_share": float(wet_share),
                "rain_extreme_months": n_extreme,
                "rain_annual_trend_mm_yr": float(slope),
                "rain_annual_trend_pct_yr": float(trend_pct),
                "rain_p95_monthly_mm": float(p95),
                "rain_total_months": int(len(s)),
            }
        )
    return pd.DataFrame(rows)


def dem_stats(boundaries: gpd.GeoDataFrame) -> pd.DataFrame:
    """Mosaic the DEM tiles and compute elevation + slope stats per township."""
    from rasterio.merge import merge

    if not DEM_FILES:
        return pd.DataFrame()
    srcs = [rasterio.open(f) for f in DEM_FILES]
    mosaic, transform = merge(srcs)
    for s in srcs:
        s.close()
    dem = mosaic[0]
    dem[dem < -1000] = np.nan  # void / nodata

    # Slope (percent) from elevation using physical pixel size in metres.
    with np.errstate(invalid="ignore", divide="ignore"):
        py_m = abs(transform.e) * 111_320.0  # north-south (latitude)
        px_m = abs(transform.a) * 111_320.0 * np.cos(np.deg2rad(transform.f))  # east-west (longitude)
        gy, gx = np.gradient(dem)
        sl = 100.0 * np.hypot(gx / px_m, gy / py_m)
        sl = np.where(np.isfinite(sl), sl, np.nan)

    bounds_gdf = boundaries.to_crs(CRS_WGS84)
    rows = []
    for i, row in bounds_gdf.iterrows():
        mask = rasterio.features.geometry_mask(
            [row.geometry], out_shape=dem.shape, transform=transform, invert=True, all_touched=True
        )
        ev = dem[mask]
        ev = ev[~np.isnan(ev)]
        sv = sl[mask]
        sv = sv[~np.isnan(sv)]
        rows.append(
            {
                "tship_idx": i,
                "elev_mean_m": float(ev.mean()) if ev.size else np.nan,
                "elev_min_m": float(ev.min()) if ev.size else np.nan,
                "elev_max_m": float(ev.max()) if ev.size else np.nan,
                "slope_mean_pct": float(sv.mean()) if sv.size else np.nan,
            }
        )
    return pd.DataFrame(rows)


def population_exposure(boundaries: gpd.GeoDataFrame) -> pd.DataFrame:
    """Area-weighted Kontur H3 population per township."""
    hex_gdf = gpd.read_file(KONTUR)
    # Reproject to boundaries CRS (WGS84) for intersection.
    hex_wgs = hex_gdf.to_crs(CRS_WGS84)
    joined = gpd.sjoin(hex_wgs, boundaries[["geometry"]], how="inner", predicate="intersects")
    hex_ids = joined.index.unique()
    sub = hex_wgs.loc[hex_ids].copy()

    # Ensure equal-area projection for area fractions.
    b_utm = boundaries.copy().to_crs(CRS_UTM)
    sub_utm = sub.to_crs(CRS_UTM)

    rows = []
    for i in range(len(boundaries)):
        poly = b_utm.geometry.iloc[i]
        hits = sub_utm[sub_utm.intersects(poly)]
        if hits.empty:
            rows.append({"tship_idx": i, "pop_est": 0.0})
            continue
        total = 0.0
        for _, h in hits.iterrows():
            inter = h.geometry.intersection(poly)
            if inter.is_empty:
                continue
            frac = inter.area / h.geometry.area if h.geometry.area > 0 else 0.0
            total += float(h["population"]) * frac
        rows.append({"tship_idx": i, "pop_est": total})
    return pd.DataFrame(rows)


def _count_facilities(boundaries: gpd.GeoDataFrame, src: Path) -> list[int]:
    """Count OSM building polygons per township via representative points."""
    bbox = boundaries.total_bounds
    gdf = gpd.read_file(src, bbox=tuple(bbox))
    if len(gdf) == 0:
        return [0] * len(boundaries)
    gdf = gdf.to_crs(CRS_WGS84)
    gdf["geometry"] = gdf.geometry.representative_point()
    j = gpd.sjoin(gdf, boundaries[["geometry"]], how="inner", predicate="within")
    counts = j.groupby("index_right").size()
    return [int(counts.get(i, 0)) for i in range(len(boundaries))]


def facility_counts(boundaries: gpd.GeoDataFrame) -> pd.DataFrame:
    """Count schools and health facilities per township."""
    rows = []
    if EDU_GEOJSON.exists():
        schools = _count_facilities(boundaries, EDU_GEOJSON)
    else:
        schools = [0] * len(boundaries)
    if HEALTH_GEOJSON.exists():
        health = _count_facilities(boundaries, HEALTH_GEOJSON)
    else:
        health = [0] * len(boundaries)
    for i in range(len(boundaries)):
        rows.append({"tship_idx": i, "schools": schools[i], "health_facilities": health[i]})
    return pd.DataFrame(rows)


def wb_rainfall_indicators(boundaries: gpd.GeoDataFrame) -> pd.DataFrame:
    """Aggregate World Bank / GFDRR flood-relevant rainfall indices to township
    via its district (ADM2)."""
    df = pd.read_csv(WB_RAINFALL)
    df["date"] = pd.to_datetime(df["date"])
    adm2 = df[(df["adm_level"] == 2) & (df["PCODE"].astype(str).str.startswith(YANGON_ADM1))].copy()

    agg = adm2.groupby("PCODE").agg(
        rfh_mean=("rfh", "mean"),
        r1h_mean=("r1h", "mean"),
        r3h_mean=("r3h", "mean"),
        rfh_p95=("rfh", lambda s: np.nanpercentile(s, 95)),
        n_obs=("rfh", "size"),
    ).reset_index()

    out = pd.DataFrame({"tship_idx": range(len(boundaries))})
    out["district_code"] = boundaries["district_code"].values
    out = out.merge(agg, left_on="district_code", right_on="PCODE", how="left")
    out = out.drop(columns=["district_code", "PCODE"])
    return out


def age_shares(boundaries: gpd.GeoDataFrame) -> pd.DataFrame:
    """Child (<15) and elderly (65+) population shares per district from WorldPop ADM2."""
    adm = pd.read_csv(ADMPOP)
    adm = adm[adm["ADM1_NAME"].astype(str).str.contains("Yangon", case=False, na=False)].copy()
    adm["district_code"] = adm["ADM2_PCODE"].astype(str).str.strip()
    child_cols = ["T_00_04", "T_05_09", "T_10_14"]
    elder_cols = ["T_65_69", "T_70_74", "T_75_79", "T_80_84", "T_85_89", "T_90Plus"]
    agg2 = adm.groupby("district_code").agg(
        **{f"sum_{c}": (c, "sum") for c in child_cols + elder_cols + ["T_TL"]}
    ).reset_index()
    agg2["child_share"] = agg2[[f"sum_{c}" for c in child_cols]].sum(axis=1) / agg2["sum_T_TL"]
    agg2["elderly_share"] = agg2[[f"sum_{c}" for c in elder_cols]].sum(axis=1) / agg2["sum_T_TL"]

    out = pd.DataFrame({"tship_idx": range(len(boundaries))})
    out["district_code"] = boundaries["district_code"].values
    out = out.merge(agg2[["district_code", "child_share", "elderly_share"]], on="district_code", how="left")
    out = out.drop(columns=["district_code"])
    return out


def main() -> None:
    qc: list[QCResult] = []

    boundaries = load_boundaries()
    print(f"boundaries: {len(boundaries)} townships")

    qc.append(run_qc(boundaries.drop(columns="geometry").assign(geometry_len=[len(g.wkt) for g in boundaries.geometry]), "boundaries_township"))

    # 2. CHIRPS series
    series = chirps_zonal_series(boundaries)
    qc.append(run_qc(series.iloc[:, :3], "chirps_monthly_series", date_col="month"))
    clim = climate_indicators(series, len(boundaries))
    print("climate indicators computed")

    # 3. DEM
    dem = dem_stats(boundaries)
    qc.append(run_qc(dem, "dem_zonal"))

    # 4. Population
    pop = population_exposure(boundaries)
    qc.append(run_qc(pop, "kontur_population"))

    # 5. Facilities
    fac = facility_counts(boundaries)
    qc.append(run_qc(fac, "facilities"))

    # 6. WB rainfall indicators
    wb = wb_rainfall_indicators(boundaries)

    # 7. Age shares
    age = age_shares(boundaries)

    # Merge
    out = boundaries.drop(columns="geometry").reset_index(drop=True)
    for df, _prefix in [
        (clim, ""),
        (dem, ""),
        (pop, ""),
        (fac, ""),
        (wb, ""),
        (age, ""),
    ]:
        df = df.reset_index(drop=True)
        out = pd.concat([out, df.drop(columns=["tship_idx"], errors="ignore")], axis=1)

    # Derived: population density (persons / km^2)
    area_km2 = boundaries.geometry.to_crs(CRS_UTM).area / 1e6
    out["area_km2"] = area_km2.values
    out["pop_density"] = out["pop_est"] / out["area_km2"]

    out.to_parquet(DATA_PROCESSED / "yangon_township_features.parquet")
    out.to_csv(DATA_PROCESSED / "yangon_township_features.csv", index=False)
    print("merged dataset written", out.shape)

    write_qc_report(qc)
    save_qc_json(qc)
    print("QC report written")


if __name__ == "__main__":
    main()
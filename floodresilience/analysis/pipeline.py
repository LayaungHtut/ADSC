"""Core analysis pipeline: build the per-kecamatan dataset for DKI Jakarta.

Stages:
  1. Load & validate administrative boundaries (44 kecamatan).
  2. CHIRPS monthly rainfall -> zonal series (1981-2026) + derived climate
     indicators (annual total, wet-season share, extreme-month count, trend).
  3. Copernicus DEM -> elevation stats (mean/min/max).
  4. Population: Kontur H3 (current) area-weighted, WorldPop/ADM2 totals.
  5. Infrastructure: schools + health facilities counts.
  6. Flood-related rainfall indicators (World Bank / GFDRR, ADM2).
  7. Persist `data/processed/jakarta_kecamatan_features.parquet`.

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
    JAKARTA_BBOX,
    CRS_WGS84,
)
from floodresilience.cleaning.quality import QCResult, run_qc, write_qc_report, save_qc_json

BOUNDARY_SRC = DATA_RAW / "boundaries" / "alfanas" / "DKI_Jakarta_kecamatan.geojson"
CHIRPS_DIR = DATA_INTERMEDIATE / "rainfall" / "chirps"
DEM_FILES = sorted((DATA_RAW / "dem").glob("*.tif"))
KONTUR = DATA_RAW / "population" / "kontur_population_ID_20231101.gpkg.u"
ADMPOP = DATA_RAW / "population" / "idn_admpop_adm2_2020_v3.csv"
WB_RAINFALL = DATA_RAW / "rainfall_indicator" / "idn-rainfall-subnat-5ytd.csv"
EDU_DIR = DATA_RAW / "education" / "unzipped" / "IDN_school_facilities"
HEALTH_GEOJSON = DATA_RAW / "health" / "unzipped" / "hotosm_idn_health_facilities_points_geojson.geojson"
DFO = DATA_RAW / "dfo" / "Global_Flood_Records.csv"


def load_boundaries() -> gpd.GeoDataFrame:
    gdf = gpd.read_file(BOUNDARY_SRC)
    gdf["kec_code"] = gdf["KODE_KEC"].astype(str).str.strip()
    gdf["kecamatan"] = gdf["KECAMATAN"].str.title()
    gdf["kota"] = gdf["KAB_KOTA"].str.replace("Kota Administrasi ", "", regex=False).str.title()
    gdf = gdf[gdf["kota"] != "Administrasi Kepulauan Seribu"]
    gdf = gdf.reset_index(drop=True)
    return gdf[["kec_code", "kecamatan", "kota", "geometry"]]


def chirps_zonal_series(boundaries: gpd.GeoDataFrame) -> pd.DataFrame:
    """Compute mean monthly rainfall per kecamatan for every CHIRPS month."""
    files = sorted(glob.glob(str(CHIRPS_DIR / "chirps_*.tif")))
    if not files:
        raise FileNotFoundError("No CHIRPS tiles under data/intermediate/rainfall/chirps/")

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
            rec[f"kec_{i}"] = float(vals.mean()) if vals.size else np.nan
        records.append(rec)
    df = pd.DataFrame(records)
    df["month"] = pd.to_datetime(df["month"])
    df["year"] = df["month"].dt.year
    df["month_of_year"] = df["month"].dt.month
    return df


def climate_indicators(series: pd.DataFrame, n_kec: int) -> pd.DataFrame:
    """Derive per-kecamatan rainfall indicators from the monthly series."""
    rows: list[dict] = []
    for i in range(n_kec):
        col = f"kec_{i}"
        s = series[["year", "month_of_year", col]].copy()
        s = s[s[col].notna()]
        if s.empty:
            rows.append({"kec_idx": i})
            continue
        # Annual totals (complete years only: months 1-12 present)
        counts = s.groupby("year")["month_of_year"].nunique()
        complete_years = counts[counts == 12].index
        annual = s[s["year"].isin(complete_years)].groupby("year")[col].sum()
        # Monthly climatology
        clim = s.groupby("month_of_year")[col].mean()
        wet_months = [12, 1, 2, 3]
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
                "kec_idx": i,
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
    """Mosaic the four DEM tiles and compute elevation + slope stats per kecamatan."""
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
                "kec_idx": i,
                "elev_mean_m": float(ev.mean()) if ev.size else np.nan,
                "elev_min_m": float(ev.min()) if ev.size else np.nan,
                "elev_max_m": float(ev.max()) if ev.size else np.nan,
                "slope_mean_pct": float(sv.mean()) if sv.size else np.nan,
            }
        )
    return pd.DataFrame(rows)


def population_exposure(boundaries: gpd.GeoDataFrame) -> pd.DataFrame:
    """Area-weighted Kontur H3 population per kecamatan."""
    hex_gdf = gpd.read_file(KONTUR)
    # Reproject to boundaries CRS (WGS84) for intersection.
    hex_wgs = hex_gdf.to_crs(CRS_WGS84)
    joined = gpd.sjoin(hex_wgs, boundaries[["geometry"]], how="inner", predicate="intersects")
    hex_ids = joined.index.unique()
    sub = hex_wgs.loc[hex_ids].copy()

    # Ensure equal-area projection for area fractions
    b_utm = boundaries.copy().to_crs("EPSG:32748")
    sub_utm = sub.to_crs("EPSG:32748")

    rows = []
    for i in range(len(boundaries)):
        poly = b_utm.geometry.iloc[i]
        hits = sub_utm[sub_utm.intersects(poly)]
        if hits.empty:
            rows.append({"kec_idx": i, "pop_est": 0.0})
            continue
        total = 0.0
        for _, h in hits.iterrows():
            inter = h.geometry.intersection(poly)
            if inter.is_empty:
                continue
            frac = inter.area / h.geometry.area if h.geometry.area > 0 else 0.0
            total += float(h["population"]) * frac
        rows.append({"kec_idx": i, "pop_est": total})
    return pd.DataFrame(rows)


def facility_counts(boundaries: gpd.GeoDataFrame) -> pd.DataFrame:
    """Count schools and health facilities per kecamatan (points within polygon)."""
    bbox = boundaries.total_bounds
    rows = []
    # Schools
    schools = None
    for f in (EDU_DIR / "IDN_school_facilities.shp",):
        if f.exists():
            schools = gpd.read_file(f, bbox=tuple(bbox))
    if schools is not None:
        schools = schools.to_crs(CRS_WGS84)
        sj = gpd.sjoin(schools, boundaries[["geometry"]], how="inner", predicate="within")
        counts = sj.groupby("index_right").size()
        for i in range(len(boundaries)):
            rows.append({"kec_idx": i, "schools": int(counts.get(i, 0))})
    else:
        for i in range(len(boundaries)):
            rows.append({"kec_idx": i, "schools": 0})
    # Health
    health = gpd.read_file(HEALTH_GEOJSON, bbox=tuple(bbox))
    health = health.to_crs(CRS_WGS84)
    hj = gpd.sjoin(health, boundaries[["geometry"]], how="inner", predicate="within")
    hcounts = hj.groupby("index_right").size()
    for r in rows:
        r["health_facilities"] = int(hcounts.get(r["kec_idx"], 0))
    return pd.DataFrame(rows)


def wb_rainfall_indicators(boundaries: gpd.GeoDataFrame) -> pd.DataFrame:
    """Aggregate World Bank / GFDRR flood-relevant rainfall indices to kecamatan."""
    df = pd.read_csv(WB_RAINFALL)
    df["date"] = pd.to_datetime(df["date"])
    # Build PCODE -> kota name map from the WorldPop ADM2 table.
    adm = pd.read_csv(ADMPOP, usecols=["ADM2_EN", "ADM2_PCODE"])
    pcode_name = adm.drop_duplicates("ADM2_PCODE").set_index("ADM2_PCODE")["ADM2_EN"].to_dict()

    adm2 = df[(df["adm_level"] == 2) & (df["PCODE"].astype(str).str.startswith("ID31"))].copy()
    adm2["kota_raw"] = adm2["PCODE"].astype(str).map(pcode_name)
    adm2["kota"] = adm2["kota_raw"].str.replace("Kota Administrasi ", "", regex=False).str.replace("Kota ", "", regex=False).str.title()

    agg = adm2.groupby("kota").agg(
        rfh_mean=("rfh", "mean"),
        r1h_mean=("r1h", "mean"),
        r3h_mean=("r3h", "mean"),
        rfh_p95=("rfh", lambda s: np.nanpercentile(s, 95)),
        n_obs=("rfh", "size"),
    ).reset_index()
    out = pd.DataFrame({"kec_idx": range(len(boundaries))})
    out["kota"] = boundaries["kota"].values
    out = out.merge(agg, on="kota", how="left")
    out = out.drop(columns=["kota"])
    return out


def age_shares(boundaries: gpd.GeoDataFrame) -> pd.DataFrame:
    """Child (<15) and elderly (65+) population shares per kota from WorldPop ADM2."""
    adm = pd.read_csv(ADMPOP)
    adm = adm[adm["ADM1_EN"].str.contains("Jakarta", case=False, na=False)]
    adm["kota"] = adm["ADM2_EN"].str.replace("Kota Administrasi ", "", regex=False).str.replace("Kota ", "", regex=False).str.title()
    child_cols = ["T_00_04", "T_05_09", "T_10_14"]
    elder_cols = ["T_65_69", "T_70_74", "T_75Plus"]
    agg2 = adm.groupby("kota").agg(
        **{f"sum_{c}": (c, "sum") for c in child_cols + elder_cols + ["T_TL"]}
    ).reset_index()
    agg2["child_share"] = agg2[[f"sum_{c}" for c in child_cols]].sum(axis=1) / agg2["sum_T_TL"]
    agg2["elderly_share"] = agg2[[f"sum_{c}" for c in elder_cols]].sum(axis=1) / agg2["sum_T_TL"]
    out = pd.DataFrame({"kec_idx": range(len(boundaries))})
    out["kota"] = boundaries["kota"].values
    out = out.merge(agg2[["kota", "child_share", "elderly_share"]], on="kota", how="left")
    out = out.drop(columns=["kota"])
    return out


def main() -> None:
    qc: list[QCResult] = []

    boundaries = load_boundaries()
    print(f"boundaries: {len(boundaries)} kecamatan")

    qc.append(run_qc(boundaries.drop(columns="geometry").assign(geometry_len=[len(g.wkt) for g in boundaries.geometry]), "boundaries_kecamatan"))

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
    for df, prefix in [
        (clim, ""),
        (dem, ""),
        (pop, ""),
        (fac, ""),
        (wb, ""),
        (age, ""),
    ]:
        df = df.reset_index(drop=True)
        out = pd.concat([out, df.drop(columns=["kec_idx"], errors="ignore")], axis=1)

    # Derived: population density (persons / km^2)
    area_km2 = boundaries.geometry.to_crs("EPSG:32748").area / 1e6
    out["area_km2"] = area_km2.values
    out["pop_density"] = out["pop_est"] / out["area_km2"]

    out.to_parquet(DATA_PROCESSED / "jakarta_kecamatan_features.parquet")
    out.to_csv(DATA_PROCESSED / "jakarta_kecamatan_features.csv", index=False)
    print("merged dataset written", out.shape)

    write_qc_report(qc)
    save_qc_json(qc)
    print("QC report written")


if __name__ == "__main__":
    main()

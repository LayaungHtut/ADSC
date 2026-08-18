"""GIS helpers: raster zonal statistics and vector utilities.

All zonal statistics are computed by rasterizing polygon cells at the raster
resolution (area-weighted), so that boundary pixels are neither dropped nor
double counted. CRS is normalised to the source raster CRS before rasterising.
"""

from __future__ import annotations

import geopandas as gpd
import numpy as np
import rasterio
import rasterio.features
from rasterio.windows import from_bounds

from floodresilience.config import CRS_WGS84


def clip_gdf_to_bbox(gdf: gpd.GeoDataFrame, bbox: tuple[float, float, float, float]) -> gpd.GeoDataFrame:
    """Keep features intersecting the (west, south, east, north) bbox (WGS84)."""
    west, south, east, north = bbox
    from shapely.geometry import box

    clip = box(west, south, east, north)
    return gdf[gdf.geometry.intersects(clip)].copy()


def raster_zonal_stats(
    raster_path: str,
    gdf: gpd.GeoDataFrame,
    stat_names: tuple[str, ...] = ("mean", "min", "max"),
    nodata: float | None = None,
) -> gpd.GeoDataFrame:
    """Compute zonal statistics of a raster over each polygon feature.

    The polygon CRS is reprojected to the raster CRS, cells are rasterised
    onto a grid matching the raster, and valid (non-nodata) cell values are
    summarised per polygon.
    """
    with rasterio.open(raster_path) as src:
        out = gdf.copy()
        # Reproject features to raster CRS.
        if out.crs is None:
            out = out.set_crs(CRS_WGS84)
        if out.crs != src.crs:
            out = out.to_crs(src.crs)
        transform = src.transform

        means: list[float | None] = []
        mins: list[float | None] = []
        maxs: list[float | None] = []
        for _, row in out.iterrows():
            geom = row.geometry
            if geom is None or geom.is_empty:
                means.append(None); mins.append(None); maxs.append(None)
                continue
            # Raster window covering the polygon.
            bbox = geom.bounds
            window = from_bounds(*bbox, transform=transform)
            window = window.intersection(src.window(*src.bounds))
            if window.width <= 0 or window.height <= 0:
                means.append(None); mins.append(None); maxs.append(None)
                continue
            data = src.read(1, window=window)
            win_transform = src.window_transform(window)

            mask = rasterio.features.geometry_mask(
                [geom],
                out_shape=data.shape,
                transform=win_transform,
                invert=True,
                all_touched=False,
            )
            values = data[mask]
            if nodata is not None:
                values = values[values != nodata]
            values = values[values >= 0]  # CHIRPS/DEM nodata are negative
            if values.size == 0:
                means.append(None); mins.append(None); maxs.append(None)
                continue
            means.append(float(values.mean()))
            mins.append(float(values.min()))
            maxs.append(float(values.max()))

        if "mean" in stat_names:
            out["zonal_mean"] = means
        if "min" in stat_names:
            out["zonal_min"] = mins
        if "max" in stat_names:
            out["zonal_max"] = maxs
    return out


def point_counts_by_polygon(
    points: gpd.GeoDataFrame,
    polygons: gpd.GeoDataFrame,
) -> dict[str, int]:
    """Count points falling inside each polygon (spatial join)."""
    join = gpd.sjoin(points, polygons, how="inner", predicate="within")
    if "count" not in join.columns and "index_right" in join.columns:
        counts = join.groupby("index_right").size()
    else:
        counts = join.groupby("index_right")["count"].sum()
    out: dict[str, int] = {}
    for i in range(len(polygons)):
        out[i] = int(counts.get(i, 0))
    return out


def h3_hex_pop_intersection(
    hex_gdf: gpd.GeoDataFrame,
    polygons: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:
    """Intersect H3 hexagons with polygons, apportioning population by area.

    Returns the polygons with an added `pop_est` column (population estimated
    inside each polygon, weighted by hexagon overlap area).
    """
    from shapely.ops import transform as shapely_transform

    if hex_gdf.crs.is_geographic and polygons.crs.is_geographic:
        hex_utm = hex_gdf.to_crs(polygons.crs)
        polys = polygons.copy()
    else:
        hex_utm = hex_gdf.to_crs("EPSG:3857")
        polys = polygons.to_crs("EPSG:3857")

    result = polygons.copy()
    if "pop_est" not in result.columns:
        result["pop_est"] = 0.0

    # Only consider hexagons near the polygons (spatial index).
    joined = gpd.sjoin(hex_gdf, polygons[["geometry"]], how="inner", predicate="intersects")
    hex_ids = joined.index.unique()
    sub = hex_gdf.loc[hex_ids]
    sub = sub.to_crs(polys.crs)

    for idx, poly in polys.iterrows():
        p = poly.geometry
        area_poly = p.area
        hits = sub[sub.intersects(p)]
        if hits.empty:
            continue
        total = 0.0
        for _, h in hits.iterrows():
            inter = h.geometry.intersection(p)
            if inter.is_empty:
                continue
            frac = inter.area / h.geometry.area if h.geometry.area > 0 else 0.0
            total += h["population"] * frac
        result.loc[idx, "pop_est"] = total
    return result

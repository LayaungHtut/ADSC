import csv
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.collections import PatchCollection

BASE = os.path.join(os.path.dirname(__file__), "..")
SAC = os.path.join(BASE, "data", "sac")
OUT = os.path.join(BASE, "outputs", "storyboard", "charts")
os.makedirs(OUT, exist_ok=True)

NAVY = "#0B2E4F"
BLUE = "#1B6CA8"
RED = "#C0392B"
GREEN = "#1E8449"
ORANGE = "#E67E22"
GRAY = "#95A5A6"
LIGHT = "#EAF2F8"

plt.rcParams.update({
    "font.size": 9.5,
    "axes.titlesize": 10.5,
    "axes.titleweight": "bold",
    "axes.labelsize": 9,
    "axes.edgecolor": "#B0BEC5",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})

RISK_CMAP = matplotlib.colormaps["RdYlGn_r"]


def risk_class_color(klass):
    return {1: "#2E86AB", 2: "#4FB286", 3: "#E6B45A", 4: "#E67E22", 5: "#C0392B"}.get(klass, GRAY)


def read(name):
    return list(csv.DictReader(open(os.path.join(SAC, name), encoding="utf-8")))


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=100, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  chart:", name)


# ---- Page 2: documented flood years timeline ----
def flood_years():
    rows = read("sac_yangon_flood_events.csv")
    years = sorted(int(r["year"]) for r in rows)
    fig, ax = plt.subplots(figsize=(10, 1.5))
    ax.scatter(years, [1] * len(years), s=70, color=BLUE, zorder=3)
    for y in years:
        ax.annotate(str(y), (y, 1), textcoords="offset points", xytext=(0, 14), ha="center", fontsize=8)
    ax.set_xlim(1984, 2024)
    ax.set_ylim(0.7, 1.35)
    ax.set_yticks([])
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.set_title("14 documented major Yangon flood years, 1988\u20132020")
    ax.set_xlabel("Year")
    save(fig, "flood_years.png")


# ---- Page 4: region overview (district-colored) ----
def all_rings(geom):
    coords = geom["coordinates"]
    if geom["type"] == "Polygon":
        return [coords[0]]
    rings = []
    for poly in coords:
        rings.append(poly[0])
    return rings


def region_map(color_key="district", title="Yangon Region \u2014 45 townships (districts)", emphasize=None, out="region_map.png"):
    g = json.load(open(os.path.join(BASE, "data", "processed", "yangon_township_risk.geojson"), encoding="utf-8"))
    dist_colors = {"East": "#2E86AB", "North": "#4FB286", "South": "#E67E22", "West": "#8E44AD"}
    polys, cols, names = [], [], []
    for f in g["features"]:
        props = f["properties"]
        rings = all_rings(f["geometry"])
        for ring in rings:
            polys.append(MplPolygon(ring, closed=True))
        if color_key == "district":
            cols.extend([dist_colors.get(props.get("district"), GRAY)] * len(rings))
        elif color_key == "risk":
            c = RISK_CMAP((int(round(float(props.get("risk_100", 0)))) / 100.0))
            cols.extend([c] * len(rings))
        else:
            k = int(props.get("risk_class", 1))
            c = risk_class_color(k) if k == 5 and emphasize else "#DDE3E8"
            cols.extend([c] * len(rings))
        names.append(props.get("township", ""))
    patch = PatchCollection(polys, facecolor=cols, edgecolor="white", linewidth=0.6)
    fig, ax = plt.subplots(figsize=(10, 2.4))
    ax.add_collection(patch)
    ax.autoscale_view()
    ax.set_aspect("equal")
    ax.axis("off")
    for f in g["features"]:
        props = f["properties"]
        if color_key == "risk" and not emphasize:
            continue
        ring = all_rings(f["geometry"])[0]
        cx = sum(p[0] for p in ring) / len(ring)
        cy = sum(p[1] for p in ring) / len(ring)
        ax.annotate(props["township"].replace("Dagon Myothit", "Dagon M."), (cx, cy),
                    ha="center", va="center", fontsize=4.6, color="#333")
    ax.set_title(title)
    save(fig, out)


# ---- Page 6: risk formula donut ----
def risk_formula():
    fig, ax = plt.subplots(figsize=(10, 2.0))
    vals = [0.40, 0.35, 0.25]
    labs = ["Hazard\n0.40", "Exposure\n0.35", "Vulnerability\n0.25"]
    colors = [RED, ORANGE, GREEN]
    wedges, _ = ax.pie(vals, colors=colors, startangle=90, counterclock=False,
                       wedgeprops=dict(width=0.34, edgecolor="white", linewidth=2))
    ax.legend(wedges, labs, loc="center", frameon=False, fontsize=10)
    ax.set_title("Risk = 0.4\u00b7Hazard + 0.35\u00b7Exposure + 0.25\u00b7Vulnerability")
    save(fig, "risk_formula.png")


# ---- Page 7: monthly climatology ----
def climatology():
    rows = read("sac_rainfall_timeseries.csv")
    mon = {}
    for r in rows:
        m = int(r["month"])
        mon[m] = mon.get(m, []) + [float(r["rainfall_mm"])]
    months = [m for m in range(1, 13)]
    means = [sum(mon[m]) / len(mon[m]) for m in months]
    fig, ax = plt.subplots(figsize=(10, 2.0))
    bars = ax.bar(months, means, color=[BLUE] * 12)
    for i in (6, 7, 5, 8):
        bars[i].set_color(ORANGE)
    for i, v in enumerate(means):
        ax.annotate(f"{v:.0f}", (months[i], v), textcoords="offset points", xytext=(0, 3), ha="center", fontsize=7)
    ax.set_xticks(months)
    ax.set_xticklabels("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), rotation=0)
    ax.set_ylabel("mm")
    ax.set_title("Mean monthly rainfall, Yangon (CHIRPS 1981\u20132026) \u2014 wettest: Jun\u2013Sep, peak Jul 698.9 mm")
    ax.set_ylim(0, max(means) * 1.18)
    save(fig, "climatology.png")


# ---- Page 8: choropleth risk map ----
def risk_map():
    region_map(color_key="risk",
               title="Township flood risk (risk_100) \u2014 dark red = highest",
               out="risk_map.png")
    region_map(color_key="district",
               title="Yangon Region \u2014 45 townships by district",
               out="region_map.png")


# ---- Page 8: elevation vs risk scatter ----
def elev_vs_risk():
    rows = read("sac_risk_by_area.csv")
    fig, ax = plt.subplots(figsize=(10, 1.5))
    for r in rows:
        k = int(r["risk_class"])
        ax.scatter(float(r["elev_mean_m"]), float(r["risk_100"]), s=60, color=risk_class_color(k),
                   edgecolor="white", linewidth=0.6, zorder=3)
        nm = r["township"]
        if nm in ("Kayan", "Hlaingtharya", "Taikkyi", "North Okkalapa"):
            ax.annotate(nm, (float(r["elev_mean_m"]), float(r["risk_100"])),
                        textcoords="offset points", xytext=(6, 5), fontsize=7.5)
    ax.set_xlabel("Mean elevation (m)")
    ax.set_ylabel("Risk (0\u2013100)")
    ax.set_title("Low elevation aligns with high risk (color = risk class 1\u20135)")
    save(fig, "elev_vs_risk.png")


# ---- Page 9: population by risk class ----
def pop_by_class():
    rows = read("sac_risk_by_area.csv")
    pops = {}
    for r in rows:
        k = int(r["risk_class"])
        pops[k] = pops.get(k, 0) + float(r["pop_est"])
    ks = sorted(pops)
    vals = [pops[k] / 1e6 for k in ks]
    fig, ax = plt.subplots(figsize=(10, 1.9))
    bars = ax.bar([str(k) for k in ks], vals, color=[risk_class_color(k) for k in ks])
    for i, v in enumerate(vals):
        ax.annotate(f"{v:.2f} M", (i, v), textcoords="offset points", xytext=(0, 3), ha="center", fontsize=8)
    ax.set_xlabel("Risk class (1 = lowest, 5 = highest)")
    ax.set_ylabel("Population (millions)")
    ax.set_title("Population living in each risk class \u2014 class 5 holds 2.60 M people (35.3%)")
    ax.set_ylim(0, max(vals) * 1.18)
    save(fig, "pop_by_class.png")


# ---- Page 10: top-10 + decomposition ----
def top10_decomp():
    rows = read("sac_risk_by_area.csv")
    top = sorted(rows, key=lambda r: -float(r["risk_100"]))[:10]
    names = [r["township"] for r in top][::-1]
    vals = [float(r["risk_100"]) for r in top][::-1]
    colors = [risk_class_color(int(r["risk_class"])) for r in top][::-1]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 2.1), gridspec_kw={"width_ratios": [1.15, 1]})
    a1.barh(names, vals, color=colors)
    a1.set_xlabel("Risk (0\u2013100)")
    a1.set_title("Top-10 risk townships")
    a1.invert_yaxis()
    a1.tick_params(axis="y", labelsize=7)
    top5 = sorted(rows, key=lambda r: -float(r["risk_100"]))[:5]
    names5 = [r["township"] for r in top5][::-1]
    h = [[float(r["hazard"]) * 40 for r in top5][::-1],
         [float(r["exposure"]) * 35 for r in top5][::-1],
         [float(r["vulnerability"]) * 25 for r in top5][::-1]]
    a2.barh(names5, h[0], color=RED, label="Hazard")
    a2.barh(names5, h[1], left=h[0], color=ORANGE, label="Exposure")
    a2.barh(names5, h[2], left=[x + y for x, y in zip(h[0], h[1])], color=GREEN, label="Vulnerability")
    a2.set_xlabel("Weighted contribution")
    a2.set_title("Why they rank high")
    a2.invert_yaxis()
    a2.tick_params(axis="y", labelsize=7)
    a2.legend(fontsize=7, loc="lower right")
    fig.suptitle("One list, 45 townships, one decision", fontsize=11, fontweight="bold", y=1.02)
    fig.tight_layout()
    save(fig, "top10_decomp.png")


# ---- Page 11: risk histogram ----
def risk_hist():
    rows = read("sac_risk_by_area.csv")
    vals = [float(r["risk_100"]) for r in rows]
    fig, ax = plt.subplots(figsize=(10, 1.3))
    ax.hist(vals, bins=12, color=BLUE, edgecolor="white")
    ax.set_xlabel("Risk (0\u2013100)")
    ax.set_ylabel("Townships")
    ax.set_title("Distribution of township risk (mean 42.5) \u2014 right tail = highest-risk townships")
    save(fig, "risk_hist.png")


# ---- Page 12: solution KPI dashboard ----
def solution_kpis():
    rows = read("sac_risk_by_area.csv")
    top = max(rows, key=lambda r: float(r["risk_100"]))
    class5 = sum(float(r["pop_est"]) for r in rows if int(r["risk_class"]) == 5)
    fac = sum(int(r["schools"]) + int(r["health_facilities"]) for r in rows)
    fig, ax = plt.subplots(figsize=(10, 1.9))
    ax.axis("off")
    panels = [
        ("TOP RISK", f"{float(top['risk_100']):.1f}", top["township"]),
        ("CLASS-5 POPULATION", f"{class5 / 1e6:.2f} M", "people in highest-risk zone"),
        ("FACILITIES MAPPED", f"{fac:,}", "schools + health facilities"),
    ]
    for i, (lab, big, sub) in enumerate(panels):
        x0 = i / 3
        ax.axvspan(x0, x0 + 1 / 3, color=LIGHT, alpha=0.6)
        ax.text(x0 + 1 / 6, 0.66, big, ha="center", fontsize=20, fontweight="bold", color=NAVY)
        ax.text(x0 + 1 / 6, 0.4, lab, ha="center", fontsize=9, fontweight="bold", color=BLUE)
        ax.text(x0 + 1 / 6, 0.16, sub, ha="center", fontsize=8, color=GRAY)
    ax.set_title("FloodResilience ASEAN \u2014 decision-support dashboard (SAC model output)", fontsize=10.5, fontweight="bold")
    save(fig, "solution_kpis.png")


# ---- Page 14: risk classes across districts (scalability framing) ----
def district_classes():
    rows = read("sac_risk_by_area.csv")
    dists = ["East", "North", "South", "West"]
    counts = {d: {k: 0 for k in range(1, 6)} for d in dists}
    for r in rows:
        counts[r["district"]][int(r["risk_class"])] += 1
    fig, ax = plt.subplots(figsize=(10, 2.0))
    bottom = [0] * 4
    for k in range(1, 6):
        vals = [counts[d][k] for d in dists]
        ax.bar(dists, vals, bottom=bottom, color=risk_class_color(k), label=f"class {k}", width=0.55)
        bottom = [b + v for b, v in zip(bottom, vals)]
    ax.set_ylabel("Townships")
    ax.set_title("Risk classes across all four Yangon districts \u2014 the same framework works region-wide")
    ax.legend(fontsize=8, ncol=5, loc="upper center", frameon=False)
    save(fig, "district_classes.png")


# ---- Page 15: class-5 emphasis map ----
def class5_map():
    region_map(color_key="class5", title="The 9 highest-risk townships (class 5) to prioritize",
               emphasize=True, out="class5_map.png")


def main():
    print("Rendering storyboard charts from real project data ...")
    flood_years()
    risk_formula()
    climatology()
    risk_map()
    elev_vs_risk()
    pop_by_class()
    top10_decomp()
    risk_hist()
    solution_kpis()
    district_classes()
    class5_map()
    print("Done.")


if __name__ == "__main__":
    main()
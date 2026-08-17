# data/ — Data organization

```
data/
├── raw/          Original downloaded files (never modified), with PROVENANCE.md
├── intermediate/ Cleaned but not yet final (documented transformations)
├── processed/    Final analysis-ready datasets (Parquet/CSV)
├── sac/          SAC-ready clean CSV exports for SAP Analytics Cloud
└── source_catalog.csv  Machine-readable source registry (see research/sources.md)
```

Rules:
- Raw files are immutable; never edit in place.
- Every transformation is logged; nothing is silently removed.
- Every dataset entry has a source + URL + licence (source_catalog.csv).
- Personal data is never collected; only aggregate public data.
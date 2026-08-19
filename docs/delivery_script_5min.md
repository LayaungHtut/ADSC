# Team Zenith — 5-Minute Delivery Script (ASEAN DSE 2026)

> Spoken script mapped to `outputs/storyboard/MYANMAR_TEAM_ZENITH.pdf` (15 pages + references).
> Target: **300 seconds**. Two presenters (Thar Lun Myint Myat Tun = TL, La Yaung Htut = LY).
> Time budget per page below; "click" notes = live SAC filters to perform during the demo.
> Defense answers: `outputs/reports/judge_questions.md`. Score self-check: `outputs/reports/competition_scorecard.md`.

| Page | Speaker | Time | Slide |
|---|---|---|---|
| 1 Cover | TL | 10 s | FloodResilience ASEAN |
| 2 Problem | TL | 25 s | When the monsoon arrives |
| 3 Alignment | LY | 20 s | SDG & ASEAN |
| 4 Approach | LY | 15 s | One question |
| 5 Data | TL | 25 s | Open data |
| 6 Method | TL | 25 s | Risk formula |
| 7 Seasonality | LY | 20 s | When it rains |
| 8 Risk map | TL | 35 s | Where it concentrates |
| 9 Exposure | LY | 25 s | Who is exposed |
| 10 Model output | TL | 25 s | The ranking |
| 11 Insights | LY | 15 s | Four answers |
| 12 Solution | TL | 20 s | The tool |
| 13 Implementation | LY | 15 s | Roadmap |
| 14 Scalability | TL | 15 s | ASEAN scale |
| 15 Conclusion | TL | 20 s | Call to action |
| buffer / transitions | — | 10 s | — |
| **Total** | | **300 s** | |

---

## Page 1 — Cover (TL, 10 s)
> "Good afternoon. We are Team Zenith from the University of Information Technology, Myanmar.
> Our storyboard is FloodResilience ASEAN — a data-driven flood risk intelligence tool for Yangon,
> built on SDG 11 and 13. This is our 5-minute pitch."

## Page 2 — The Problem (TL, 25 s)
> "Yangon floods are not hypothetical. We have documented 14 major flood years since 1988, Myanmar
> records 33 national flood events, and the monsoon peaks at nearly 700 millimetres in July.
> Seven million people live across 45 townships. The question was never *if* a flood comes —
> it is *where* it will hurt most."
*(Hand to LY on the last sentence.)*

## Page 3 — Why It Matters (LY, 20 s)
> "This is not a local exercise. We anchor every output to SDG 11.5 and 11.b, SDG 13.1 and 13.3,
> and to the ASEAN Blueprint elements B.2 and D.4 — equitable access and protecting vulnerable
> communities. That alignment is what makes the work relevant, fundable and repeatable."

## Page 4 — Our Approach (LY, 15 s)
> "One question drives everything: *which townships face the highest flood risk, and which people,
> schools and clinics are exposed there?* Our pipeline runs open data through hazard, exposure and
> vulnerability, then into SAP Analytics Cloud. And we state our limits up front — this is relative
> township risk, not a flood forecast."

## Page 5 — The Data (TL, 25 s)
> "Credibility comes from the data. 547 months of satellite rainfall from CHIRPS, elevation from the
> Copernicus DEM, population and age structure from the official 2014 Census, flood events from the
> Dartmouth Flood Observatory, and 1,320 schools and 1,178 health facilities from OpenStreetMap.
> Every single number on every slide is open, cited and traceable."

## Page 6 — Method (TL, 25 s)
> "The model is transparent, not a black box. Risk equals 0.4 hazard, plus 0.35 exposure, plus
> 0.25 vulnerability. We tested robustness — re-running with plus or minus 10 percent shifts a
> township's rank by only four positions on average. And rainfall genuinely predicts extremes:
> our extreme-rainfall classifier scores 0.949 area under the curve."

## Page 7 — Seasonality (LY, 20 s)
> "The data tells us *when*. July peaks at 699 millimetres; June to September are the four wettest
> months. Flood years average about 59 millimetres wetter than the long-run mean — so wet years are
> measurably dangerous years. We deliberately do not overclaim a climate trend; variability dominates."

## Page 8 — Risk Map (TL, 35 s)
> *(Click: highlight class-5 townships; click district filter to South, then back to all.)*
> "Now the *where*. The risk map ranks all 45 townships. The highest-risk five are Kayan at 58.3,
> Thongwa, North Okkalapa, Thanlyin and Hlaingtharya. Notice the pattern — the lowest-lying
> townships along the Yangon, Bago and Hlaing rivers and the delta fringe are exactly where risk
> concentrates. Geography is the story."

## Page 9 — Exposure (LY, 25 s)
> "Risk is people and services, not polygons. 2.6 million people — 35 percent of the region — live
> in the highest-risk townships. East Yangon holds 2.37 million, North 2.6 million, South 1.4 million,
> West under a million. And schools and clinics exist in every township, so no flood is ever free of
> public-service impact."

## Page 10 — The Ranking (TL, 25 s)
> *(Click: Top-N 10, then decomposition for Kayan.)*
> "One list, 45 townships, one decision. The top ten makes clear who needs early warning and drainage
> investment first. And the decomposition shows *why* — Kayan and Thongwa rank high on hazard and
> vulnerability, North Okkalapa on exposure. This is a list a decision-maker can actually act on."

## Page 11 — Key Insights (LY, 15 s)
> "Four evidence-backed answers. Flood years are wet years. Risk follows elevation and the rivers.
> Exposure is concentrated while services are everywhere. And the ranking is robust. We attach a
> limitation to every insight — that honesty is part of the analysis."

## Page 12 — Solution (TL, 20 s)
> "Analysis only matters if it changes a decision. FloodResilience ASEAN turns the SAC model into a
> tool anyone can use — a live risk explorer for 45 townships, a scenario engine that re-ranks
> townships as conditions change, and a facility locator. The web prototype is open; the analytics
> engine is SAP Analytics Cloud."

## Page 13 — Implementation (LY, 15 s)
> "And we have a plan. Phase one, six months, validates with the Yangon DRR office and issues risk
> briefs to five townships. Phase two makes the tool public and links it to monsoon early warning.
> Phase three replicates the pipeline to a second ASEAN city. No invented budgets — costs depend on
> the host government."

## Page 14 — ASEAN Scalability (TL, 15 s)
> "Everything here is reusable. CHIRPS, the DEM, census and facility data exist for every ASEAN
> country. Replication is three steps: fetch open layers for the target city, run the documented
> pipeline, import to SAC. Low marginal cost — that is viability."

## Page 15 — Conclusion (TL, 20 s)
> "The next monsoon is coming. We now know where it will hurt and what to do about it. Prioritize
> Kayan, Thongwa, North Okkalapa, Thanlyin and Hlaingtharya first — then replicate across ASEAN.
> Team Zenith, University of Information Technology, Myanmar. Our data, method and tool are open and
> cited. Thank you."

---

## Presenter checklist
- [ ] Rehearse twice to time; pause 1 s on each page transition (buffer = 10 s).
- [ ] Live demo clicks: Page 8 (district filter), Page 10 (Top-N + decomposition), Page 11 (Smart
      Discovery screenshot). Keep each click under 5 s — have the filters pre-loaded.
- [ ] Never say "we predicted" — say "we ranked" and cite the source for every headline number.
- [ ] Prototype screenshots must be captioned "prototype"; SAC charts must be real (build them first).
- [ ] Know the 3 hardest defense questions from `outputs/reports/judge_questions.md` (census 2014
      vintage, DEM vs flood depth, OSM facility completeness) — each has a limitation line in the script.
- [ ] Bring the PDF backup on a USB in case the SAC demo fails — the storyboard stands alone.
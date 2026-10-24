# The Bullet Club Effect

A data-driven study of Bullet Club's footprint, 2013-2026, built from the Bullet Club Impact Database workbook.

## Contents

| File | What it is |
|---|---|
| `The_Bullet_Club_Effect_Report.pdf` | 7-page research report with 7 figures, 2 tables and a sensitivity analysis. Start here. |
| `bullet_club_dashboard.html` | Self-contained interactive dashboard. Open in any browser, no internet needed. Tabs: Overview, Index, Members (click a name for a profile), Timeline, Money, Audience, Titles, Lineage (family tree), Gaps. |
| `data/Bullet_Club_Impact_Database_EXHAUSTIVE_PUBLIC_RESEARCH.xlsx` | The source database. Every figure in the report and dashboard comes from here. |
| `figures/` | The seven report figures as PNGs (f1 roster, f2 index, f3 sensitivity, f4 Hot Topic, f5 promotions, f6 causal chain, f7 lineage). |
| `code/` | Scripts that regenerate everything. |

## Main findings

- Bullet Club operated across at least seven partner promotions and seeded successor groups in AEW, WWE and Impact/TNA.
- Merchandise evidence is strong (Hot Topic reorders 5.6x the initial order in 2017; six of PWT's top ten wrestler sellers in 2018 were BC/Elite-linked) but contains no revenue figure.
- The annual footprint index peaks in 2023 under equal weights, but the peak is not robust: it moves to 2017 when merchandise is weighted up or audience is excluded. Two eras compete for the peak (2017-18 and 2023).
- The evidence shows association, not cause. It does not establish that Bullet Club caused AEW.

## Known limitations

- Exact merchandise revenue/profit, NJPW World viewership and complete ROH/TNA ratings are not public and are not estimated.
- Titles are undated in the workbook, so they are not in the annual index.
- Merchandise unit data exist only for 2017; the merch measure is effectively a one-year marker.
- AEW ratings were recovered only for 2023-24, so the 2023 audience score reflects data coverage as much as reach.
- The workbook's Dashboard sheet says 68 roster entries; the Members sheet contains 69. Not reconciled.
- Leadership-era boundaries in Figure 1 are approximate.

## Regenerating

Requires Python 3 with openpyxl, numpy, matplotlib and reportlab. The scripts use the original sandbox paths (`/mnt/user-data/...`); edit the paths at the top of each script to run them locally.

1. `model.py` computes the index and sensitivity results.
2. `figs.py` draws the figures (needs `model.py` in the same folder).
3. `report.py` builds the PDF (needs the figures).
4. `build.py` embeds the workbook data into `t.html` to produce the dashboard.

## Not included

The online Word-style draft doc is superseded by the PDF and not packaged.

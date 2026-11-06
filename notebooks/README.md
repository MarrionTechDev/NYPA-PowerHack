# notebooks/

**Owners:** Data lead (`01_clean`), Analyst (`02_analysis`)

## Purpose
Where the data work happens and where the reasoning is recorded.

## What goes in this folder
| File | What it does | Owner |
|---|---|---|
| `01_clean.ipynb` | Reads `data/raw.csv`, cleans it, validates it, writes `data/clean.csv`. | Data lead |
| `02_analysis.ipynb` | Reads `data/clean.csv`, explores it, prototypes charts as functions, and records 3 to 5 insights. | Analyst |

## What this folder does
- `01_clean` is the only thing that creates `clean.csv`, so the cleaning is reproducible and explainable to the judges.
- `02_analysis` produces two things for the team: finished chart functions (moved into `dashboard/charts.py`) and the written insights the Presenter turns into slides.

## Rules
1. Notebooks must run top to bottom without errors (Runtime > Restart and run all) before you call them done.
2. `02_analysis` reads `clean.csv` only, never `raw.csv`.
3. Write each insight as one sentence with the number in it (for example, "Category X is 42% of total").
4. No stray scratch notebooks here. Keep experiments in your own copy.

## Done when
- [ ] `01_clean` runs cleanly and has produced `clean.csv`
- [ ] `02_analysis` runs cleanly on `clean.csv`
- [ ] Final chart functions are copied into `dashboard/charts.py`
- [ ] 3 to 5 insights are written at the bottom of `02_analysis` and shared with the Presenter

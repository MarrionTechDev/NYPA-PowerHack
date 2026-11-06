# data/

**Owner:** Data lead

## Purpose
The single source of truth for the dataset. Everyone else reads from here and nobody edits the files by hand.

## What goes in this folder
| File | What it is | Who writes it |
|---|---|---|
| `raw.csv` | The original dataset exactly as received. Never modified. | Nobody (just drop it in) |
| `clean.csv` | The cleaned dataset the whole team uses. | Only `notebooks/01_clean.ipynb` |
| `DATA_CONTRACT.txt` | Column names, types, allowed values, how missing values are handled. | Data lead |

## What this folder does
- `raw.csv` goes in, `01_clean.ipynb` turns it into `clean.csv`, and the Analyst and Dashboard lead build on `clean.csv`.
- `DATA_CONTRACT.txt` is the agreement between the three technical roles: if a column changes, update the contract and tell the team.

## Rules
1. Never edit `raw.csv` or `clean.csv` manually. Re-run the notebook instead.
2. Upload a rough first `clean.csv` as early as possible so the others can start. A better version can replace it later.
3. `raw.csv` stays on Drive only (it is git-ignored). `clean.csv` goes to Drive and the GitHub repo.

## Done when
- [ ] `raw.csv` is here
- [ ] `DATA_CONTRACT.txt` lists every column of `clean.csv`
- [ ] `clean.csv` is here, on Drive and committed to the repo
- [ ] The team has been told it's ready

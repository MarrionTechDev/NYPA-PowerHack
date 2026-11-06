# dashboard/

**Owners:** Dashboard lead (`app.py`), Analyst (`charts.py`)

## Purpose
The live app that gets demoed. This folder mirrors the GitHub repo.

## What goes in this folder
| File | What it does | Owner |
|---|---|---|
| `app.py` | The Streamlit app: loads `data/clean.csv`, lays out the page, calls the chart functions. | Dashboard lead |
| `charts.py` | One function per chart (DataFrame in, figure out) plus a `CHARTS` registry the app reads. | Analyst |
| `requirements.txt` | Python packages needed to run the app. | Dashboard lead |

## What this folder does
- The Analyst builds charts in `02_analysis.ipynb`, then moves the finished functions into `charts.py`.
- The Dashboard lead imports them in `app.py`, so the two roles never edit the same file.

## How to run
    pip install -r dashboard/requirements.txt
    streamlit run dashboard/app.py

Run it from the project root so the app can find `data/clean.csv`.

## Rules
1. `charts.py` has no file reading and no Streamlit calls, only data in and a figure out.
2. Add every new package to `requirements.txt` right away.
3. Commit small and often. Pull before you push.
4. Code freeze one hour before presenting. After that, only fix crashes.

## Done when
- [ ] `streamlit run dashboard/app.py` works on a fresh machine
- [ ] Every chart the demo needs is in `charts.py`
- [ ] The latest version is pushed to GitHub
- [ ] The Presenter has run the demo once from start to finish

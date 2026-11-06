"""app.py  (owner: Dashboard lead)

Run:  streamlit run dashboard/app.py   (from the PowerHack/ folder)

Reads data/clean.csv and renders the chart functions from charts.py.
"""
from pathlib import Path

import pandas as pd
import streamlit as st

import charts

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "clean.csv"

st.set_page_config(page_title="PowerHack Dashboard", layout="wide")
st.title("PowerHack Dashboard")


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


if not DATA_PATH.exists():
    st.warning(f"Waiting for {DATA_PATH.name}. The Data lead produces it with notebooks/01_clean.ipynb.")
    st.stop()

df = load_data(DATA_PATH)

# ---- Sidebar ---------------------------------------------------------------
st.sidebar.header("Controls")
chart_name = st.sidebar.selectbox("Chart", list(charts.CHARTS))
cols = df.columns.tolist()
num_cols = df.select_dtypes("number").columns.tolist()

# TODO: replace these generic pickers with real filters once DATA_CONTRACT.txt is filled in.
x_col = st.sidebar.selectbox("X / category / date column", cols)
y_col = st.sidebar.selectbox("Value column", num_cols or cols)

# ---- Main ------------------------------------------------------------------
c1, c2, c3 = st.columns(3)
c1.metric("Rows", f"{len(df):,}")
c2.metric("Columns", len(cols))
c3.metric("Missing cells", int(df.isna().sum().sum()))

fig = charts.CHARTS[chart_name](df, x_col, y_col)
st.plotly_chart(fig)

with st.expander("Data preview"):
    st.dataframe(df.head(100))

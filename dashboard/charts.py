"""charts.py  (owner: Analyst)

Every chart is a plain function: DataFrame in, Plotly figure out.
The dashboard (app.py) imports these, so the Analyst can prototype them in
notebooks/02_analysis.ipynb and drop the finished versions here.

Rules:
  - No file reading, no Streamlit calls in this module.
  - Code against data/DATA_CONTRACT.txt column names.
  - Each function gets a one-line docstring: that line becomes the chart caption.
"""
import pandas as pd
import plotly.express as px


def example_bar(df: pd.DataFrame, category: str, value: str):
    """Total of `value` by `category`."""
    agg = df.groupby(category, as_index=False)[value].sum().sort_values(value, ascending=False)
    return px.bar(agg, x=category, y=value, title=f"{value} by {category}")


def example_line(df: pd.DataFrame, date: str, value: str):
    """`value` over time."""
    agg = df.groupby(date, as_index=False)[value].sum().sort_values(date)
    return px.line(agg, x=date, y=value, title=f"{value} over time")


# Registry used by the dashboard sidebar. Add new charts here.
CHARTS = {
    "Bar: by category": example_bar,
    "Line: over time": example_line,
}

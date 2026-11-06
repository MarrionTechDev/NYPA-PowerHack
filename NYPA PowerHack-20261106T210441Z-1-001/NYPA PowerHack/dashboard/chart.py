"""Chart + calculations for the Minimum energy-mix view."""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

FUELS = ["natural_gas", "dual_fuel", "nuclear", "hydro", "wind",
         "other_renewables", "other_fossil"]
FOSSIL = ["natural_gas", "dual_fuel", "other_fossil"]
LABELS = {"natural_gas": "Natural Gas", "dual_fuel": "Dual Fuel", "nuclear": "Nuclear",
          "hydro": "Hydro", "wind": "Wind", "other_renewables": "Other Renewables",
          "other_fossil": "Other Fossil"}
FOSSIL_COLOR, CLEAN_COLOR = "#8a5a44", "#2a7f62"
MWH_COLS = [f + "_mwh" for f in FUELS]
SEASONS = ["Summer", "Winter", "Fall", "Spring"]
SEASON_COLORS = {"Winter": "#3b6fb6", "Spring": "#7fb069",
                 "Summer": "#e4572e", "Fall": "#e0a526"}
_MONTH_TO_SEASON = {12: "Winter", 1: "Winter", 2: "Winter", 3: "Spring", 4: "Spring",
                    5: "Spring", 6: "Summer", 7: "Summer", 8: "Summer", 9: "Fall",
                    10: "Fall", 11: "Fall"}


def check_totals(monthly: pd.DataFrame) -> float:
    """Max gap between the sum of the 7 fuels and total_mwh (should be 0)."""
    return float((monthly[MWH_COLS].sum(axis=1) - monthly["total_mwh"]).abs().max())


def yearly_shares(monthly: pd.DataFrame) -> pd.DataFrame:
    """Yearly share (%) per fuel = yearly fuel MWh / yearly total MWh.
    Sums MWh first; never averages monthly percentages."""
    yr = monthly.groupby("year")[MWH_COLS + ["total_mwh"]].sum()
    shares = yr[MWH_COLS].div(yr["total_mwh"], axis=0) * 100
    shares.columns = FUELS
    shares["fossil"] = shares[FOSSIL].sum(axis=1)
    shares["zero_carbon"] = 100 - shares["fossil"]
    shares["total_TWh"] = yr["total_mwh"] / 1e6
    return shares


def energy_mix_chart(shares: pd.DataFrame, years=None):
    """Sorted horizontal bars, one panel per selected year."""
    years = list(years) if years else list(shares.index)
    order = shares.loc[years[-1], FUELS].sort_values().index
    fig, axes = plt.subplots(1, len(years), figsize=(4.6 * len(years) + 1, 4.8),
                             sharex=True, sharey=True, squeeze=False)
    for ax, y in zip(axes[0], years):
        vals = shares.loc[y, order]
        bars = ax.barh([LABELS[f] for f in order], vals,
                       color=[FOSSIL_COLOR if f in FOSSIL else CLEAN_COLOR for f in order])
        for b, v in zip(bars, vals):
            ax.text(v + 0.4, b.get_y() + b.get_height() / 2, f"{v:.1f}%",
                    va="center", fontsize=9)
        ax.set_title(f"{y}  ({shares.loc[y, 'total_TWh']:.0f} TWh)")
        ax.set_xlim(0, shares[FUELS].to_numpy().max() * 1.2)
        ax.set_xlabel("% of New York generation")
        ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle("Where New York's electricity is generated, by fuel",
                 fontsize=13, x=0.01, ha="left")
    fig.text(0.01, 0.01, "Source: NYISO real-time fuel mix (P-63), 2023-2025. Generation in "
             "New York; excludes imports and rooftop solar.  Brown = fossil, green = zero-carbon.",
             fontsize=7.5)
    fig.tight_layout(rect=(0, 0.05, 1, 0.94))
    return fig


def seasonal_daily(monthly: pd.DataFrame) -> pd.DataFrame:
    """Add date, season and avg_daily_gwh (total MWh / days in month / 1000).
    Dividing by days in month keeps February and 31-day months comparable.
    Season is derived from month (Dec-Feb = Winter) so it needs no extra column."""
    df = monthly.copy()
    df["date"] = pd.to_datetime(dict(year=df["year"], month=df["month"], day=1))
    df["season"] = df["month"].map(_MONTH_TO_SEASON)
    df["avg_daily_gwh"] = df["total_mwh"] / df["date"].dt.days_in_month / 1000
    return df


def season_averages(monthly: pd.DataFrame) -> pd.Series:
    """Mean avg-daily GWh per season across all months, ordered Summer, Winter, Fall, Spring."""
    return seasonal_daily(monthly).groupby("season")["avg_daily_gwh"].mean().reindex(SEASONS)


def seasonal_chart(monthly: pd.DataFrame):
    """Left: every month coloured by season, each year's peak labelled.
    Right: average per season."""
    df = seasonal_daily(monthly)
    avg = season_averages(monthly)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.8),
                                   gridspec_kw={"width_ratios": [3, 1]})
    ax1.bar(df["date"], df["avg_daily_gwh"], width=25,
            color=df["season"].map(SEASON_COLORS))
    for _, r in df.loc[df.groupby("year")["avg_daily_gwh"].idxmax()].iterrows():
        ax1.annotate(f"{r['date']:%b %Y}\n{r['avg_daily_gwh']:.0f}",
                     (r["date"], r["avg_daily_gwh"]), ha="center", va="bottom",
                     fontsize=9, fontweight="bold")
    ax1.set_ylabel("GWh per day")
    ax1.set_ylim(0, df["avg_daily_gwh"].max() * 1.18)
    ax1.set_title("Average daily generation by month")
    ax1.legend(handles=[Patch(color=SEASON_COLORS[s], label=s) for s in SEASON_COLORS],
               ncol=4, loc="upper left", frameon=False)
    bars = ax2.bar(SEASONS, avg, color=[SEASON_COLORS[s] for s in SEASONS])
    ax2.bar_label(bars, fmt="%.0f", padding=3)
    ax2.set_ylim(0, avg.max() * 1.18)
    ax2.set_title("Season average")
    for ax in (ax1, ax2):
        ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle("Summer and winter peaks vs. spring and fall",
                 fontsize=13, x=0.01, ha="left")
    fig.text(0.01, 0.01, "Source: NYISO real-time fuel mix (P-63), 2023-2025. Generation in "
             "New York; excludes imports and rooftop solar. Winter = Dec-Feb.", fontsize=7.5)
    fig.tight_layout(rect=(0, 0.05, 1, 0.94))
    return fig

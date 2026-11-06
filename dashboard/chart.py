"""Chart + calculations for the Minimum energy-mix view."""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

FUELS = ["natural_gas", "dual_fuel", "nuclear", "hydro", "wind",
         "other_renewables", "other_fossil"]
FOSSIL = ["natural_gas", "dual_fuel", "other_fossil"]
LABELS = {"natural_gas": "Natural Gas", "dual_fuel": "Dual Fuel", "nuclear": "Nuclear",
          "hydro": "Hydro", "wind": "Wind", "other_renewables": "Other Renewables",
          "other_fossil": "Other Fossil"}
FOSSIL_COLOR, CLEAN_COLOR = "#8a5a44", "#2a7f62"
MWH_COLS = [f + "_mwh" for f in FUELS]


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

import pandas as pd
import streamlit as st
from chart import FUELS, LABELS, check_totals, yearly_shares, energy_mix_chart

st.set_page_config(page_title="NY Electricity Mix", layout="wide")
st.title("Where does New York's electricity come from?")
st.caption("NYISO real-time fuel mix (P-63), 2023-2025. Generation in New York; "
           "excludes imports and rooftop solar.")

DEFAULT_PATH = "nyiso_fuel_mix_monthly_2023_2025.csv"   # put the CSV next to app.py


@st.cache_data
def load(path_or_file):
    return pd.read_csv(path_or_file)


try:
    monthly = load(DEFAULT_PATH)
except FileNotFoundError:
    up = st.file_uploader("Upload the monthly CSV", type="csv")
    if up is None:
        st.stop()
    monthly = load(up)

gap = check_totals(monthly)
shares = yearly_shares(monthly)

years = st.multiselect("Years", list(shares.index), default=list(shares.index))
if not years:
    st.stop()

st.pyplot(energy_mix_chart(shares, years))

first, last = shares.index[0], shares.index[-1]
c1, c2, c3 = st.columns(3)
c1.metric(f"Fossil share {last}", f"{shares.loc[last, 'fossil']:.1f}%",
          f"{shares.loc[last, 'fossil'] - shares.loc[first, 'fossil']:+.1f} pts vs {first}",
          delta_color="inverse")
c2.metric(f"Wind share {last}", f"{shares.loc[last, 'wind']:.1f}%",
          f"{shares.loc[last, 'wind'] - shares.loc[first, 'wind']:+.1f} pts vs {first}")
c3.metric(f"Hydro share {last}", f"{shares.loc[last, 'hydro']:.1f}%",
          f"{shares.loc[last, 'hydro'] - shares.loc[first, 'hydro']:+.1f} pts vs {first}")

with st.expander("Show the numbers and checks"):
    st.write(f"Max gap between sum of fuels and total: {gap:.0f} MWh (should be 0)")
    st.write("Each year's shares sum to:",
             shares[FUELS].sum(axis=1).round(6).tolist())
    st.dataframe(shares.rename(columns=LABELS).round(2).T)

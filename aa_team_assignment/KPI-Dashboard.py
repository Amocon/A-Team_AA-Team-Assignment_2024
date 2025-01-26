"""This code is the optimized (mostly styling) version from chat-gpt of a code I have written"""
import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
import pytz

# Run via: "poetry run streamlit run KPI-Dashboard.py"

# -------------------------------------------------------------
# 1) PAGE CONFIG & TITLE
# -------------------------------------------------------------
st.set_page_config(page_title="KPI Dashboard", layout="wide")

st.title("⚡ EV Charging KPI Dashboard")
st.markdown("""
<style>
.big-metric {
    font-size: 1.2rem;
    font-weight: 600;
    color: #4CAF50; /* green-ish */
}
hr {
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data(file_path):
    """Loads the feather file into a DataFrame."""
    try:
        df = pd.read_feather(file_path)
        return df
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# -------------------------------------------------------------
# 2) LOAD KPI DATA
#    Make sure kpi_df has these columns:
#    ['local_hour', 'total_kWh', 'session_count', 'loading_utilization']
# -------------------------------------------------------------
kpi_df = load_data('../data/kpi_df.feather')

if kpi_df.empty:
    st.stop()

# -------------------------------------------------------------
# 3) SINGLE HOUR KPI LOOKUP
# -------------------------------------------------------------
st.subheader("1) Single-Hour KPI Lookup")

col1, col2 = st.columns(2)

with col1:
    selected_date = st.date_input("Select a date:", datetime.today().date())

with col2:
    selected_time = st.time_input("Select a time (hourly steps):", step=timedelta(hours=1))

# Combine into a datetime localized to Burbank (America/Los_Angeles)
burbank_tz = pytz.timezone('America/Los_Angeles')
selected_datetime_naive = datetime.combine(selected_date, selected_time)
selected_datetime_burbank = burbank_tz.localize(selected_datetime_naive).replace(
    minute=0, second=0, microsecond=0
)

st.write(f"**Selected Date and Time (Burbank):** {selected_datetime_burbank}")

def get_kpis(time: datetime, df: pd.DataFrame):
    """
    Given a Burbank-localized datetime, return the row of KPIs for that hour.
    Assumes df['local_hour'] is also in America/Los_Angeles time.
    """
    row = df.loc[df["local_hour"] == time]
    if row.empty:
        return None
    # Return a single dict with the KPI values
    return {
        "session_count": row["session_count"].iloc[0],
        "total_kWh": row["total_kWh"].iloc[0],
        "loading_utilization": row["loading_utilization"].iloc[0],
    }

kpis = get_kpis(selected_datetime_burbank, kpi_df)
if kpis is None:
    st.warning("No data found for the selected date and time.")
else:
    st.success("**KPIs for this hour:**")
    st.markdown(f"""
    <div class="big-metric">Session Count: {kpis['session_count']}</div>
    <div class="big-metric">Total kWh: {kpis['total_kWh']:.2f}</div>
    <div class="big-metric">Loading Utilization: {kpis['loading_utilization']:.2f}</div>
    """, unsafe_allow_html=True)

st.markdown("<hr/>", unsafe_allow_html=True)

# -------------------------------------------------------------
# 4) KPI TREND OVER A TIME RANGE
# -------------------------------------------------------------
st.subheader("2) KPI Trend Over Time")

col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input("Start date:", datetime.today().date() - timedelta(days=7))
with col2:
    end_date = st.date_input("End date:", datetime.today().date())

# Convert start & end to local Burbank datetimes.
start_dt_naive = datetime.combine(start_date, datetime.min.time())
end_dt_naive = datetime.combine(end_date, datetime.max.time())

start_dt_burbank = burbank_tz.localize(start_dt_naive)
end_dt_burbank = burbank_tz.localize(end_dt_naive)

# Filter the KPI DF by the selected date range
filtered_df = kpi_df[(kpi_df['local_hour'] >= start_dt_burbank) &
                     (kpi_df['local_hour'] <= end_dt_burbank)].copy()

if filtered_df.empty:
    st.warning("No data for the selected date range.")
else:
    # Let user pick which metrics to chart
    available_metrics = ["total_kWh", "session_count", "loading_utilization"]
    selected_metrics = st.multiselect(
        "Pick metrics to visualize:",
        available_metrics,
        default=["total_kWh", "session_count"]
    )

    # "Melt" the data for Altair (long format)
    # If user picks no metrics, skip
    if len(selected_metrics) > 0:
        df_long = filtered_df.melt(
            id_vars="local_hour",
            value_vars=selected_metrics,
            var_name="Metric",
            value_name="Value"
        )

        # Create a line chart with Altair
        line_chart = alt.Chart(df_long).mark_line(point=True).encode(
            x=alt.X("local_hour:T", title="Local Hour"),
            y=alt.Y("Value:Q", title="Value"),
            color="Metric:N"
        ).properties(
            width="container",
            height=400
        ).interactive()

        st.altair_chart(line_chart, use_container_width=True)

        st.markdown("**Data Preview**:")
        st.dataframe(filtered_df[["local_hour"] + selected_metrics].head(10))

    else:
        st.info("Select at least one metric to see a chart.")
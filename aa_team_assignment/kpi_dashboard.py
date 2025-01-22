import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

def get_count(time: datetime):
    try:
        return  counting_df.loc[counting_df["local_hour"] == time]["session_count"].iloc[0]
    except:
        return 0

# poetry run streamlit run KPI-Dashboard.py"

st.title("Connection Count Viewer")
st.write("Select a date and time to view the number of connections.")


@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_feather(file_path)
        return df
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()


counting_df = load_data('../data/kpi_df.feather')

if counting_df.empty:
    st.stop()

selected_date = st.date_input(
    "Select a date:",
    datetime.today().date()
)

selected_time = st.time_input(
    "Select a time:",
    step=timedelta(hours=1)
)

selected_datetime_naive = datetime.combine(selected_date, selected_time)
burbank_tz = pytz.timezone('America/Los_Angeles')
selected_datetime_burbank = burbank_tz.localize(selected_datetime_naive).replace(minute=0, second=0, microsecond=0)



st.write(f"**Selected Date and Time (Burbank):** {selected_datetime_burbank}")

try:
    connection_count = get_count(selected_datetime_burbank)
    st.success(f"**Connections at {selected_datetime_burbank}:** {connection_count}")
except KeyError:
    st.warning("No data found for the selected date and time.")
except Exception as e:
    st.error(f"An error occurred: {e}")


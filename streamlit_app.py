import altair as alt
import streamlit as st
import altair as alt

"""
# City weather analysis - Temperature Threshold

Select your temperature threshold for which you want to find how many days a year, on average, are above that temperature in the selected location (currently set for Seattle)

"""

@st.cache_data
def fetch_data():
    conn = st.connection('snowflake')
    query = """
        SELECT 
            DOY_STD,
            (AVG_OF__DAILY_AVG_TEMPERATURE_FEELSLIKE_F - 32) * 5.0 / 9 AS AVG_TEMP_C,
            (AVG_OF__DAILY_MAX_TEMPERATURE_FEELSLIKE_F - 32) * 5.0 / 9 AS MAX_TEMP_C,
            (AVG_TEMP_C + MAX_TEMP_C) / 2 AS DAY_TEMP_C
        FROM STANDARD_TILE.CLIMATOLOGY_DAY 
        WHERE POSTAL_CODE = '98126' -- Seattle
        ORDER BY DOY_STD ASC
    """
    climatology_data = conn.query(query)
    return climatology_data

climatology_data = fetch_data()
#st.line_chart(climatology_data, x="DOY_STD")
days = 1

def query_days():
    days = climatology_data.where(climatology_data["DAY_TEMP_C"] >= temp_threshold).count()[0]
    return days

temp_threshold = st.slider("Temperature threshold (°C)", 0, 50, 18, on_change=query_days)
days = query_days()

"""
## Temperature chart

The horizontal green line is your threshold

"""

st.write("There are " + str(days) + " days on average at or above " + str(temp_threshold) + " °C a year in Seattle.")

alt_chart = (
   alt.Chart(climatology_data)
   .encode(x="DOY_STD")
)
chart = alt.layer(
    alt_chart.mark_line(color='#6822D3').encode(y='MAX_TEMP_C'),
    alt_chart.mark_line(color='#D32234').encode(y='DAY_TEMP_C'),
    alt_chart.mark_line(color='#2234D3').encode(y='AVG_TEMP_C'),
    alt_chart.mark_rule(color='#2BAF1C').encode(x=alt.datum(0),x2=alt.datum(365), y=alt.datum(temp_threshold))
)


st.altair_chart(chart, use_container_width=True)
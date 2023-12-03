import altair as alt
import streamlit as st
import altair as alt

"""
# City Climate Analysis

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

st.markdown("""
    <style>
    .big-font {
        font-size:20px !important;
        color: #E03F50;
    }
    </style>
    """, unsafe_allow_html=True)
st.markdown("There are <span class=\"big-font\">**" + str(days) + "**</span> days on average at or above " + str(temp_threshold) + " °C a year in Seattle.",unsafe_allow_html=True)

"""
## Temperature chart

"""

st.write("There are 3 lines in the chart:")
st.markdown("""● The <span style='color:#7F3FE0'>purple</span> line is the maximum temperature of that day.<br/>
            ● The <span style='color:#D32234'>red</span> line is 'Day temperature', is obtained by averaging the two other lines.<br/>
            ● The <span style='color:#3F50E0'>blue</span> line is the mean temperature of that day.""",unsafe_allow_html=True)

st.write("Here we're looking for how many days in the red line are above the threshold.")

alt_chart = (
   alt.Chart(climatology_data)
   .encode(alt.X('DOY_STD', title='Day of the year'))
)
chart = alt.layer(
    alt_chart.mark_line(color='#7F3FE0').encode(y=alt.Y('MAX_TEMP_C', title='Temperature (°C)')),
    alt_chart.mark_line(color='#D32234').encode(y='DAY_TEMP_C'),
    alt_chart.mark_line(color='#3F50E0').encode(y='AVG_TEMP_C'),
    alt_chart.mark_rule(color='#2BAF1C').encode(x=alt.datum(0),x2=alt.datum(365), y=alt.datum(temp_threshold))
)


st.altair_chart(chart, use_container_width=True)

st.markdown("**Note**: The 'Day temperature' concept was created as a way to try and represent an approximation of the temperature a given day actually feels like. The average temperature is biased down by the minimum, which happens at 2 or 3 in the morning, and the maximum temperature is only reality for a few hours in the day, so neither represent how a day feels like, in general.<br/>Perhaps a better way would be something like 'days with more than X hours at or above the threshold temperature', but mean of avg and max are good enough to work with for now.",unsafe_allow_html=True)
st.markdown("**Note 2**: This was made with [Streamlit](https://streamlit.io/) connecting to [Snowflake](https://www.snowflake.com/) using [Weather Source's climatology dataset](https://app.snowflake.com/marketplace/listing/GZSOZ1LLD8/weather-source-llc-global-weather-climate-data-for-bi).")
st.markdown("**Note 3**: I like celsius.")
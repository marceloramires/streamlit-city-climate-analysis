# import altair as alt
# import numpy as np
# import pandas as pd
import streamlit as st

"""
# City weather analysis

test text

"""

num_points = st.slider("Temperature threshold (°C)", -100, 100, 18)

conn = st.experimental_connection('GLOBAL_WEATHER__CLIMATE_DATA_FOR_BI')
query = """
    SELECT 
        DOY_STD,
        (AVG_OF__DAILY_AVG_TEMPERATURE_FEELSLIKE_F - 32) * 5.0 / 9 AS AVG_TEMP_C,
        (AVG_OF__DAILY_MAX_TEMPERATURE_FEELSLIKE_F - 32) * 5.0 / 9 AS MAX_TEMP_C,
        (AVG_TEMP_C + MAX_TEMP_C) / 2 AS DAY_TEMP_C
    FROM STANDARD_TILE.CLIMATOLOGY_DAY 
    WHERE POSTAL_CODE = '98126' -- Seattle
"""
climatology_data = conn.query(query)
st.dataframe(climatology_data)
# -*- coding: utf-8 -*-
"""Contact Center ROI Calculator.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dVd4UsTiK6n41RmjE9gjG8nZ-StEhu2a
"""

import streamlit as st
from PIL import Image
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Conversation AI ROI Calculator', page_icon=":robot:")

# Company logo
logo = Image.open('company_logo.png')
st.image(logo, width=100)

st.title('Conversation AI ROI Calculator')

# Input current metrics
col1, col2 = st.columns(2)
current_aht = col1.number_input('Current AHT', min_value=0.0)
current_non_talk_time = col2.number_input('Current Non-Talk Time', min_value=0.0)
current_asa = col1.number_input('Current ASA', min_value=0.0)
current_wrap_up = col2.number_input('Current Wrap Up', min_value=0.0)

# Input simulated metrics  
col1, col2 = st.columns(2)
aht = col1.slider('AHT % Reduction', min_value=0.0, max_value=100.0, value=0.0, step=0.05)
non_talk_time = col2.slider('Non-Talk Time % Reduction', min_value=0.0, max_value=100.0, value=0.0, step=0.05)
asa = col1.slider('ASA % Reduction', min_value=0.0, max_value=100.0, value=0.0, step=0.05)
wrap_up = col2.slider('Wrap Up % Reduction', min_value=0.0, max_value=100.0, value=0.0, step=0.05)

# Input number of calls
calls_per_day = st.number_input('Number of Calls per Day', min_value=0, value=2500)  

# Calculations
aht_base = 450.0
non_talk_time_base = 90.0
asa_base = 31.0 
wrap_up_base = 31.0

aht_reduced = aht_base * (1 - aht/100)
non_talk_reduced = non_talk_time_base * (1 - non_talk_time/100)  
asa_reduced = asa_base * (1 - asa/100)
wrap_up_reduced = wrap_up_base * (1 - wrap_up/100)

call_duration_before = aht_base + non_talk_time_base
call_duration_after = aht_reduced + non_talk_reduced

total_reduction = (call_duration_before - call_duration_after) / call_duration_before * 100

# Total seconds
secs_per_call_before = call_duration_before
secs_per_call_after = call_duration_after

total_secs_before = calls_per_day * secs_per_call_before
total_secs_after = calls_per_day * secs_per_call_after  

st.write(f'Total Seconds Without Reduction: {total_secs_before}')
st.write(f'Total Seconds With Reduction: {total_secs_after}')

# Trend chart
start_month = st.date_input('Start month', value=pd.to_datetime('2023-01-01'))
end_month = st.date_input('End month', value=pd.to_datetime('2023-12-01'))  

months = pd.date_range(start_month, end_month, freq='MS').strftime("%b %Y").tolist()
improvements = [0] + [total_reduction/12]*(len(months)-2) + [total_reduction] 

df = pd.DataFrame({'Months': months, 'Improvements': improvements})

fig = px.line(df, x='Months', y='Improvements')
st.write(fig)  

# FTE savings
fte_before = total_secs_before / (60*60*8)
fte_after = total_secs_after / (60*60*8)
fte_savings = fte_before - fte_after

st.metric('FTE Savings', fte_savings)

# Cost savings
cost_per_call = 20  
cost_per_sec = cost_per_call / aht_base

secs_saved_per_call = call_duration_before - call_duration_after 
savings_per_call = secs_saved_per_call * cost_per_sec  

total_savings = savings_per_call * calls_per_day 
monthly_savings = total_savings * 30  

st.metric('Total Monthly Savings', monthly_savings)

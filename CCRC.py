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
logo = Image.open('humach.png')
st.image(logo, width=100)

st.title('Conversation AI ROI Calculator')

# Input current metrics
col1, col2 = st.columns(2)
current_aht = col1.number_input('Current AHT', min_value=0.0, format="%.0f")
current_non_talk_time = col2.number_input('Current Non-Talk Time', min_value=0.0, format="%.0f")
current_asa = col1.number_input('Current ASA', min_value=0.0, format="%.0f")
current_wrap_up = col2.number_input('Current Wrap Up', min_value=0.0, format="%.0f")

# Input simulated metrics  
col3, col4 = st.columns(2)
aht_slider = col3.slider('AHT % Reduction', min_value=0.0, max_value=100.0, step=0.05, format="%.2f")
aht = col3.number_input('AHT % Reduction', min_value=0.0, max_value=100.0, step=0.05, format="%.2f")
non_talk_slider = col4.slider('Non-Talk Time % Reduction', min_value=0.0, max_value=100.0, step=0.05, format="%.2f")
non_talk_time = col4.number_input('Non-Talk Time % Reduction', min_value=0.0, max_value=100.0, step=0.05, format="%.2f")

# Input simulated metrics  
col5, col6 = st.columns(2)
asa_slider = col5.slider('ASA % Reduction', min_value=0.0, max_value=100.0, step=0.05, format="%.2f")
asa = col5.number_input('ASA % Reduction', min_value=0.0, max_value=100.0, step=0.05, format="%.2f")
wrap_up_slider = col6.slider('Wrap Up % Reduction', min_value=0.0, max_value=100.0, step=0.05, format="%.2f")
wrap_up = col6.number_input('Wrap Up % Reduction', min_value=0.0, max_value=100.0, step=0.05, format="%.2f")

# Input number of calls
calls_per_day = st.number_input('Number of Calls per Day', min_value=0, format="%i")  

# Input cost related metrics
cost_per_call = st.number_input('Cost Per Call (Fully loaded)', min_value=0.0, format="%.2f")
cost_per_sec = cost_per_call / current_aht if current_aht != 0 else 0
total_cost = cost_per_call * calls_per_day
calls_per_day_input = st.number_input('Calls per Day', min_value=0, format="%i")

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
total_secs_before = calls_per_day * call_duration_before
total_secs_after = calls_per_day * call_duration_after  

# FTE savings
fte_before = total_secs_before / (60*60*8)
fte_after = total_secs_after / (60*60*8)
fte_savings = round(fte_before - fte_after)

st.metric('FTE Savings', fte_savings)

# Cost savings
secs_saved_per_call = call_duration_before - call_duration_after 
savings_per_call = secs_saved_per_call * cost_per_call  

total_savings = savings_per_call * calls_per_day 
monthly_savings = round(total_savings * 30, 2)  

st.metric('Total Monthly Savings ($)', f"${monthly_savings:.2f}")

# Total cost, cost per second, calls per day
st.write(f'Cost Per Second: ${cost_per_sec:.2f}')
st.write(f'Total Cost: ${total_cost:.2f}')
st.write(f'Calls per Day: {calls_per_day_input}')

# Total seconds without reduction and with reduction section with 0 decimal places
st.write(f'Total Seconds Without Reduction: {total_secs_before:.0f}')
st.write(f'Total Seconds With Reduction: {total_secs_after:.0f}')

# Improvement trend chart
start_month = st.date_input('Start month', value=pd.to_datetime('2023-01-01'))
end_month = st.date_input('End month', value=pd.to_datetime('2023-12-01'))  

months = pd.date_range(start_month, end_month, freq='MS').strftime("%b %Y").tolist()
improvements = [0] + [total_reduction/12]*(len(months)-2) + [total_reduction] 

df = pd.DataFrame({'Months': months, 'Improvements': improvements})

fig = px.line(df, x='Months', y='Improvements')
st.write(fig)  

# Show total improvement percentage
st.write(f'Total Improvement Percentage: {total_reduction:.2f}%')

# -*- coding: utf-8 -*-
"""Contact Center ROI Calculator.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dVd4UsTiK6n41RmjE9gjG8nZ-StEhu2a
"""

import streamlit as st
from PIL import Image

st.set_page_config(page_title='Conversation AI ROI Calculator', page_icon=":robot:")

# Company logo
logo = Image.open('Humach.png')
st.image(logo, width=100) 

st.title('Conversation AI ROI Calculator')

# Input current metrics
col1, col2 = st.columns(2)

current_aht = col1.number_input('Current AHT', min_value=0.0)
current_non_talk_time = col2.number_input('Current Non-Talk Time', min_value=0.0)  

current_asa = col1.number_input('Current ASA', min_value=0.0) 
current_wrap_up = col2.number_input('Current Wrap Up', min_value=0.0)

current_call_duration = current_aht + current_non_talk_time

# Input simulated metrics
col1, col2 = st.columns(2)

aht = col1.slider('AHT', min_value=0.0, max_value=100.0, value=0.0, step=0.05)
non_talk_time = col2.slider('Non-Talk Time', min_value=0.0, max_value=100.0, value=0.0, step=0.05)  

asa = col1.slider('ASA', min_value=0.0, max_value=100.0, value=0.0, step=0.05)
wrap_up = col2.slider('Wrap Up', min_value=0.0, max_value=100.0, value=0.0, step=0.05)

# Calculations 
aht_base = 450.0
non_talk_time_base = 90.0
asa_base = 31.0
wrap_up_base = 31.0
call_duration_base = aht_base + non_talk_time_base  

aht_reduced = aht_base * (1 - aht/100.0)
non_talk_time_reduced = non_talk_time_base * (1 - non_talk_time/100.0) 
asa_reduced = asa_base * (1 - asa/100.0)
wrap_up_reduced = wrap_up_base * (1 - wrap_up/100.0)
call_duration_reduced = aht_reduced + non_talk_time_reduced

# Show comparison
col1.write(f'Current AHT: {current_aht}')
col1.write(f'Simulated AHT: {aht_reduced}')  

col2.write(f'Current Non-Talk Time: {current_non_talk_time}') 
col2.write(f'Simulated Non-Talk Time: {non_talk_time_reduced}')

# FTE savings
daily_calls = 2770
secs_per_call_before = call_duration_base  
secs_per_call_after = call_duration_reduced
secs_per_day_before = daily_calls * secs_per_call_before
secs_per_day_after = daily_calls * secs_per_call_after   

fte_before = secs_per_day_before / (60.0 * 60.0 * 8.0)
fte_after = secs_per_day_after / (60.0 * 60.0 * 8.0)  
fte_savings = fte_before - fte_after

st.metric('FTE Savings', fte_savings)

# Cost savings
cost_per_call = 15.0
cost_per_second = cost_per_call / aht_base   

seconds_saved_per_call = call_duration_base - call_duration_reduced  
total_seconds_saved = seconds_saved_per_call * daily_calls

savings_per_call = seconds_saved_per_call * cost_per_second 
daily_savings = savings_per_call * daily_calls  
monthly_savings = daily_savings * 30.0

col1.metric('Total Seconds Saved', total_seconds_saved)
col2.metric('Savings per Call', savings_per_call) 

st.metric('Daily Savings', daily_savings)
st.metric('Monthly Savings', monthly_savings)

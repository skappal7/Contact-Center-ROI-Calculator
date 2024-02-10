# -*- coding: utf-8 -*-
"""Contact Center ROI Calculator.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dVd4UsTiK6n41RmjE9gjG8nZ-StEhu2a
"""

import streamlit as st
from PIL import Image

st.set_page_config(page_title='Conversational AI ROI Calculator', page_icon=":robot:")

# Company logo
logo = Image.open('Humach.png')  
st.image(logo, width=100)

st.title('Conversation AI ROI Calculator') 

# Input metrics
col1, col2 = st.columns(2)

aht = col1.slider('AHT', min_value=0, max_value=100, value=0, step=0.05)
non_talk_time = col2.slider('Non-Talk Time', min_value=0, max_value=100, value=0, step=0.05)

col1.write(f'AHT Reduction: {aht}%')  
col2.write(f'Non-Talk Time Reduction: {non_talk_time}%')

asa = col1.slider('ASA', min_value=0, max_value=100, value=0, step=0.05)
wrap_up = col2.slider('Wrap Up', min_value=0, max_value=100, value=0, step=0.05) 

col1.write(f'ASA Reduction: {asa}%')
col2.write(f'Wrap Up Reduction: {wrap_up}%')

# Calculations
aht_base = 450
non_talk_time_base = 90
asa_base = 31
wrap_up_base = 31 
call_duration_base = aht_base + non_talk_time_base

aht_reduced = aht_base * (1 - aht/100)  
non_talk_time_reduced = non_talk_time_base * (1 - non_talk_time/100) 
asa_reduced = asa_base * (1 - asa/100)
wrap_up_reduced = wrap_up_base * (1 - wrap_up/100)
call_duration_reduced = aht_reduced + non_talk_time_reduced  

total_reduction = 100 * (1 - call_duration_reduced/call_duration_base)

st.write(f'**Total Reduction:** {total_reduction:.2f}%')

# FTE savings
daily_calls = 2770  
secs_per_call_before = call_duration_base 
secs_per_call_after = call_duration_reduced
secs_per_day_before = daily_calls * secs_per_call_before 
secs_per_day_after = daily_calls * secs_per_call_after

fte_before = secs_per_day_before / (60 * 60 * 8)
fte_after = secs_per_day_after / (60 * 60 * 8) 
fte_savings = fte_before - fte_after

st.metric('FTE Savings', fte_savings)

# Cost savings 
cost_per_call = 15
cost_per_second = cost_per_call / aht_base 

seconds_saved_per_call = call_duration_base - call_duration_reduced
total_seconds_saved = seconds_saved_per_call * daily_calls  

savings_per_call = seconds_saved_per_call * cost_per_second
daily_savings = savings_per_call * daily_calls 
monthly_savings = daily_savings * 30  

col1.metric('Total Seconds Saved', total_seconds_saved)
col2.metric('Savings per Call', savings_per_call)

st.metric('Daily Savings', daily_savings)  
st.metric('Monthly Savings', monthly_savings)

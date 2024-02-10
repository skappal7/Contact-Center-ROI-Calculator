# -*- coding: utf-8 -*-
"""Contact Center ROI Calculator.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dVd4UsTiK6n41RmjE9gjG8nZ-StEhu2a
"""
import streamlit as st
from PIL import Image
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title='Conversation AI ROI Calculator', page_icon=":robot:")

# Company logo
logo = Image.open('Humach.png')
st.image(logo, width=100)

st.title('Conversation AI ROI Calculator')

# Sample list of months for demonstration
months = ['Jan 2023', 'Feb 2023', 'Mar 2023', 'Apr 2023', 'May 2023', 'Jun 2023', 'Jul 2023', 'Aug 2023', 'Sep 2023', 'Oct 2023', 'Nov 2023', 'Dec 2023']

# Input current metrics
col1, col2 = st.columns(2)
current_aht = col1.number_input('Current AHT', min_value=0.0, format="%.0f")
current_non_talk_time = col2.number_input('Current Non-Talk Time', min_value=0.0, format="%.0f")
current_asa = col1.number_input('Current ASA', min_value=0.0, format="%.0f")
current_wrap_up = col2.number_input('Current Wrap Up', min_value=0.0, format="%.0f")

# Input simulated metrics  
col3, col4 = st.columns(2)
aht_slider = col3.slider('AHT % Reduction', min_value=0.0, max_value=100.0, step=0.05, format="%.2f")
aht = col3.number_input('AHT % Reduction', min_value=0.0, max_value=100.0, step=0.05, value=aht_slider, format="%.2f")
non_talk_slider = col4.slider('Non-Talk Time % Reduction', min_value=0.0, max_value=100.0, step=0.05, format="%.2f")
non_talk_time = col4.number_input('Non-Talk Time % Reduction', min_value=0.0, max_value=100.0, step=0.05, value=non_talk_slider, format="%.2f")

# Input simulated metrics  
col5, col6 = st.columns(2)
asa_slider = col5.slider('ASA % Reduction', min_value=0.0, max_value=100.0, step=0.05, format="%.2f")
asa = col5.number_input('ASA % Reduction', min_value=0.0, max_value=100.0, step=0.05, value=asa_slider, format="%.2f")
wrap_up_slider = col6.slider('Wrap Up % Reduction', min_value=0.0, max_value=100.0, step=0.05, format="%.2f")
wrap_up = col6.number_input('Wrap Up % Reduction', min_value=0.0, max_value=100.0, step=0.05, value=wrap_up_slider, format="%.2f")

# Input number of calls
calls_per_day = st.number_input('Number of Calls per Day', min_value=0, format="%i")  

# Input cost related metrics
cost_per_call = st.number_input('Cost Per Call (Fully loaded)', min_value=0.0, format="%.2f")
cost_per_sec = cost_per_call / 450.0 if current_aht != 0 else 0
total_cost = cost_per_call * calls_per_day

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

# Total monthly savings
seconds_saved_per_call = call_duration_before - call_duration_after
savings_per_call = seconds_saved_per_call * cost_per_sec  
total_monthly_savings = savings_per_call * calls_per_day * 30

# Waterfall chart for savings
st.subheader("Monthly Savings Waterfall Chart")

# Monthly savings calculation for waterfall chart
savings_per_month = []
improvement_per_month = total_reduction / 100  # Normalize total improvement to 1
monthly_savings = savings_per_call * calls_per_day * 30
for i in range(len(months)):
    if i <= 2:
        # After ramp-up period, show 10% improvement each month
        savings = monthly_savings * 0.1 
    else:
        # After second quarter, show full improvement
        savings = monthly_savings * improvement_per_month
    savings_per_month.append(savings)

# Create cumulative savings
cumulative_savings = []
cum_sum = 0
for savings in savings_per_month:
    cum_sum += savings  
    cumulative_savings.append(cum_sum)

# Create waterfall chart data
waterfall_data = [
    go.Bar(x=months, y=savings_per_month, marker=dict(color='rgb(0, 128, 0)'), name='Monthly Savings', 
           text=[f"${s:,.0f}" for s in savings_per_month], textposition='inside'),
    go.Scatter(x=months, y=cumulative_savings, mode='lines+markers', marker=dict(color='rgb(255, 0, 0)'), 
               name='Cumulative Savings')
]

# Create waterfall chart layout
waterfall_layout = go.Layout(title="Monthly Savings Waterfall Chart",
                             xaxis_title="Month",
                             yaxis=dict(title="Savings ($)", overlaying='y', side='left'),
                             showlegend=True)

# Create figure
fig = go.Figure(data=waterfall_data, layout=waterfall_layout)

# Plot the waterfall chart
st.plotly_chart(fig)  

# Display FTE savings and total monthly savings at the top
col7, col8, col9 = st.columns(3)
with col7:
    st.markdown(
        f"""
        <div style="background-color:#0089BA;padding:10px;border-radius:10px;box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.1);">
        <span style="color:#002244;font-size:18px;"><b>FTE Savings</b></span><br>
        <span style="color:#ffffff;font-size:28px;"><b>{fte_savings}</b></span>
        </div>
        """,
        unsafe_allow_html=True
    )

with col8:
    st.markdown(
        f"""
        <div style="background-color:#0066b2;padding:10px;border-radius:10px;box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.1);">
        <span style="color:#002244;font-size:18px;"><b>Total Monthly Savings</b></span><br>
        <span style="color:#ffffff;font-size:28px;"><b>${total_monthly_savings:,.2f}</b></span>
        </div>
        """,
        unsafe_allow_html=True
    )

with col9:
    st.markdown(
        f"""
        <div style="background-color:#2E2E2E;padding:10px;border-radius:10px;box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.1);">
        <span style="color:#ffffff;font-size:18px;"><b>Total Improvement Percentage</b></span><br>
        <span style="color:#ffffff;font-size:28px;"><b>{round(total_reduction, 2)}%</b></span>
        </div>
        """,
        unsafe_allow_html=True
    )

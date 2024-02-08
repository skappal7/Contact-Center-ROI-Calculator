# -*- coding: utf-8 -*-
"""Contact Center ROI Calculator.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dVd4UsTiK6n41RmjE9gjG8nZ-StEhu2a
"""

import streamlit as st

# Function to calculate potential savings
def calculate_savings(avg_handle_time, non_talk_time, wrapup_time, speed_to_answer,
                      fcr_percent, sentiment_score, repeat_caller_percent, cost_per_call,
                      reduction_percents, num_calls_received):
    # Calculate the reductions
    reduced_avg_handle_time = avg_handle_time * (1 - reduction_percents['avg_handle_time'] / 100)
    reduced_non_talk_time = non_talk_time * (1 - reduction_percents['non_talk_time'] / 100)
    reduced_wrapup_time = wrapup_time * (1 - reduction_percents['wrapup_time'] / 100)
    reduced_speed_to_answer = speed_to_answer * (1 - reduction_percents['speed_to_answer'] / 100)
    reduced_fcr_percent = fcr_percent + (100 - fcr_percent) * (reduction_percents['fcr_percent'] / 100)
    reduced_sentiment_score = sentiment_score + (5 - sentiment_score) * (reduction_percents['sentiment_score'] / 100)
    reduced_repeat_caller_percent = repeat_caller_percent * (1 - reduction_percents['repeat_caller_percent'] / 100)
    
    # Calculate potential savings per call
    savings_per_call = (avg_handle_time - reduced_avg_handle_time +
                        non_talk_time - reduced_non_talk_time +
                        wrapup_time - reduced_wrapup_time +
                        speed_to_answer - reduced_speed_to_answer) * cost_per_call
    
    # Calculate total potential savings
    total_savings = savings_per_call * num_calls_received
    
    # Calculate percentage savings compared to original values
    avg_handle_time_savings = (avg_handle_time - reduced_avg_handle_time) / avg_handle_time * 100
    non_talk_time_savings = (non_talk_time - reduced_non_talk_time) / non_talk_time * 100
    wrapup_time_savings = (wrapup_time - reduced_wrapup_time) / wrapup_time * 100
    speed_to_answer_savings = (speed_to_answer - reduced_speed_to_answer) / speed_to_answer * 100
    fcr_percent_savings = (fcr_percent - reduced_fcr_percent) / fcr_percent * 100
    sentiment_score_savings = (5 - reduced_sentiment_score) / (5 - sentiment_score) * 100
    repeat_caller_percent_savings = (repeat_caller_percent - reduced_repeat_caller_percent) / repeat_caller_percent * 100
    
    return total_savings, {
        'Average Handle Time (seconds)': reduced_avg_handle_time,
        'Non-Talk Time (seconds)': reduced_non_talk_time,
        'Wrap-up Time (seconds)': reduced_wrapup_time,
        'Speed to Answer (seconds)': reduced_speed_to_answer,
        'First Call Resolution (%)': reduced_fcr_percent,
        'Sentiment Score (1-5)': reduced_sentiment_score,
        'Repeat Caller Rate (%)': reduced_repeat_caller_percent
    }, total_savings

# Streamlit UI
st.title('Contact Center Savings Calculator')

# Input variables
original_cost = st.number_input('Original Cost of Metric Performance ($)', value=10000)
avg_handle_time = st.number_input('Average Handle Time (seconds)', value=300)
non_talk_time = st.number_input('Non-Talk Time (seconds)', value=60)
wrapup_time = st.number_input('Wrap-up Time (seconds)', value=30)
speed_to_answer = st.number_input('Speed to Answer (seconds)', value=20)
fcr_percent = st.number_input('First Call Resolution (%)', value=80)
sentiment_score = st.number_input('Sentiment Score (1-5)', min_value=1, max_value=5, value=4)
repeat_caller_percent = st.number_input('Repeat Caller Rate (%)', value=10)
cost_per_call = st.number_input('Cost of Call ($)', value=5)
num_calls_received = st.number_input('Number of Calls Received', value=100)

# Percentage reduction sliders for each variable in a separate panel
with st.sidebar:
    st.title('Percentage Reduction')
    reduction_percents = {
        'avg_handle_time': st.slider('Avg Handle Time Reduction (%)', 1, 100, 10, 1),
        'non_talk_time': st.slider('Non-Talk Time Reduction (%)', 1, 100, 10, 1),
        'wrapup_time': st.slider('Wrap-up Time Reduction (%)', 1, 100, 10, 1),
        'speed_to_answer': st.slider('Speed to Answer Reduction (%)', 1, 100, 10, 1),
        'fcr_percent': st.slider('FCR Improvement (%)', 1, 100, 10, 1),
        'sentiment_score': st.slider('Sentiment Score Improvement (%)', 1, 100, 10, 1),
        'repeat_caller_percent': st.slider('Repeat Caller Rate Reduction (%)', 1, 100, 10, 1)
    }

# Calculate total potential savings, new values, and ROI
total_savings, new_values, roi = calculate_savings(avg_handle_time, non_talk_time, wrapup_time,
                                                   speed_to_answer, fcr_percent, sentiment_score,
                                                   repeat_caller_percent, cost_per_call,
                                                   reduction_percents, num_calls_received)

# Display total potential savings and ROI
st.subheader('Total Potential Savings and ROI')
st.write(f'Original Cost of Metric Performance: **${original_cost:.2f}**')
st.write(f'ROI Achieved based on New Values: **${roi:.2f}**')

# Display new values based on selection
st.subheader('New Values based on Selection')
new_values_display = {key: f'{value:.1f}' for key, value in new_values.items()}
st.table(new_values_display)

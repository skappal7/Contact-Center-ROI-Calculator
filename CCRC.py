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
    
    return total_savings

# Streamlit UI
st.title('Contact Center Savings Calculator')

# Input variables with default values
default_avg_handle_time = 300
default_non_talk_time = 60
default_wrapup_time = 30
default_speed_to_answer = 20
default_fcr_percent = 80
default_sentiment_score = 4
default_repeat_caller_percent = 10
default_cost_per_call = 5
default_num_calls_received = 100

avg_handle_time = st.number_input('Average Handle Time (seconds)', value=default_avg_handle_time)
non_talk_time = st.number_input('Non-Talk Time (seconds)', value=default_non_talk_time)
wrapup_time = st.number_input('Wrap-up Time (seconds)', value=default_wrapup_time)
speed_to_answer = st.number_input('Speed to Answer (seconds)', value=default_speed_to_answer)
fcr_percent = st.number_input('First Call Resolution (%)', value=default_fcr_percent)
sentiment_score = st.number_input('Sentiment Score (1-5)', min_value=1, max_value=5, value=default_sentiment_score)
repeat_caller_percent = st.number_input('Repeat Caller Rate (%)', value=default_repeat_caller_percent)
cost_per_call = st.number_input('Cost of Call ($)', value=default_cost_per_call)
num_calls_received = st.number_input('Number of Calls Received', value=default_num_calls_received)

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

# Display reduced values in input sections
st.subheader('Reduced Values:')
st.write(f'Reduced Average Handle Time: {avg_handle_time - (avg_handle_time * reduction_percents["avg_handle_time"] / 100):.2f} seconds')
st.write(f'Reduced Non-Talk Time: {non_talk_time - (non_talk_time * reduction_percents["non_talk_time"] / 100):.2f} seconds')
st.write(f'Reduced Wrap-up Time: {wrapup_time - (wrapup_time * reduction_percents["wrapup_time"] / 100):.2f} seconds')
st.write(f'Reduced Speed to Answer: {speed_to_answer - (speed_to_answer * reduction_percents["speed_to_answer"] / 100):.2f} seconds')
st.write(f'Reduced FCR Percentage: {fcr_percent + (100 - fcr_percent) * (reduction_percents["fcr_percent"] / 100):.2f}%')
st.write(f'Reduced Sentiment Score: {sentiment_score + (5 - sentiment_score) * (reduction_percents["sentiment_score"] / 100):.2f}')
st.write(f'Reduced Repeat Caller Rate: {repeat_caller_percent - (repeat_caller_percent * reduction_percents["repeat_caller_percent"] / 100):.2f}%')

# Reset button to reset all input values
if st.button('Reset'):
    avg_handle_time = default_avg_handle_time
    non_talk_time = default_non_talk_time
    wrapup_time = default_wrapup_time
    speed_to_answer = default_speed_to_answer
    fcr_percent = default_fcr_percent
    sentiment_score = default_sentiment_score
    repeat_caller_percent = default_repeat_caller_percent
    cost_per_call = default_cost_per_call
    num_calls_received = default_num_calls_received

# Calculate total potential savings
total_savings = calculate_savings(avg_handle_time, non_talk_time, wrapup_time,
                                  speed_to_answer, fcr_percent, sentiment_score,
                                  repeat_caller_percent, cost_per_call,
                                  reduction_percents, num_calls_received)

# Display total potential savings
st.write(f'Total Potential Savings: ${total_savings:.2f}')

"""
idea for second page a calorie tracker, where user inputs there meal
"""
"""
My first app in streamlit, a fitness tracker where 
the user in the main page can input there exercises.
(on the future second page user will input meals with its calories and macros)
And use an LLM to recommend the users a workout plan based on there input
"""

import streamlit as st
import pandas as pd
import numpy as np
import datetime

#list of workouts in the session
if "workout_list" not in st.session_state:
    st.session_state.workout_list = []
number_of_workouts = st.session_state.workout_list

def save_workouts(workout):
    return None


st.title('Gym Tracker')
st.write("Welcome to your gym tracker app")


#Date needed to log the workout
current_date = datetime.date.today()
today_abbreviation = current_date.strftime("%b-%d-%Y")

#User input that gets saved in a dictionary
st.sidebar.title("Log your workout")
st.sidebar.write("Date: ", today_abbreviation)
exercise_name = st.sidebar.text_input("Exercise")
weight_type = st.sidebar.radio("Measuring weight preference", ["kg", "lb"])
number_of_reps = st.sidebar.slider("Repetitions done", 1)
number_of_sets = st.sidebar.slider("Number of sets", 1)
duration = st.sidebar.number_input("Duration of workout in minutes", 1)
if weight_type == 'kg':
    weight_lifted = st.sidebar.number_input("Weight in kilograms", 1)
elif weight_type == 'lb':
    weight_lifted = st.sidebar.number_input("Weight in pounds", 1)
submit = st.sidebar.button("Submit exercise")


workout = {"Date": today_abbreviation, "Exercise": exercise_name, "Reps": number_of_reps, 
           "Sets": number_of_sets, "Weight": weight_lifted, "Duration": duration}

#When submit button is pressed user input is submitted
if submit:
    number_of_workouts.append(workout)
    

workout_df = pd.DataFrame(data=number_of_workouts)
st.table(workout_df)
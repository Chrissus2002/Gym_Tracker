import streamlit as st
import pandas as pd
import datetime
import api_snowflake as api
import openai_api as ai_api


st.set_page_config(page_title="Fitness Tracker", layout="centered")

#puts the user info to save it in the session state
if "user_form" not in st.session_state:
    st.session_state.user_form = {}
user = st.session_state.user_form

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content":"Hello, how can i help with your workouts?"}]

with st.sidebar:  
    with st.form("user_info"):
        user_weight = st.number_input("Enter your current weight in kg:", 1, value=50)
        user_height = st.number_input("Enter your current height in meters:", 1.0)
        if st.form_submit_button("Submit"):
            user["weight"] = user_weight
            user["height"] = user_height


st.title('Gym Tracker')
st.write("Welcome to your gym tracker app")

#Date needed to log the workout
current_date = datetime.date.today()
today_abbreviation = current_date.strftime("%b-%d-%Y")
#User input diplayed on the sidebar
st.title("Log your workout")
st.write("Date: ", today_abbreviation)
st.divider()
col1, col2 = st.columns(2)
with col1:
    exercise_name = st.text_input("Exercise")
    number_of_reps = st.slider("Repetitions done", 1)
    number_of_sets = st.slider("Number of sets", 1)
with col2:
    weight_lifted = st.number_input("Weight in kilograms", 1.0, step=0.5)
    duration = st.number_input("Duration of workout in minutes", 1)
    submit = st.button("Submit exercise")


#When submit button is pressed user input is submitted
if submit:
    if not exercise_name:
         st.error("Please write an exercise name")
    else:
        workout = {"Date": today_abbreviation, "Exercise_name": exercise_name, "Number_of_reps": number_of_reps, 
           "Number_of_sets": number_of_sets, "Weight_lifted": weight_lifted, "Duration": duration}
        df = pd.Dataframe(api.insert_exercise(workout))


if st.button("Display"):
    display_df = api.retrieve_data_df()
    st.dataframe(display_df)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is a good workout?"):
    st.session_state.messages.append({"role": "user", "content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        stream = ai_api.get_chagpt_response(prompt)
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content":response})
import snowflake.snowpark.session
import streamlit as st
import pandas as pd
import os
import datetime
import snowflake.connector
import snowflake.snowpark

st.set_page_config("Fitness Tracker")

#list of workouts in the session
if "workout_list" not in st.session_state:
    st.session_state.workout_list = []
number_of_workouts = st.session_state.workout_list

def create_connection_snowflake(account, user, password):
    try:
        conn = snowflake.connector.connect(
            account=account,
            user=user,
            password=password,
            )
        st.write("Connection succesful")
    except Exception as e:
        st.error(f"Connection problem: {e}")
    return conn


st.title('Gym Tracker')
st.write("Welcome to your gym tracker app")


st.header("Snowflake credentials")
col1, col2 = st.columns(2)
with col1:
    account_sf = st.text_input("Account: ")
    user_sf = st.text_input("User: ")
    password_sf = st.text_input("Password: ", type="password")
    #role_sf = st.text_input("Role:", )
#with col2:
 #   warehouse_sf = st.text_input("Warehouse: ")
  #  database_sf = st.text_input("Database: ")
   # schema_sf = st.text_input("Schema:")
    connect = st.button("Connect")
    if connect:
        connenction = create_connection_snowflake(account=account_sf,user=user_sf,password=password_sf)
        


#Date needed to log the workout
current_date = datetime.date.today()
today_abbreviation = current_date.strftime("%b-%d-%Y")
#User input diplayed on the sidebar
with st.sidebar:
    st.title("Log your workout")
    st.write("Date: ", today_abbreviation)
    exercise_name = st.text_input("Exercise")
    weight_type = st.radio("Measuring weight preference", ["kg", "lb"])
    number_of_reps = st.slider("Repetitions done", 1)
    number_of_sets = st.slider("Number of sets", 1)
    duration = st.number_input("Duration of workout in minutes", 1)
    if weight_type == 'kg':
        weight_lifted = st.number_input("Weight in kilograms", 1)
    elif weight_type == 'lb':
        weight_lifted = st .number_input("Weight in pounds", 1)
    submit = st.button("Submit exercise")

#When submit button is pressed user input is submitted
if submit:
    workout = {"Date": today_abbreviation, "Exercise": exercise_name, "Reps": number_of_reps, 
           "Sets": number_of_sets, "Weight": weight_lifted, "Duration": duration}
    number_of_workouts.append(workout)
    

workout_df = pd.DataFrame(data=number_of_workouts)
if not workout_df.empty:
    st.table(workout_df)
import streamlit as st
import snowflake.connector


def _init_connection():
    st.toast("connection established")
    return snowflake.connector.connect(**st.secrets["connection"])


def insert_exercise(workout_dict):
    conn = _init_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exercises (
        id INTEGER PRIMARY KEY autoincrement,
        date TEXT,
        exercise_name TEXT,
        number_of_reps INTEGER,
        number_of_sets INTEGER,
        duration INTEGER,
        weight_lifted FLOAT
    )
    ''')
    cursor.execute('''INSERT INTO exercises(date, exercise_name, number_of_reps, number_of_sets, duration, weight_lifted) 
                   VALUES('{0}','{1}',{2},{3},{4},{5})'''.format(workout_dict["Date"], workout_dict["Exercise_name"], workout_dict["Number_of_reps"], 
                                           workout_dict["Number_of_sets"], workout_dict["Weight_lifted"], workout_dict["Duration"]))
    conn.commit()
    conn.close()

@st.cache_data
def retrieve_data_df():
    conn = _init_connection()
    cur = conn.cursor()
    sql = "SELECT date,exercise_name, number_of_reps, number_of_sets, duration, weight_lifted FROM exercises"
    cur.execute(sql)
    df = cur.fetch_pandas_all()
    return df

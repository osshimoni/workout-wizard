'''
Workout Application
'''

import streamlit as st
from datetime import datetime
from datetime import date
import pandas as pd

today = date.today()

def end_workout(start_time, end_time):
    duration = end_time.replace(microsecond=0) - start_time.replace(microsecond=0)
    st.sidebar.title(f'Workout duration: {duration}')
    if st.sidebar.button('Log workout'):
        st.sidebar.write('Workout Saved')


def push(location):
    st.subheader("Push Workout")
    df = pd.read_csv('push_ymca.csv')

    if location == 'YMCA':
        st.table(df)

def main():
    st.sidebar.title("Workout Wizard")
    status = st.sidebar.selectbox("Start or Finish Workout:", ("","In Progress", "End"))
    if status == "In Progress":

        with open(f"{today}_start", 'w') as start_time:
            start_time.write(f'{datetime.now()}')

        location = st.sidebar.selectbox("Select a location:", ("YMCA", "Office"))
        day = st.sidebar.selectbox("What day is it?", ("", "Push", "Pull", "Shoulders", "Legs", "Core"))

        if day == "Push":
            push(location)

    elif status == "End":
        end_time = datetime.now()
        with open(f"{today}_start") as f:
            start_time = datetime.fromisoformat(f.read())
        end_workout(start_time, end_time)


main()

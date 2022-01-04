'''
Workout Application
'''

import streamlit as st
from datetime import datetime
from datetime import date
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('workout-wizard-337222-f628ea871ec6.json', scope)
# authorize the clientsheet
client = gspread.authorize(creds)

today = date.today()

def end_workout(start_time, end_time):
    duration = end_time.replace(microsecond=0) - start_time.replace(microsecond=0)
    st.sidebar.title(f'Workout duration: {duration}')
    if st.sidebar.button('Log workout'):
        st.sidebar.write('Workout Saved')


def push(location):
    st.subheader("Push Workout")



    if location == 'YMCA':
        # get the instance of the Spreadsheet
        sheet = client.open('push_ymca')

        # get the first sheet of the Spreadsheet
        sheet_instance = sheet.get_worksheet(0)

        df = pd.DataFrame.from_dict(sheet_instance.get_all_records())
        st.write(df)


def main():
    st.sidebar.title("Workout Wizard")
    status = st.sidebar.selectbox("Start or Finish Workout:", ("","In Progress", "End"))
    if status == "In Progress":

        with open(f"times/{today}_start", 'w') as start_time:
            start_time.write(f'{datetime.now()}')

        location = st.sidebar.selectbox("Select a location:", ("YMCA", "Office"))
        day = st.sidebar.selectbox("What day is it?", ("", "Push", "Pull", "Shoulders", "Legs", "Core"))

        if day == "Push":
            push(location)

    elif status == "End":
        end_time = datetime.now()
        with open(f"times/{today}_start") as f:
            start_time = datetime.fromisoformat(f.read())
        end_workout(start_time, end_time)


main()

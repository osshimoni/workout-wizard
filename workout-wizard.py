'''
Workout Application
Author: Osher Shimoni
January 4th, 2022
Personalized workout wizard
'''

import streamlit as st
from datetime import datetime
from datetime import date
import pandas as pd
import gspread as gspread
from oauth2client.service_account import ServiceAccountCredentials
import gspread_dataframe as gs

gc = gspread.service_account(filename="workout-wizard-337222-f628ea871ec6.json")

today = date.today()

def new_data(df):
    movement_list = df['Movement'].tolist()
    movement_list.append("New Movement")
    movement_list.insert(0,'')

    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

    with col1:
        movement = st.selectbox('Select a Movement:',options = list(movement_list))
    with col2:
        weight = st.text_input("Enter Weight:")
    with col3:
        reps = st.text_input("Enter Reps:")
    with col4:
        sets = st.text_input("Enter Sets:")

    save_col, notify_col = st.columns([.1,.1])

    with save_col:
        if st.button('Save'):
            movement_condition = (df.Movement == movement)
            df.loc[movement_condition, 'Weight'] = weight
            df.loc[movement_condition, 'Reps'] = reps
            df.loc[movement_condition, 'Sets'] = sets
            with notify_col:
                st.write('Movement Saved')
    return df
    # if st.button('New Movement'):
    #     df = new_movement(df)
    #     st.write(df)

# def new_movement(df):
#     col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
#
#     with col1:
#         new_movement_name = st.text_input('Movement Name:')
#     with col2:
#         new_movement_weight = st.text_input("Weight:")
#     with col3:
#         new_movement_reps = st.text_input("Reps:")
#     with col4:
#         new_movement_sets = st.text_input("Sets:")
#
#     new_movement_df = {'Movement': new_movement_name, 'Weight': new_movement_weight, 'Reps': new_movement_reps, 'Sets': new_movement_sets}
#     df.append(new_movement_df, ignore_index=True)
#     return(df)

def get_data(sheet):

    ws = gc.open(sheet).worksheet('data')
    df = pd.DataFrame.from_dict(ws.get_all_records())
    return df

def get_ws(sheet):
    ws = gc.open(sheet).worksheet('data')
    return ws

def workout(sheet):

    st.subheader(f'{sheet.capitalize()} Workout')

    df = get_data(sheet)

    col1, col2 = st.columns([10, 1])
    with col1:
        st.table(get_data(sheet))
    with col2:
        if st.button('Refresh'):
            get_data(sheet)

    new_data(df)

    ws = get_ws(sheet)
    gs.set_with_dataframe(worksheet=ws, dataframe=df, include_index=False, include_column_header=True,
                          resize=True)

def main():
    st.sidebar.title("Workout Wizard")
    status = st.sidebar.selectbox("Start or Finish Workout:", ("","In Progress", "End"))
    if status == "In Progress":

        with open(f"{today}_start", 'w') as start_time:
            start_time.write(f'{datetime.now()}')

        day = st.sidebar.selectbox("What day is it?", ('', "Push", "Pull", "Shoulders", "Legs", "Core"))
        sheet = ''
        if day == "Push":
            sheet = 'push'
            workout(sheet)
        elif day == 'Pull':
            sheet = 'pull'
            workout(sheet)
        elif day == 'Shoulders':
            sheet = 'shoulders'
            workout(sheet)
        elif day == 'Legs':
            sheet = 'legs'
            workout(sheet)
        elif day == 'Core':
            sheet = 'core'
            workout(sheet)

    elif status == "End":
        end_time = datetime.now()
        with open(f"times/{today}_start") as f:
            start_time = datetime.fromisoformat(f.read())
        duration = end_time.replace(microsecond=0) - start_time.replace(microsecond=0)
        st.sidebar.title(f'Workout duration: {duration}')

    elif status == '':
        st.header('Use the menu to begin workout')


main()

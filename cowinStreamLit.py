import streamlit as st
from datetime import date
from cowin_api import CoWinAPI
import requests
import pandas as pd
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

st.title("CoWin Tracker")
age_option = st.sidebar.selectbox(
    "Which age category do you want to Query?", ("18", "45")
)

cowin = CoWinAPI()
stateList=[]
distList=[]
dist_code=1
for state in cowin.get_states()["states"]:
    stateList.append(state['state_name'])
state_selector = st.sidebar.selectbox("State Selector",stateList)
for state in cowin.get_states()["states"]:
    if(state['state_name'] == state_selector):
        state_code=state['state_id']

for dist in cowin.get_districts(state_code)['districts']:
    distList.append(dist['district_name'])
dist_selector = st.sidebar.selectbox("District Selector",distList)
for dist in cowin.get_districts(state_code)['districts']:
    print(dist)
    if(dist['district_name'] == dist_selector):
        dist_code=dist['district_id']
        


format = 'MMM DD, YYYY'
start_date = st.sidebar.date_input("Vaccination Date", date.today()).strftime("%d/%m/%y")

print(f'print dist sel:: {dist_selector}, {start_date}, {age_option}')
if st.sidebar.button("Get Slots"):
    URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(dist_code, start_date)
    print (URL)
    result = requests.get(URL, headers=header)
    print (result.json()["centers"])
    
    
    st.table(result.json()["centers"])





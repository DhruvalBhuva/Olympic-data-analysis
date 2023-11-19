import streamlit as st
import pandas as pd
from appComponents import preprocessing, helper


df = pd.read_csv('./Dataset/athlete_events.csv')
region_df = pd.read_csv('./Dataset/noc_regions.csv')

df = preprocessing.preprocess(df, region_df)


user_menu = st.sidebar.radio(
    "Select an option",
    ("Medal tally", "Overall Analysis",
     "Country-wise Analysis", "Athlete-wise Analysis")
)

# st.dataframe(df)

if user_menu == "Medal tally":
    st.title("Medal Tally")
    st.table(helper.medal_telly(df))

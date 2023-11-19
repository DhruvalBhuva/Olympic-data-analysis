import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from appComponents import preprocessing, helper


df = pd.read_csv('./Dataset/athlete_events.csv')
region_df = pd.read_csv('./Dataset/noc_regions.csv')

df = preprocessing.preprocess(df, region_df)

st.sidebar.title("Olympics Analysis")

user_menu = st.sidebar.radio(
    "Select an option",
    ("Medal tally", "Overall Analysis",
     "Country-wise Analysis", "Athlete-wise Analysis")
)


if user_menu == "Medal tally":
    st.sidebar.header("Medal Tally")

    years, country = helper.county_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_telly = helper.fetch_medal_tally(df, selected_year, selected_country)

    if selected_year == "Overall" and selected_country == "Overall":
        st.title("Overall Tally")
    if selected_year != "Overall" and selected_country == "Overall":
        st.title("Tally for " + str(selected_year) + " Olympics")
    if selected_year == "Overall" and selected_country != "Overall":
        st.title(selected_country + " overall performance")
    if selected_year != "Overall" and selected_country != "Overall":
        st.title(selected_country + " performance in " + str(selected_year))

    st.table(medal_telly)

if user_menu == "Overall Analysis":

    editions = len(df['Year'].unique())
    cities = len(df['City'].unique())
    sports = len(df['Sport'].unique())
    events = len(df['Event'].unique())
    athletes = len(df['Name'].unique())
    nations = len(df['region'].unique())

    st.title("Top Statistics")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)

    with col2:
        st.header("Hosts")
        st.title(cities)

    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)

    with col2:
        st.header("Nations")
        st.title(nations)

    with col3:
        st.header("Athletes")
        st.title(athletes)

    # Total number of countries participating each year
    nations_overTime = helper.data_over_time(df, "region")
    country_fig = px.line(nations_overTime, x="Year", y="count")
    country_fig.update_layout(title="Nations Over Time", xaxis_title="Year",
                              yaxis_title="Number of Nations")
    st.plotly_chart(country_fig)

    # Total number of events over time
    events_overTime = helper.data_over_time(df, "Event")
    events_fig = px.line(events_overTime, x="Year", y="count")
    events_fig.update_layout(title="Events Over Time", xaxis_title="Year",
                             yaxis_title="Number of Events")
    st.plotly_chart(events_fig)

    # Athletes participation over time
    athletes_overTime = helper.data_over_time(df, "Name")
    athletes_fig = px.line(athletes_overTime, x="Year", y="count")
    athletes_fig.update_layout(title="Athletes Over Time", xaxis_title="Year",
                               yaxis_title="Number of Athletes")
    st.plotly_chart(athletes_fig)

    st.title("No. of Events over time(Every Sport)")
    fig, ax = plt.subplots(figsize=(30, 30))
    heatMap_df = df.drop_duplicates(subset=['Year', 'Sport', 'Event'])
    ax = sns.heatmap(heatMap_df.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(
        int), annot=True, cmap='YlGnBu')
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list = df["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "Overall")

    selected_sport = st.selectbox("Select a Sport", sport_list)

    athlete_df = helper.most_successfull_athelete(df, selected_sport)
    st.table(athlete_df)

if user_menu == "Country-wise Analysis":
    st.sidebar.title("Country-wise Analysis")

    all_country_list = df["region"].dropna().unique().tolist()
    all_country_list.sort()

    selected_country = st.sidebar.selectbox(
        "Select a Country", all_country_list)

    yearwise_medal_tally_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(yearwise_medal_tally_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally Over the Years")
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports")
    pivot_table = helper.country_yearwise_medal_tally_overyear(
        df, selected_country)

    fig, ax = plt.subplots(figsize=(25, 25))
    ax = sns.heatmap(pivot_table, annot=True)
    st.pyplot(fig)

    st.title("Top 10 Athletes of " + selected_country)
    top10_atheletes = helper.most_successfull_athelete_countrywise(
        df, selected_country)
    st.table(top10_atheletes)

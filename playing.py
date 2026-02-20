import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Football Stats Analyzer", layout="wide")

st.title(" Football Stats Analyzer Dashboard")


# LOAD DATA

@st.cache_data
def load_data():
    attacking = pd.read_csv("attacking_data.csv")
    defending = pd.read_csv("defending_data.csv")
    goalkeeping = pd.read_csv("goalkeeping_data.csv")
    goals = pd.read_csv("goals_data.csv")
    disciplinary = pd.read_csv("disciplinary_data.csv")
    players = pd.read_csv("players_data.csv")
    teams = pd.read_csv("teams_data.csv")
    return attacking, defending, goalkeeping, goals, disciplinary, players, teams

attacking, defending, goalkeeping, goals, disciplinary, players, teams = load_data()


# SIDEBAR

st.sidebar.header("Navigation")
page = st.sidebar.selectbox(
    "Choose Section",
    [
        "Home",
        "Top Scorers",
        "Playmakers",
        "Defenders",
        "Goalkeepers",
        "Discipline",
        "Team Comparison",
    ],
)


# HOME

if page == "Home":
    st.subheader("Tournament Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Teams", teams.shape[0])
    col2.metric("Total Players", players.shape[0])
    col3.metric("Total Goals", goals["goals"].sum())

# TOP SCORERS

elif page == "Top Scorers":
    st.subheader("Top 10 Goal Scorers")

    top_scorers = goals.sort_values("goals", ascending=False).head(10)

    fig = px.bar(
        top_scorers,
        x="player_name",
        y="goals",
        color="goals",
        title="Top 10 Scorers",
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(top_scorers)


# PLAYMAKERS

elif page == "Playmakers":
    st.subheader("Top 10 Assist Providers")

    top_assist = attacking.sort_values("assists", ascending=False).head(10)

    fig = px.bar(
        top_assist,
        x="player_name",
        y="assists",
        color="assists",
        title="Top Assist Providers",
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(top_assist)


# DEFENDERS

elif page == "Defenders":
    st.subheader("Top Defensive Players (Tackles)")

    top_def = defending.sort_values("tackles", ascending=False).head(10)

    fig = px.bar(
        top_def,
        x="player_name",
        y="tackles",
        color="tackles",
        title="Top Tacklers",
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(top_def)


# GOALKEEPERS

elif page == "Goalkeepers":
    st.subheader("Top Goalkeepers (Saves)")

    top_gk = goalkeeping.sort_values("saves", ascending=False).head(10)

    fig = px.bar(
        top_gk,
        x="player_name",
        y="saves",
        color="saves",
        title="Top Goalkeepers",
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(top_gk)


# DISCIPLINE

elif page == "Discipline":
    st.subheader("Most Booked Players")

    disciplinary["total_cards"] = (
        disciplinary["yellow_cards"] + disciplinary["red_cards"]
    )

    top_cards = disciplinary.sort_values("total_cards", ascending=False).head(10)

    fig = px.bar(
        top_cards,
        x="player_name",
        y="total_cards",
        color="total_cards",
        title="Most Cards",
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(top_cards)


# TEAM COMPARISON

elif page == "Team Comparison":
    st.subheader("Compare Two Teams")

    team_list = teams["team_name"].unique()

    team1 = st.selectbox("Select Team 1", team_list)
    team2 = st.selectbox("Select Team 2", team_list)

    team1_stats = teams[teams["team_name"] == team1]
    team2_stats = teams[teams["team_name"] == team2]

    comparison = pd.concat([team1_stats, team2_stats])

    st.dataframe(comparison)

    numeric_cols = comparison.select_dtypes(include="number").columns

    fig = px.bar(
        comparison,
        x="team_name",
        y=numeric_cols,
        barmode="group",
        title="Team Comparison",
    )


    st.plotly_chart(fig, use_container_width=True)

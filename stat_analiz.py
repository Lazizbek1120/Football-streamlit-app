import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Football Stats Analyzer", layout="wide")
st.title("Football Stats Analyzer Dashboard")


# =========================
# COLUMN CLEANER
# =========================
def clean_columns(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
        .str.replace("%", "", regex=False)
    )
    return df


# =========================
# NUMERIC CONVERTER
# =========================
def convert_numeric(df):
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="ignore")
    return df


# =========================
# PLAYER MERGE
# =========================
def merge_players(df, players):
    if "id_player" in df.columns and "id_player" in players.columns:
        df = df.merge(players, on="id_player", how="left")
    return df


# =========================
# TEAM MERGE (AUTO NAME FIX)
# =========================
def merge_teams(df, teams):
    if "team" in df.columns and "team" in teams.columns:
        df = df.merge(teams, on="team", how="left")

        # Team nomi bo‘lishi mumkin bo‘lgan ustunlar
        possible_cols = ["team", "team_name", "name", "club", "club_name"]

        for col in possible_cols:
            if col in df.columns:
                df["team_display"] = df[col]
                break

    return df


# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():

    attacking = clean_columns(pd.read_csv("attacking_data.csv"))
    defending = clean_columns(pd.read_csv("defending_data.csv"))
    goalkeeping = clean_columns(pd.read_csv("goalkeeping_data.csv"))
    goals = clean_columns(pd.read_csv("goals_data.csv"))
    disciplinary = clean_columns(pd.read_csv("disciplinary_data.csv"))
    players = clean_columns(pd.read_csv("players_data.csv"))
    teams = clean_columns(pd.read_csv("teams_data.csv"))

    attacking = convert_numeric(attacking)
    defending = convert_numeric(defending)
    goalkeeping = convert_numeric(goalkeeping)
    goals = convert_numeric(goals)
    disciplinary = convert_numeric(disciplinary)
    players = convert_numeric(players)
    teams = convert_numeric(teams)

    # PLAYER MERGE
    attacking = merge_players(attacking, players)
    defending = merge_players(defending, players)
    goalkeeping = merge_players(goalkeeping, players)
    goals = merge_players(goals, players)
    disciplinary = merge_players(disciplinary, players)

    # TEAM MERGE
    attacking = merge_teams(attacking, teams)
    defending = merge_teams(defending, teams)
    goalkeeping = merge_teams(goalkeeping, teams)
    goals = merge_teams(goals, teams)
    disciplinary = merge_teams(disciplinary, teams)

    return attacking, defending, goalkeeping, goals, disciplinary, players, teams


attacking, defending, goalkeeping, goals, disciplinary, players, teams = load_data()


# =========================
# SIDEBAR
# =========================
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Select Section",
    [
        "Home",
        "Top Scorers",
        "Playmakers",
        "Defenders",
        "Goalkeepers",
        "Discipline",
    ],
)


# =========================
# HOME
# =========================
if page == "Home":

    col1, col2, col3 = st.columns(3)

    total_goals = goals["goals"].sum() if "goals" in goals.columns else 0

    col1.metric("Total Teams", len(teams))
    col2.metric("Total Players", len(players))
    col3.metric("Total Goals", int(total_goals))


# =========================
# TOP SCORERS
# =========================
elif page == "Top Scorers":

    if "goals" in goals.columns:

        top = goals.sort_values("goals", ascending=False).head(10)

        fig = px.bar(
            top,
            x="player_name" if "player_name" in top.columns else top.columns[0],
            y="goals",
            color="team_display" if "team_display" in top.columns else None,
            title="Top 10 Goal Scorers",
        )

        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(top)

    else:
        st.warning("Goals column not found.")


# =========================
# PLAYMAKERS
# =========================
elif page == "Playmakers":

    if "assists" in attacking.columns:

        top = attacking.sort_values("assists", ascending=False).head(10)

        fig = px.bar(
            top,
            x="player_name" if "player_name" in top.columns else top.columns[0],
            y="assists",
            color="team_display" if "team_display" in top.columns else None,
            title="Top Assist Providers",
        )

        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(top)

    else:
        st.warning("Assists column not found.")


# =========================
# DEFENDERS
# =========================
elif page == "Defenders":

    if "tackles" in defending.columns:

        top = defending.sort_values("tackles", ascending=False).head(10)

        fig = px.bar(
            top,
            x="player_name" if "player_name" in top.columns else top.columns[0],
            y="tackles",
            color="team_display" if "team_display" in top.columns else None,
            title="Top Tacklers",
        )

        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(top)

    else:
        st.warning("Tackles column not found.")


# =========================
# GOALKEEPERS
# =========================
elif page == "Goalkeepers":

    if "saves" in goalkeeping.columns:

        top = goalkeeping.sort_values("saves", ascending=False).head(10)

        fig = px.bar(
            top,
            x="player_name" if "player_name" in top.columns else top.columns[0],
            y="saves",
            color="team_display" if "team_display" in top.columns else None,
            title="Top Goalkeepers",
        )

        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(top)

    else:
        st.warning("Saves column not found.")


# =========================
# DISCIPLINE
# =========================
elif page == "Discipline":

    if "yellow_cards" in disciplinary.columns and "red_cards" in disciplinary.columns:

        disciplinary["total_cards"] = (
            disciplinary["yellow_cards"] + disciplinary["red_cards"]
        )

        top = disciplinary.sort_values("total_cards", ascending=False).head(10)

        fig = px.bar(
            top,
            x="player_name" if "player_name" in top.columns else top.columns[0],
            y="total_cards",
            color="team_display" if "team_display" in top.columns else None,
            title="Most Booked Players",
        )

        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(top)

    else:
        st.warning("Card columns not found.")


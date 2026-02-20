import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Football Stats Analyzer", layout="wide")
st.title(" Football Stats Analyzer")

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
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass
    return df


# =========================
# PLAYER MERGE
# =========================
def merge_players(df, players):
    if "id_player" in df.columns and "id_player" in players.columns:
        df = df.merge(players, on="id_player", how="left")
    return df


# =========================
# TEAM MERGE (100% FIX)
# =========================
def merge_teams(df, teams):

    if "id_team" in df.columns and "id_team" in teams.columns:

        df = df.merge(teams, on="id_team", how="left")

        # team nom ustunini aniqlaymiz
        if "team" in df.columns:
            df["team"] = df["team"]
        elif "name" in df.columns:
            df["team"] = df["name"]
        else:
            for col in teams.columns:
                if col != "id_team" and teams[col].dtype == "object":
                    df["team"] = df[col]
                    break

        # id_team ni o‘chiramiz
        df = df.drop(columns=["id_team"], errors="ignore")

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

    # Merge players
    attacking = merge_players(attacking, players)
    defending = merge_players(defending, players)
    goalkeeping = merge_players(goalkeeping, players)
    goals = merge_players(goals, players)
    disciplinary = merge_players(disciplinary, players)

    # Merge teams
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
st.sidebar.title("📊 Navigation")
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
            x="player_name",
            y="goals",
            color="team" if "team" in top.columns else None,
            title="Top 10 Goal Scorers",
        )

        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(top[["player_name", "team", "goals"]])

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
            x="player_name",
            y="assists",
            color="team" if "team" in top.columns else None,
            title="Top Assist Providers",
        )

        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(top[["player_name", "team", "assists"]])

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
            x="player_name",
            y="tackles",
            color="team" if "team" in top.columns else None,
            title="Top Tacklers",
        )

        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(top[["player_name", "team", "tackles"]])

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
            x="player_name",
            y="saves",
            color="team" if "team" in top.columns else None,
            title="Top Goalkeepers",
        )

        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(top[["player_name", "team", "saves"]])

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
            x="player_name",
            y="total_cards",
            color="team" if "team" in top.columns else None,
            title="Most Booked Players",
        )

        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(top[["player_name", "team", "total_cards"]])

    else:
        st.warning("Card columns not found.")


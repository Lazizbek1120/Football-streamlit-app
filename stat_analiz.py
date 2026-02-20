import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Football Stats Analyzer", layout="wide")
st.title(" Football Stats Analyzer Dashboard")


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
# NUMERIC AUTO CONVERTER
# =========================
def convert_numeric(df):
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="ignore")
    return df


# =========================
# AUTO TEAM COLUMN DETECTOR
# =========================
def get_team_column(df):
    possible_team_cols = [
        "team",
        "team_name",
        "club",
        "club_name",
        "squad"
    ]
    for col in possible_team_cols:
        if col in df.columns:
            return col
    return None


# =========================
# SAFE PLAYER MERGE
# =========================
def merge_players(df, players):
    if "id_player" in df.columns and "id_player" in players.columns:
        df = df.merge(players, on="id_player", how="left")
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
    teams = convert_numeric(teams)

    # Merge players
    attacking = merge_players(attacking, players)
    defending = merge_players(defending, players)
    goalkeeping = merge_players(goalkeeping, players)
    goals = merge_players(goals, players)
    disciplinary = merge_players(disciplinary, players)

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
        "Team Comparison",
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
# GENERIC PLAYER PAGE
# =========================
def player_page(df, stat_column, title):

    if stat_column in df.columns:

        top = df.sort_values(stat_column, ascending=False).head(10)

        team_col = get_team_column(top)

        x_col = "player_name" if "player_name" in top.columns else top.columns[0]

        fig = px.bar(
            top,
            x=x_col,
            y=stat_column,
            title=title,
        )

        st.plotly_chart(fig, use_container_width=True)

        show_cols = [x_col, stat_column]
        if team_col:
            show_cols.append(team_col)

        st.dataframe(top[show_cols])

    else:
        st.warning(f"{stat_column} column not found.")


# =========================
# TOP SCORERS
# =========================
elif page == "Top Scorers":
    player_page(goals, "goals", "Top 10 Goal Scorers")


# =========================
# PLAYMAKERS
# =========================
elif page == "Playmakers":
    player_page(attacking, "assists", "Top 10 Assist Providers")


# =========================
# DEFENDERS
# =========================
elif page == "Defenders":
    player_page(defending, "tackles", "Top 10 Tacklers")


# =========================
# GOALKEEPERS
# =========================
elif page == "Goalkeepers":
    player_page(goalkeeping, "saves", "Top 10 Goalkeepers")


# =========================
# DISCIPLINE
# =========================
elif page == "Discipline":

    if "yellow_cards" in disciplinary.columns and "red_cards" in disciplinary.columns:

        disciplinary["total_cards"] = (
            disciplinary["yellow_cards"] + disciplinary["red_cards"]
        )

        player_page(disciplinary, "total_cards", "Most Booked Players")

    else:
        st.warning("Card columns not found.")


# =========================
# TEAM COMPARISON
# =========================
elif page == "Team Comparison":

    team_col = get_team_column(teams)

    if team_col:

        team_list = teams[team_col].unique()

        team1 = st.selectbox("Select Team 1", team_list)
        team2 = st.selectbox("Select Team 2", team_list)

        team1_data = teams[teams[team_col] == team1]
        team2_data = teams[teams[team_col] == team2]

        comparison = pd.concat([team1_data, team2_data])

        numeric_cols = comparison.select_dtypes(include="number").columns

        if len(numeric_cols) > 0:
            fig = px.bar(
                comparison,
                x=team_col,
                y=numeric_cols,
                barmode="group",
                title="Team Comparison",
            )
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(comparison)
        else:
            st.warning("No numeric columns available.")

    else:
        st.warning("Team column not found in teams dataset.")

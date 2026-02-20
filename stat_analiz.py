import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Football Stats Analyzer", layout="wide")

st.title(" Football Stats Analyzer")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    attacking = pd.read_csv("attacking_data.csv")
    defending = pd.read_csv("defending_data.csv")
    goalkeeping = pd.read_csv("goalkeeping_data.csv")
    goals = pd.read_csv("goals_data.csv")
    disciplinary = pd.read_csv("disciplinary_data.csv")
    players = pd.read_csv("players_data.csv")
    teams = pd.read_csv("teams_data.csv")

    # Normalize column names
    attacking.columns = attacking.columns.str.lower()
    defending.columns = defending.columns.str.lower()
    goalkeeping.columns = goalkeeping.columns.str.lower()
    goals.columns = goals.columns.str.lower()
    disciplinary.columns = disciplinary.columns.str.lower()
    players.columns = players.columns.str.lower()
    teams.columns = teams.columns.str.lower()

    # Merge all player-based tables
    attacking = attacking.merge(players, on="id_player", how="left")
    defending = defending.merge(players, on="id_player", how="left")
    goalkeeping = goalkeeping.merge(players, on="id_player", how="left")
    goals = goals.merge(players, on="id_player", how="left")
    disciplinary = disciplinary.merge(players, on="id_player", how="left")

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
    st.subheader("Tournament Overview")

    col1, col2, col3 = st.columns(3)

    total_goals = pd.to_numeric(goals["goals"], errors="coerce").sum()

    col1.metric("Total Teams", teams.shape[0])
    col2.metric("Total Players", players.shape[0])
    col3.metric("Total Goals", int(total_goals))


# =========================
# TOP SCORERS
# =========================
elif page == "Top Scorers":
    st.subheader("Top 10 Goal Scorers")

    goals["goals"] = pd.to_numeric(goals["goals"], errors="coerce")

    top_scorers = goals.sort_values("goals", ascending=False).head(10)

    fig = px.bar(
        top_scorers,
        x="player_name",
        y="goals",
        title="Top 10 Scorers",
    )

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(top_scorers[["player_name", "team", "goals"]])


# =========================
# PLAYMAKERS
# =========================
elif page == "Playmakers":
    st.subheader("Top 10 Assist Providers")

    attacking["assists"] = pd.to_numeric(attacking["assists"], errors="coerce")

    top_assist = attacking.sort_values("assists", ascending=False).head(10)

    fig = px.bar(
        top_assist,
        x="player_name",
        y="assists",
        title="Top Assist Providers",
    )

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(top_assist[["player_name", "team", "assists"]])


# =========================
# DEFENDERS
# =========================
elif page == "Defenders":
    st.subheader("Top 10 Tacklers")

    defending["tackles"] = pd.to_numeric(defending["tackles"], errors="coerce")

    top_def = defending.sort_values("tackles", ascending=False).head(10)

    fig = px.bar(
        top_def,
        x="player_name",
        y="tackles",
        title="Top Tacklers",
    )

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(top_def[["player_name", "team", "tackles"]])


# =========================
# GOALKEEPERS
# =========================
elif page == "Goalkeepers":
    st.subheader("Top 10 Goalkeepers (Saves)")

    goalkeeping["saves"] = pd.to_numeric(goalkeeping["saves"], errors="coerce")

    top_gk = goalkeeping.sort_values("saves", ascending=False).head(10)

    fig = px.bar(
        top_gk,
        x="player_name",
        y="saves",
        title="Top Goalkeepers",
    )

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(top_gk[["player_name", "team", "saves"]])


# =========================
# DISCIPLINE
# =========================
elif page == "Discipline":
    st.subheader("Most Booked Players")

    disciplinary["yellow_cards"] = pd.to_numeric(
        disciplinary["yellow_cards"], errors="coerce"
    )
    disciplinary["red_cards"] = pd.to_numeric(
        disciplinary["red_cards"], errors="coerce"
    )

    disciplinary["total_cards"] = (
        disciplinary["yellow_cards"] + disciplinary["red_cards"]
    )

    top_cards = disciplinary.sort_values("total_cards", ascending=False).head(10)

    fig = px.bar(
        top_cards,
        x="player_name",
        y="total_cards",
        title="Most Cards",
    )

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(
        top_cards[
            ["player_name", "team", "yellow_cards", "red_cards", "total_cards"]
        ]
    )


# =========================
# TEAM COMPARISON
# =========================
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

    if len(numeric_cols) > 0:
        fig = px.bar(
            comparison,
            x="team_name",
            y=numeric_cols,
            barmode="group",
            title="Team Comparison",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:

        st.warning("No numeric columns available for comparison.")

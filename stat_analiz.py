import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Football Stats Analyzer", layout="wide")
st.title(" Football Stats Analyzer")


# ======================
# CLEAN COLUMNS
# ======================
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


# ======================
# SAFE NUMERIC CONVERT
# ======================
def convert_numeric(df):
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="ignore")
    return df


# ======================
# FIND TEAM COLUMN
# ======================
def find_team_column(df):
    for col in ["team", "team_name", "club", "club_name", "squad"]:
        if col in df.columns:
            return col
    return None


# ======================
# LOAD DATA
# ======================
@st.cache_data
def load_data():

    attacking = convert_numeric(clean_columns(pd.read_csv("attacking_data.csv")))
    defending = convert_numeric(clean_columns(pd.read_csv("defending_data.csv")))
    goalkeeping = convert_numeric(clean_columns(pd.read_csv("goalkeeping_data.csv")))
    goals = convert_numeric(clean_columns(pd.read_csv("goals_data.csv")))
    disciplinary = convert_numeric(clean_columns(pd.read_csv("disciplinary_data.csv")))
    players = convert_numeric(clean_columns(pd.read_csv("players_data.csv")))
    teams = convert_numeric(clean_columns(pd.read_csv("teams_data.csv")))

    # Merge players if possible
    if "id_player" in players.columns:
        if "id_player" in attacking.columns:
            attacking = attacking.merge(players, on="id_player", how="left")
        if "id_player" in defending.columns:
            defending = defending.merge(players, on="id_player", how="left")
        if "id_player" in goalkeeping.columns:
            goalkeeping = goalkeeping.merge(players, on="id_player", how="left")
        if "id_player" in goals.columns:
            goals = goals.merge(players, on="id_player", how="left")
        if "id_player" in disciplinary.columns:
            disciplinary = disciplinary.merge(players, on="id_player", how="left")

    return attacking, defending, goalkeeping, goals, disciplinary, players, teams


attacking, defending, goalkeeping, goals, disciplinary, players, teams = load_data()


# ======================
# SIDEBAR
# ======================
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


# ======================
# GENERIC PLAYER PAGE
# ======================
def show_player_stat(df, stat_col, title):

    if stat_col not in df.columns:
        st.warning(f"{stat_col} column not found.")
        return

    df = df.sort_values(stat_col, ascending=False).head(10)

    player_col = "player_name" if "player_name" in df.columns else df.columns[0]
    team_col = find_team_column(df)

    fig = px.bar(df, x=player_col, y=stat_col, title=title)
    st.plotly_chart(fig, use_container_width=True)

    show_cols = [player_col, stat_col]
    if team_col:
        show_cols.append(team_col)

    st.dataframe(df[show_cols])


# ======================
# PAGES
# ======================
if page == "Home":

    total_goals = goals["goals"].sum() if "goals" in goals.columns else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Teams", len(teams))
    col2.metric("Total Players", len(players))
    col3.metric("Total Goals", int(total_goals))


elif page == "Top Scorers":
    show_player_stat(goals, "goals", "Top 10 Goal Scorers")


elif page == "Playmakers":
    show_player_stat(attacking, "assists", "Top 10 Assist Providers")


elif page == "Defenders":
    show_player_stat(defending, "tackles", "Top 10 Tacklers")


elif page == "Goalkeepers":
    show_player_stat(goalkeeping, "saves", "Top 10 Goalkeepers")


elif page == "Discipline":

    if "yellow_cards" in disciplinary.columns and "red_cards" in disciplinary.columns:
        disciplinary["total_cards"] = (
            disciplinary["yellow_cards"] + disciplinary["red_cards"]
        )
        show_player_stat(disciplinary, "total_cards", "Most Booked Players")
    else:
        st.warning("Card columns not found.")


elif page == "Team Comparison":

    team_col = find_team_column(teams)

    if not team_col:
        st.warning("Team column not found in teams dataset.")
    else:
        team_list = teams[team_col].unique()

        team1 = st.selectbox("Select Team 1", team_list)
        team2 = st.selectbox("Select Team 2", team_list)

        df_compare = teams[teams[team_col].isin([team1, team2])]

        numeric_cols = df_compare.select_dtypes(include="number").columns

        if len(numeric_cols) == 0:
            st.warning("No numeric stats available.")
        else:
            fig = px.bar(
                df_compare,
                x=team_col,
                y=numeric_cols,
                barmode="group",
                title="Team Comparison",
            )
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(df_compare)

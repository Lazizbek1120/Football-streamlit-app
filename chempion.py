import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="UCL 2025-26 Dashboard", layout="wide")
st.title("UEFA Champions League 2025-26 Data Analysis Dashboard")


# LOAD DATA

df = pd.read_csv("ucl_2025_26_matches_with_goals.csv")

# Ensure numeric
df["home_goals"] = pd.to_numeric(df["home_goals"], errors="coerce")
df["away_goals"] = pd.to_numeric(df["away_goals"], errors="coerce")

# Total goals per match
df["total_goals"] = df["home_goals"] + df["away_goals"]


# 1️ ENG KO‘P GOL URGAN JAMOA

home_goals = df.groupby("home_team")["home_goals"].sum()
away_goals = df.groupby("away_team")["away_goals"].sum()

total_scored = home_goals.add(away_goals, fill_value=0).sort_values(ascending=False)

st.subheader(" Eng ko‘p gol urgan jamoalar")
fig1 = px.bar(total_scored.head(10),
              title="Top 10 Goal Scoring Teams",
              labels={"value":"Goals","index":"Team"})
st.plotly_chart(fig1, use_container_width=True)


# 2️ ENG KO‘P GOL O‘TKAZGAN JAMOA

home_conceded = df.groupby("home_team")["away_goals"].sum()
away_conceded = df.groupby("away_team")["home_goals"].sum()

total_conceded = home_conceded.add(away_conceded, fill_value=0).sort_values(ascending=False)

st.subheader(" Eng ko‘p gol o‘tkazgan jamoalar")
fig2 = px.bar(total_conceded.head(10),
              title="Most Goals Conceded",
              labels={"value":"Goals","index":"Team"})
st.plotly_chart(fig2, use_container_width=True)


# 3️ UY VS SAFAR STATISTIKASI

st.subheader(" Uy vs ✈ Safar Statistikasi")

home_total = df["home_goals"].sum()
away_total = df["away_goals"].sum()

col1, col2 = st.columns(2)
col1.metric("Uyda urilgan jami gollar", int(home_total))
col2.metric("Safarda urilgan jami gollar", int(away_total))


# 4️ ENG NATIJADOR O‘YINLAR

st.subheader(" Eng natijador o‘yinlar")

top_matches = df.sort_values("total_goals", ascending=False).head(10)

st.dataframe(
    top_matches[["date","home_team","away_team","home_goals","away_goals","total_goals"]]
)


# 5️ O‘RTACHA GOL KO‘RSATKICHI

st.subheader(" O‘rtacha gol ko‘rsatkichi")

avg_goals = df["total_goals"].mean()
st.metric("Har o‘yinga o‘rtacha gol", round(avg_goals, 2))

fig3 = px.histogram(df, x="total_goals", nbins=12,
                    title="Goal Distribution Per Match")
st.plotly_chart(fig3, use_container_width=True)


# 6️ CHEMPION BASHORATI (POINT SYSTEM)

st.subheader(" Kubok sohibi bashorati")

teams = list(set(df["home_team"]).union(set(df["away_team"])))
points = {team: 0 for team in teams}
goal_diff = {team: 0 for team in teams}

for _, row in df.iterrows():
    home = row["home_team"]
    away = row["away_team"]
    hg = row["home_goals"]
    ag = row["away_goals"]

    goal_diff[home] += hg - ag
    goal_diff[away] += ag - hg

    if hg > ag:
        points[home] += 3
    elif hg < ag:
        points[away] += 3
    else:
        points[home] += 1
        points[away] += 1

table = pd.DataFrame({
    "Points": points,
    "Goal Difference": goal_diff
}).sort_values(["Points","Goal Difference"], ascending=False)

st.dataframe(table.head(10))

predicted_champion = table.index[0]


st.success(f" Bashorat qilingan chempion: {predicted_champion}")

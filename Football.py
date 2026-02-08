import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Football.csv")

st.set_page_config(page_title="Futbol Analiz", layout="wide")

st.title("⚽ La Liga Player Statistikasi")

st.sidebar.header("Filter")

year = st.sidebar.selectbox("Yil tanlang", df["Year"].unique())
league = st.sidebar.selectbox("Liga tanlang", df["League"].unique())
club = st.sidebar.selectbox("Klub tanlang", df["Club"].unique())

filtered_df = df[
    (df["Year"] == year) &
    (df["League"] == league) &
    (df["Club"] == club)
]

st.subheader("O'yinchilar ro'yxati")
st.dataframe(filtered_df)

st.subheader("Top 10 Eng Ko'p Gol")

top_players = filtered_df.sort_values(by="Goals", ascending=False).head(10)

plt.figure()
plt.bar(top_players["Player Names"], top_players["Goals"])
plt.xticks(rotation=45)
st.pyplot(plt)
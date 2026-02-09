import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sahifa sozlamasi
st.set_page_config(page_title="Futbol Analiz", layout="wide")

st.title(" Futbol Player Statistikasi Dashboard")

# CSV faylni o‘qish
df = pd.read_csv("Football.csv")

# Sidebar filterlar
st.sidebar.header("Filter")

year = st.sidebar.selectbox("Yil tanlang", sorted(df["Year"].unique()))
league = st.sidebar.selectbox("Liga tanlang", df["League"].unique())
club = st.sidebar.selectbox("Klub tanlang", df["Club"].unique())

# Filtrlash
filtered_df = df[
    (df["Year"] == year) &
    (df["League"] == league) &
    (df["Club"] == club)
]

st.subheader(" O'yinchilar ro'yxati")
st.dataframe(filtered_df)

# Agar ma'lumot bo‘lsa grafik chiqarish
if not filtered_df.empty:
    st.subheader(" Top 10 Eng Ko'p Gol Urganlar")

    top_players = filtered_df.sort_values(
        by="Goals", ascending=False
    ).head(10)

    plt.figure()
    plt.bar(top_players["Player Names"], top_players["Goals"])
    plt.xticks(rotation=45)
    plt.xlabel("O'yinchi")
    plt.ylabel("Gollar")
    st.pyplot(plt)
else:
    st.warning("Ma'lumot topilmadi.")
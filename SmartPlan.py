import streamlit as st
from auth import register_user, authenticate_user
from layout_engine import generate_layout
from plotly_3d import generate_3d

st.title("🏠 SmartPlan AI - Pro MVP")

menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

if menu == "Register":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        register_user(username, password)
        st.success("User created!")

if menu == "Login":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate_user(username, password):
            st.success("Logged in!")

            width = st.number_input("Width", min_value=5)
            height = st.number_input("Height", min_value=5)
            rooms = st.slider("Rooms", 2, 6)

            if st.button("Generate Layout"):
                layout = generate_layout(width, height, rooms)
                st.write(layout)

                fig = generate_3d(layout)
                st.plotly_chart(fig)
        else:

            st.error("Wrong credentials")


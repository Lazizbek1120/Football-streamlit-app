import streamlit as st
from Database import SessionLocal, User, Project
from auth import register_user, authenticate_user
from layout_engine import generate_layout
from plotly_3d import generate_3d

st.set_page_config(page_title="SmartPlan AI", layout="wide")

st.title("🏠 SmartPlan AI - Startup MVP")

# =========================
# SESSION
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None


# =========================
# SIDEBAR MENU
# =========================
menu = st.sidebar.selectbox("Menu", ["Login", "Register"])


# =========================
# REGISTER
# =========================
if menu == "Register":
    st.subheader("Create Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        register_user(username, password)
        st.success("User created! Now login.")


# =========================
# LOGIN
# =========================
if menu == "Login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate_user(username, password):
            st.session_state.logged_in = True
            st.session_state.user = username
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Wrong credentials")


# =========================
# AFTER LOGIN
# =========================
if st.session_state.logged_in:

    st.sidebar.success(f"Welcome {st.session_state.user}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

    st.subheader("Generate Your House Plan")

    width = st.number_input("Width (meters)", min_value=5)
    height = st.number_input("Height (meters)", min_value=5)
    rooms = st.slider("Number of Rooms", 2, 6)

    if st.button("Generate Layout"):
        layout = generate_layout(width, height, rooms)

        st.write("### 📐 Room Layout")
        st.write(layout)

        st.write("### 🏗 3D Preview")
        fig = generate_3d(layout)
        st.plotly_chart(fig)

        # SAVE PROJECT
        if st.button("Save Project"):
            db = SessionLocal()

            user = db.query(User).filter(
                User.username == st.session_state.user
            ).first()

            project = Project(
                user_id=user.id,
                name="My House Plan",
                data=str(layout)
            )

            db.add(project)
            db.commit()
            db.close()

            st.success("Project saved successfully!")
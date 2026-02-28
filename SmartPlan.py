import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from passlib.context import CryptContext
import plotly.graph_objects as go

# =========================
# DATABASE
# =========================
engine = create_engine("sqlite:///smartplan.db")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    name = Column(String)
    data = Column(String)

Base.metadata.create_all(engine)

# =========================
# AUTH
# =========================
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

def register_user(username, password):
    db = SessionLocal()
    hashed = pwd_context.hash(password)
    user = User(username=username, password=hashed)
    db.add(user)
    db.commit()
    db.close()

def authenticate_user(username, password):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    return pwd_context.verify(password, user.password)

# =========================
# COST ENGINE
# =========================
REGION_COEFFICIENT = {
    "Toshkent": 1.2,
    "Samarqand": 1.0,
    "Qashqadaryo": 0.9
}

MATERIAL_MULTIPLIER = {
    "Brick": 1.0,
    "Concrete": 1.3,
    "Frame": 0.8
}

def calculate_materials(area, floors, material, region):
    region_coef = REGION_COEFFICIENT[region]
    material_coef = MATERIAL_MULTIPLIER[material]
    total_area = area * floors

    concrete = total_area * 0.25 * material_coef
    bricks = total_area * 120 * material_coef
    rebar = total_area * 8 * material_coef
    roof = total_area * 1.1
    total_cost = total_area * 300 * region_coef * material_coef

    return {
        "Concrete (m3)": round(concrete, 2),
        "Bricks (pcs)": int(bricks),
        "Rebar (kg)": round(rebar, 2),
        "Roof material (m2)": round(roof, 2),
        "Estimated Cost ($)": round(total_cost, 2)
    }

# =========================
# SMART LAYOUT
# =========================
def generate_smart_layout(width, height):
    return [
        {"name": "Living Room", "zone": "front"},
        {"name": "Kitchen", "zone": "middle"},
        {"name": "Bathroom", "zone": "corner"},
        {"name": "Bedroom", "zone": "back"},
        {"name": "Garage", "zone": "outer"}
    ]

# =========================
# 3D ENGINE
# =========================
def generate_3d():
    fig = go.Figure()
    fig.add_trace(go.Mesh3d(
        x=[0,5,5,0],
        y=[0,0,5,5],
        z=[0,0,3,3],
        opacity=0.5
    ))
    return fig

# =========================
# UI
# =========================
st.set_page_config(page_title="SmartPlan AI", layout="wide")
st.title("🏠 SmartPlan AI - Startup Version")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

# REGISTER
if menu == "Register":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        register_user(username, password)
        st.success("User created!")

# LOGIN
if menu == "Login":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate_user(username, password):
            st.session_state.logged_in = True
            st.session_state.user = username
            st.success("Logged in!")
            st.rerun()
        else:
            st.error("Wrong credentials")

# AFTER LOGIN
if st.session_state.logged_in:
    st.sidebar.success(f"Welcome {st.session_state.user}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.subheader("House Parameters")

    width = st.number_input("Width (m)", min_value=5)
    height = st.number_input("Height (m)", min_value=5)
    floors = st.slider("Floors", 1, 3)
    material = st.selectbox("Material", ["Brick", "Concrete", "Frame"])
    region = st.selectbox("Region", ["Toshkent", "Samarqand", "Qashqadaryo"])

    if st.button("Generate Smart Plan"):

        layout = generate_smart_layout(width, height)
        st.write("### Smart Room Placement")
        st.write(layout)

        area = width * height
        materials = calculate_materials(area, floors, material, region)

        st.write("### Construction Materials & Estimated Cost")
        st.write(materials)

        st.write("### 3D Preview")
        fig = generate_3d()
        st.plotly_chart(fig)

        if st.button("Save Project"):
            db = SessionLocal()
            user = db.query(User).filter(User.username == st.session_state.user).first()
            project = Project(user_id=user.id, name="Smart Plan", data=str(layout))
            db.add(project)
            db.commit()
            db.close()
            st.success("Project Saved!")
from passlib.context import CryptContext
from Database import SessionLocal, User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
    if user and pwd_context.verify(password, user.password):
        return True
    return False
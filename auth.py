from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import FastAPI
import bcrypt
from database import db_conn


def create_table_users():
    conn = db_conn()
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT UNIQUE,
                   password TEXT
                   )
                   """)
    
    conn.commit()
    conn.close()

create_table_users()

app = FastAPI()

SECRET_KEY = "1e038aa16fdc2c17a4eab16b85085d58e4c52617973ca8573aa828a0070a8c7e"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# password
def hash_password(password: str):
    password_bytes = password.encode("utf-8")[:72]
    hashed_by = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_by.decode("utf-8")

def verify_password(plain: str, hashed: str):
    password_bytes = plain.encode("utf-8")[:72]
    return bcrypt.checkpw(password_bytes, hashed.encode("utf-8"))

# token
def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# login
def login(username, password):
    conn = db_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and verify_password(password, user[2]):
        return create_token(user[0])
    
    return None

# register - working
def register(username: str, password: str):
    conn = db_conn()
    cursor = conn.cursor()

    hashed = hash_password(password)
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))

    conn.commit()
    conn.close()

    return f"User named {username} successfully registered"
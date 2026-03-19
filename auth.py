from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import FastAPI
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
pwd_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])



def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@app.post("/register")
def user_register(username, password):
    conn = db_conn()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))

    conn.commit()
    conn.close()
    


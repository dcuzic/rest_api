from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import bcrypt
import sqlite3
from database import db_conn
from models import User

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

# current_user token - needs testing
oauth2_var = OAuth2PasswordBearer(tokenUrl="login")

def current_token(token: str = Depends(oauth2_var)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["ALGORITHM"])
        user_id = payload.get("user_id")

        if user_id == None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

# register - working
@app.post("/register")
def register(user: User):
    conn = db_conn()
    cursor = conn.cursor()

    hashed = hash_password(user.password)

    try: 
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username, hashed))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail=f"Username {user.username} already exists, please choose another username.")
    conn.close()
    return f"User {user.username} successfully registered!"

#login
@app.post("/login")
def login(user: User):
    conn = db_conn()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (user.username,))
    user_check = cursor.fetchone()
    conn.close()

    if not user_check or not verify_password(user.password, user_check["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_token({"user_id": user_check["id"]})
    return {"access_token": token}
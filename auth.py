from fastapi import FastAPI
from database import db_conn

app = FastAPI()

SECRET_KEY = "1e038aa16fdc2c17a4eab16b85085d58e4c52617973ca8573aa828a0070a8c7e"

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

@app.post("/register")
def user_register(username, password):
    conn = db_conn()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))

    conn.commit()
    conn.close()
    


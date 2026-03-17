import models
from database import db_conn

def create_table_users():
    conn = db_conn()
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                   username TEXT UNIQUE,
                   password TEXT
                   )
                   """)
    conn.commit()
    conn.close()

username = 
password = 

def create_user():
    conn = db_conn()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))

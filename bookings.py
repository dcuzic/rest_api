from fastapi import FastAPI, HTTPException
import sqlite3
from models import Booking
from database import db_conn

app = FastAPI()

def create_table_bookings():
    conn = db_conn()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS bookings (
                   id INTEGER PRIMARY KEY AUTOINCREMENT
                   date TEXT NOT NULL
                   people INTEGER
                   created_by TEXT NOT NULL
                   )""")
    
    conn.commit()
    conn.close()
    
@app.post("/booking")
def new_booking(book: Booking):
    conn = db_conn()
    cursor = conn.cursor()

    if 

    cursor.execute("INSERT INTO bookings VALUES (?, ?, ?)", (book.date, book.people, book.created_by))




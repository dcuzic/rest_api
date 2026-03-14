from fastapi import FastAPI, HTTPException
import sqlite3

app = FastAPI()

def create_table():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS bookings (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   date TEXT NOT NULL
                   )              
                   """)
    
    conn.commit()
    conn.close()

create_table()

# adds booking, works
@app.post("/bookings/")
def create_booking(booking_name, booking_date):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
                   INSERT INTO bookings (name, date)
                   VALUES (?, ?)""",
                   (booking_name, booking_date)
                   )
    
    conn.commit()
    conn.close()
    return {"booking successfully created"}

# deletes booking from database, works
@app.delete("/bookings")
def delete_booking(booking_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""DELETE FROM bookings WHERE id = ?""", (booking_id,))

    conn.commit()
    conn.close()
    return {f"booking no {booking_id} successfully deleted"}

# returns all bookings in database, works
@app.get("/bookings/")
def all_bookings():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bookings")
    rows = cursor.fetchall()
    data = [dict(row) for row in rows]

    conn.close()
    return {
        "message": "here are all the bookings in the system right now",
        "data": data
    }

# returns booking info by id, works
@app.get("/bookings/{booking_id}/")
def search_booking(booking_id):
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bookings WHERE id = ?", (booking_id,))
    row = cursor.fetchone()
    booking_info = [dict(row)]

    if booking_info is None:
        raise HTTPException(status_code=404, detail="booking not found")

    conn.close()
    return booking_info


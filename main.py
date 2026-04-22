from fastapi import FastAPI, HTTPException, Depends
from auth import router as auth_router, protected
import sqlite3

app = FastAPI()
app.include_router(auth_router)

# maybe doesnt work
def create_table():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS bookings (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   date TEXT NOT NULL,
                   user_id NOT NULL
                   )              
                   """)
    
    conn.commit()
    conn.close()

create_table()

# adds booking, works
@app.post("/bookings/")
def create_booking(booking_name, booking_date, user_id = Depends(protected)):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()



    cursor.execute("""
                   INSERT INTO bookings (name, date, user_id)
                   VALUES (?, ?, ?)""",
                   (booking_name, booking_date, user_id)
                   )
    
    conn.commit()
    conn.close()
    return {f"booking successfully created, {user_id}"}

# deletes booking from database, works
@app.delete("/bookings")
def delete_booking(booking_id, user_id = Depends(protected)):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM bookings WHERE user_id = ?", (user_id,))
    current_user_bookings = cursor.fetchone()
    if booking_id in current_user_bookings:
        cursor.execute("SELECT * FROM bookings WHERE id = ?", (booking_id,))
        delete_result = cursor.fetchone()
        if delete_result == None:
            conn.close()
            raise HTTPException(status_code=404, detail="404 booking not found")
        else:
            cursor.execute("""DELETE FROM bookings WHERE id = ?""", (booking_id,))
            conn.commit()
            conn.close()
            return {f"booking no {booking_id} successfully deleted", user_id}
    else:
        raise HTTPException(status_code=403, detail="403 forbidden")

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

    if row is not None:
        booking_info = [dict(row)] 
    else:
        raise HTTPException(status_code=404, detail="booking not found")

    conn.close()
    return booking_info




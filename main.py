from fastapi import FastAPI, HTTPException, Depends, Query
from auth import router as auth_router, protected
from database import db_conn
import sqlite3

app = FastAPI()
app.include_router(auth_router)

# bookings database
def create_table():
    conn = db_conn()
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

# checks user role (User, Admin)
@app.get("/admin")
def check_user_role(user_id = Depends(protected)):
    conn = db_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
    role_result = cursor.fetchone()

    conn.close()

    return role_result[0]

# adds booking, users can only create bookings for current user
@app.post("/bookings/")
def create_booking(booking_name, 
                   booking_date, 
                   user_id = Depends(protected), 
                   target_user_id: int | None = Query(
                       default=None,
                       description="ADMIN ONLY: Create booking for any user"
                   )
                   ):
    conn = db_conn()
    cursor = conn.cursor()

    role = check_user_role(user_id)

    if target_user_id is not None and role != "Admin":
        raise HTTPException(status_code=403, detail="403 Forbidden")

    if role == "Admin" and target_user_id:
        final_user_id = target_user_id
    else:
        final_user_id = user_id

    cursor.execute("""
                   INSERT INTO bookings (name, date, user_id)
                   VALUES (?, ?, ?)""",
                   (booking_name, booking_date, final_user_id)
                   )
    
    conn.commit()
    conn.close()
    return {"msg":f"booking successfully created for user {final_user_id}"}

# deletes booking from database users can only delete their bookings
@app.delete("/bookings")
def delete_booking(booking_id: int, user_id: int = Depends(protected)):
    conn = db_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM bookings WHERE id = ?", (booking_id,))
    booking = cursor.fetchone()

    if not booking:
        conn.close()
        raise HTTPException(status_code=404, detail="404 Booking not found")
    
    booking_owner_id = booking[0]

    role = check_user_role(user_id)

    if role != "Admin" and booking_owner_id != user_id:
        conn.close()
        raise HTTPException(status_code=403, detail="403 Forbidden")
    
    cursor.execute("DELETE FROM bookings WHERE id =?", (booking_id,))
    conn.commit()
    conn.close()

    return {"msg":f"booking {booking_id} successfully deleted!"}

# returns all bookings in database, users can see only their bookings
@app.get("/bookings/")
def all_bookings(user_id: int = Depends(protected)):
    conn = db_conn()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    role = check_user_role(user_id)

    if not role :
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")

    if role == "Admin":
        cursor.execute("SELECT * FROM bookings")
    else:
        cursor.execute("SELECT * FROM bookings WHERE user_id = ?", (user_id,))
    
    rows = cursor.fetchall()
    data = [dict(row) for row in rows]
    conn.close()
    return {
    "message": "bookings in the system right now",
    "data": data
    }

# returns booking info by id, users can only see their bookings
@app.get("/bookings/{booking_id}/")
def search_booking(booking_id: int, user_id: int = Depends(protected)):
    conn = db_conn()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM bookings WHERE id = ?", (booking_id,))
    booking = cursor.fetchone()

    if not booking:
        conn.close()
        raise HTTPException(status_code=404, detail="404 Booking not found")
    
    booking_owner_id = booking[0]

    role = check_user_role(user_id)

    if role != "Admin" and booking_owner_id != user_id:
        conn.close()
        raise HTTPException(status_code=403, detail="403 Forbidden")
    
    cursor.execute("SELECT * FROM bookings WHERE id = ?", (booking_id,))
    search_result = cursor.fetchone()

    if search_result is not None:
        booking_info = [dict(search_result)] 

    conn.close()
    return booking_info


# ADMIN:

# delete user
@app.delete("/admin/delete_user")
def delete_user(user_id: int = Depends(protected),
                target_user_id: int | None = Query(
                    default=None,
                    description="ADMIN ONLY: Delete user")
                ):
    conn = db_conn()
    cursor = conn.cursor()

    role = check_user_role(user_id)

    if target_user_id is not None and role != "Admin":
        raise HTTPException(status_code=403, detail="403 Forbidden")
    
    cursor.execute("DELETE FROM users WHERE id = ?", (target_user_id,))
    
    conn.commit()
    conn.close()

    return {"msg":f"user {target_user_id} successfully deleted"}

# create admin
@app.post("/admin/create_admin")
def create_admin(user_id: int = Depends(protected),
                 target_user_id: int | None = Query(
                     default=None,
                     description="ADMIN ONLY: Create new admin"
                 )):
    conn = db_conn()
    cursor = conn.cursor()

    role = check_user_role(user_id)

    if target_user_id is not None and role != "Admin":
        raise HTTPException(status_code=403, detail="403 Forbidden")
    
    cursor.execute("SELECT * FROM users WHERE id = ?", (target_user_id,))
    target_result = cursor.fetchall()

    if not target_result:
        raise HTTPException(status_code=404, detail="404 User not found")
    
    cursor.execute("SELECT role FROM users WHERE id = ?", (target_user_id,))
    user_role = cursor.fetchone()[0]

    if user_role == "Admin":
        raise HTTPException(status_code=409, detail="409 User is already an administrator")
    
    cursor.execute("UPDATE users SET role = ? WHERE id = ?", ("Admin", target_user_id))

    conn.commit()
    conn.close()

    return {"msg":f"user {target_user_id} is now admin"}

# remove admin
@app.patch("/admin/remove_admin")
def remove_admin(user_id: int = Depends(protected),
                 target_user_id: int | None = Query(
                     default=None,
                     description="ADMIN ONLY: Remove admin"
                 )):
    conn = db_conn()
    cursor = conn.cursor()

    role = check_user_role(user_id)

    if target_user_id is not None and role != "Admin":
        raise HTTPException(status_code=403, detail="403 Forbidden")
    
    cursor.execute("SELECT * FROM users WHERE id = ?", (target_user_id,))
    target_result = cursor.fetchall()

    if not target_result:
        raise HTTPException(status_code=404, detail="404 User not found")
    
    cursor.execute("SELECT role FROM users WHERE id = ?", (target_user_id,))
    user_role = cursor.fetchone()[0]

    if user_role == "User":
        raise HTTPException(status_code=409, detail="409 User is not an administrator")
    
    if target_user_id == user_id:
        raise HTTPException(status_code=403, detail="403 Forbidden")
    
    cursor.execute("UPDATE users SET role = ? WHERE id = ?", ("User", target_user_id))

    conn.commit()
    conn.close()

    return {"msg":f"User {target_user_id} is not admin anymore"}

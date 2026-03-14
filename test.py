from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class Booking(BaseModel):
    name: str
    date: str

app = FastAPI()

# database



bookings = []

@app.post("/bookings/")
def create_booking(booking: Booking):
    booking_id = len(bookings) + 1
    booking_dict = booking.dict()
    booking_dict["id"] = booking_id
    bookings.append(booking_dict)
    return booking_dict

@app.get("/bookings/{booking_id}")
def id(booking_id: int):    
    for booking in bookings:
        if booking["id"] == booking_id:
            return booking
        else:
            raise HTTPException(status_code=404, detail="Booking not found")
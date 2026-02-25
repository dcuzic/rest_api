from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


count_file = "count.txt"

class Booking(BaseModel):
    name: str
    date: str

app = FastAPI()

bookings = []
id_count = 1

# це ніби працює no idea how tho 
@app.post("/booking/")
def create_booking(booking: Booking):
    booking_dict = booking.dict()
    global id_count
    booking_id = id_count
    ids = id_count =+ 1
    def increment_counter():
        try:
            with open(count_file, "r") as s:
                count = int(s.read())
        except FileNotFoundError:
            count = 0
        count += 1
        with open(count_file, "w") as s:
            s.write(str(count))
        return count
    booking_dict["id"] = increment_counter()
    bookings.append(booking_dict)
    print(booking_dict)
    return booking_dict

# це працює
@app.get("/booking/")
def all_bookings():
    return bookings

# пише booking not found, Тому працюєм над цим  
@app.get("/booking/{booking_id}")
def id(booking_id: int):
    for booking in bookings:
        if booking_id == booking["id"]:
            print(type(booking_id))
            return booking
    else:
        raise HTTPException(status_code=404, detail="Booking not found")
        
# працює but when post new booking ids mix up, it creates new booking counting its order based on bookings before
@app.delete("/bookings/{booking_id}")
def delete_booking(booking_id: int):
    for booking in bookings:
        if booking["id"] == booking_id:
            bookings.remove(booking)
            return {f"Booking {booking_id} deleted successfully"}
    
    else:
        return HTTPException(status_code=404, detail="Booking not found")



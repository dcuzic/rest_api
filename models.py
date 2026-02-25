from pydantic import BaseModel

class Booking(BaseModel):
    name: str
    date: str

from pydantic import BaseModel

class User(BaseModel): 
    username: str
    password: str

class Booking(BaseModel):
    date: str
    people: str
    created_by: str
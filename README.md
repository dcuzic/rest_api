This is a simple REST API project demonstrating a booking system based on FastAPI for my apprenticeship CV.

The app can:
* Create a new booking
* Search for the booking by ID and return its details
* View all the bookings in in-memory storage
* Delete a booking

How to use:
1. `http://127.0.0.1:8000/booking` - to see all the bookings
2. `http://127.0.0.1:8000/booking/86` - to see booking details. `86` is booking's ID assigned automatically when a booking is created via POST
3. `http://127.0.0.1:8000/docs/` - to post, delete, and get booking's details

How to open:
1. Download FastAPI: `pip install "fastapi[standard]"`
2. Download uvicorn: `pip install uvicorn`
3. Run `uvicorn main:app --reload` in terminal
4. Go to `http://127.0.0.1:8000/` or `http://127.0.0.1:8000/docs` in your browser.

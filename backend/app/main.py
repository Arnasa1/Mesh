from fastapi import FastAPI, Response
from app.api.registration import RegistrationRequest

app = FastAPI(
    title="Mesh API",
    version="0.0.0",
)

@app.get("/")
async def root():
    return {"message": "Mesh API is running"}

@app.post("/register/")
async def registration(username, email, password ):
    return {"username": username, "email": email, "password": password}

from fastapi import FastAPI, Depends, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.registration import RegistrationRequest
from app.models.models import User

app = FastAPI(
    title="Mesh API",
    version="0.0.0",
)

@app.get("/")
async def root():
    return {"message": "Mesh API is running"}

@app.post("/register/")
async def registration(username, email, password, registration: RegistrationRequest, db: Session = Depends(get_db)):

    db_users = User(   
        username = registration.username,
        email = registration.email,
        password_hash = registration.password,
    )
    db.add(db_users)
    db.commit()
    db.refresh(db_users)
    db.close()

    return {
            "username": registration.username,
            "email": registration.email,
            "password": registration.password
            }

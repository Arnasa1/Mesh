from fastapi import FastAPI, Depends, Response, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.registration import RegistrationRequest, RegistrationResponse
from app.models.models import User
import argon2

app = FastAPI(
    title="Mesh API",
    version="0.0.0",
)

router = APIRouter()

ph = argon2.PasswordHasher()

@router.post(
        "/register/",
        response_model = RegistrationResponse,
        status_code = status.HTTP_201_CREATED
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

    # Check username

    existing_username = (
        db.query(User)
        .filter(User.username == registration.username)
        .first()
    )
    if existing_username : 
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Username or Email already exists"
        )

    # Check email

    existing_email = (
        db.query(User)
        .filter(User.username == registration.username)
        .first()
    )

    if existing_email : 
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = "Username or Email already exists"
            )

    password_hash = ph.hash(registration.password)

    try:
        db.add(db_users)
        db.commit()
        db.refresh(db_users)
    except Exception as e:
        db.rollback()
        return Response( content = f"Error: {str(e)}", status_code = 400)


    db.add(db_users)
    db.commit()
    db.refresh(db_users)
    db.close()

    return {
            "username": registration.username,
            "email": registration.email,
            "password": password_hash
            }

from fastapi import FastAPI, Depends, Response, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.exceptions import RequestValidationError
from app.database import get_db
from app.api.document import DocumentCreate
from app.api.registration import RegistrationRequest, RegistrationResponse
from app.models.models import Document, User
import argon2
from fastapi import Request

app = FastAPI(
    title="Mesh API",
    version="0.0.0",
)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return Response(
        content=f"Validation error: {exc}", status_code=400
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

@app.post("/documents/")
async def create_document(document: DocumentCreate,
    db: Session = Depends(get_db),
):
    db_document = Document(
        title=document.title,
        content=document.content,
    )
    try:
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
    except Exception as e:
        db.rollback()
        return Response(
            content=f"Error creating document: {str(e)}", status_code=400)
    return {
        "title": document.title,
        "content": document.content,
    }

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

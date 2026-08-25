from fastapi import FastAPI, Request, Depends, Response, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi.exceptions import RequestValidationError
from app.database import get_db
from app.api.document import DocumentCreate
from app.api.auth import RegistrationRequest, RegistrationResponse, LoginRequest
from app.models.models import Document, User
import argon2

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

    # Check username

    existing_username = (
        db.query(User)
        .filter(User.username == registration.username)
        .first()
    )
    if existing_username : 
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Username already exists"
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
                detail = "Email already exists"
            )

    password_hash = ph.hash(registration.password)

    db_users = User(   
            username = registration.username,
            email = registration.email,
            password_hash = password_hash,
        )

    try:
        db.add(db_users)
        db.commit()
        db.refresh(db_users)
    except Exception as e:
        db.rollback()
        return Response(content=f"Error: 400", status_code=400)

    return {
            "id": db_users.id,
            "email": db_users.email,
            }

@app.post("/login/")
async def login(user, password, login: LoginRequest, db: Session = Depends(get_db)):
    
    # Check db for existing username/email

    existing_user = (
            db.query(User)
            .filter(or_(User.username == login.user, User.email == login.user))
            .first()
        )
    if not existing_user : 
            raise HTTPException(
            detail = "Invalid credencials", status_code=401
        )

    # Check hashed password

    try:
        ph.verify(existing_user.password_hash, login.password)
        return{
                    "status": "login successful", 
              }
    except Exception as e:
            return Response(content=f"Invalid credencials", status_code=401)
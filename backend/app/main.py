from fastapi import FastAPI, Request, Depends, Response, APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi.exceptions import RequestValidationError
from app.database import get_db
from app.api.document import DocumentCreate
from app.api.auth import RegistrationRequest, RegistrationResponse, LoginRequest
from app.models.models import Document, User
from app.api.jwt import create_jwt_token, SECRET_KEY
import jwt
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
        content=f"Validation error: {exc}", status_code=422
    )

router = APIRouter()

ph = argon2.PasswordHasher()

@app.get("/home")
async def root():
    return {"message": "Mesh API is running"}

@app.post("/register", status_code = status.HTTP_201_CREATED)
async def registration(registration: RegistrationRequest, db: Session = Depends(get_db)):

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
        .filter(User.email == registration.email)
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
        return Response(content=f"Unprocessable entity", status_code=422)

    return {
            "status": "Registration successful",
            "email": db_users.email,
            }

@app.post("/login")
async def login(login: LoginRequest, db: Session = Depends(get_db)):
    
    # Check db for existing username/email

    existing_user = (
            db.query(User)
            .filter(or_(User.username == login.user, User.email == login.user))
            .first()
        )
    if not existing_user : 
            raise HTTPException(
            detail = "Invalid credentials", status_code=401
        )
    

    # Check hashed password
    try:
        ph.verify(existing_user.password_hash, login.password)
    except Exception as e:
            return Response(content=f"Invalid credentials", status_code=401)

    # Creating jwt token
    token = create_jwt_token(user_id=existing_user.id, username=existing_user.username, expires_in_minutes=30)

    response = JSONResponse(
        content={
            "status": "Login successful",
        }
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,       # JS can't read it — mitigates XSS token theft
        secure=True,         # only sent over HTTPS (set False for local http dev)
        samesite="lax",      # or "strict"/"none" depending on your CORS setup
        max_age=30 * 60,     # match your JWT expiry, in seconds
        path="/",
    )

    return response

async def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == payload["user_id"]).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@app.get("/me")
async def read_current_user(user: User = Depends(get_current_user)):
     return{
          "username": user.username,
     }

@app.post("/documents/")
async def create_document(document: DocumentCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
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
            content=f"Bad request: {str(e)}", status_code=400)
    return {
        "title": document.title,
        "content": document.content,
    }

@app.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token", path="/")
    return{
          "status": "Logged out"
     }
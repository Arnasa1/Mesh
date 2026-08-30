from fastapi import FastAPI, Request, Depends, Response, APIRouter, status, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default; adjust if different
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    error = exc.errors()[0]

    field = error["loc"][-1]

    messages = {
        "email": "Invalid email address.",
        "password": "Invalid password.",
    }

    return JSONResponse(
        content={"message": messages.get(field, error["msg"])},
        status_code=422,
    )

router = APIRouter()

ph = argon2.PasswordHasher()

@app.get("/")
async def root():
    return RedirectResponse(url="/home")

@app.get("/home")
async def home():
    return {"message": "Mesh API is running"}

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def registration(registration: RegistrationRequest, db: Session = Depends(get_db)):
    
    existing_username = (
        db.query(User)
        .filter(User.username == registration.username)
        .first()
    )
    if existing_username:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"message": "Username already exists"},
        )

    # Check email
    existing_email = (
        db.query(User)
        .filter(User.email == registration.email)
        .first()
    )
    if existing_email:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"message": "Email already exists"},
        )

    password_hash = ph.hash(registration.password)

    db_user = User(
        username=registration.username,
        email=registration.email,
        password_hash=password_hash,
    )

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"message": "Unprocessable entity"},
            status_code=422,
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "Registration successful",
            "email": db_user.email,
        },
    )

@app.post("/login")
async def login(login: LoginRequest, db: Session = Depends(get_db)):

    # Check db for existing username/email
    existing_user = (
        db.query(User)
        .filter(or_(User.username == login.username, User.email == login.username))
        .first()
    )
    if not existing_user:
        return JSONResponse(
            content={"message": "Invalid credentials"},
            status_code=401,
        )

    # Check hashed password
    try:
        ph.verify(existing_user.password_hash, login.password)
    except Exception as e:
        return JSONResponse(
            content={"message": "Invalid credentials"},
            status_code=401,
        )

    # Creating jwt token
    token = create_jwt_token(user_id=existing_user.id, username=existing_user.username, expires_in_minutes=30)

    response = JSONResponse(
        content={
            "message": "Login successful",
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
    return {
        "username": user.username,
    }

@app.post("/documents/")
async def create_document(
    document: DocumentCreate,
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
        return JSONResponse(
            content={"message": f"Bad request: {str(e)}"},
            status_code=400,
        )
    return {
        "title": document.title,
        "content": document.content,
    }

@app.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token", path="/")
    return {
        "message": "Logged out",
    }
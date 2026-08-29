from app.database import get_db
from app.models.models import User
from pydantic import BaseModel, Field, EmailStr, field_validator
import re

class RegistrationRequest(BaseModel):
    username: str = Field(..., max_length=255)
    email: EmailStr = Field(..., max_length=255)
    password: str = Field(min_length=12, max_length=20)
    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain a lowercase letter")

        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain an uppercase letter")

        if not re.search(r"\d", password):
            raise ValueError("Password must contain a digit")

        if not re.search(r"[!@#$%^&*_\-+=~?.,]", password):
            raise ValueError("Password must contain a special character")

        if not re.fullmatch(r"[A-Za-z\d!@#$%^&*_\-+=~?.,]+", password):
            raise ValueError("Password contains invalid characters")

        return password



class RegistrationResponse(BaseModel):
    status: str
    id: int
    username: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    username: str = Field(..., max_length=255)
    password: str = Field(min_length=12, max_length=20)

class LoginResponse(BaseModel):
    username: str
    password: str
# Password validation rules
# -------------------------
# Have at least one number
# Have at least one uppercase letter
# Have at least one lowercase letter
# Have at least one special character ($, @, #, %)
# Be between 12 and 20 characters in length
# -------------------------
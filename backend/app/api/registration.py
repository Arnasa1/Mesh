from app.database import get_db
from app.models.models import User
from pydantic import BaseModel, EmailStr
import argon2

class RegistrationRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class RegistrationResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

ph = argon2.PasswordHasher()

def login(db, user, password):
    hash = db.get_password_hash_for_user(user)

    ph.verify(hash, password)
    if ph.check_needs_rehash(hash):
        db.set_password_hash_for_user(user, ph.hash(password))

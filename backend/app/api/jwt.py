import jwt

from app.database import get_db
from app.main import Session, Depends
from app.api.auth import LoginRequest
from app.models.models import User
import datetime
import os

SECRET_KEY = os.urandom(32)

def create_jwt_token(user_id: int, username: str, expires_in_minutes: int):
    now = datetime.datetime.now(datetime.timezone.utc)
    payload ={
        'user_id': user_id,
        'username':username,
        'exp': now + datetime.timedelta(minutes=expires_in_minutes),
        'iat': now.isoformat(),
        'sub': 'Login request'
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    

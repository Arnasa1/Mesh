from app.database import get_db
from app.main import Session, Depends
from app.api.auth import LoginRequest
from app.models.models import User
import datetime
import os

SECRET_KEY = os.urandom(32)
now = datetime.datetime.now()

def create_jwt_token(db: Session = Depends(get_db), expires_in_minutes=30):
    db.query(User)
    {
        'user_id': User.id,
        'username': User.username,
        'exp': now + datetime.timedelta(minutes=expires_in_minutes),
        'iat': now.isoformat(),
        'sub': 'Login request'
    }
    

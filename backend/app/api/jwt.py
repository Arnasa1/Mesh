import jwt
import datetime
import os

SECRET_KEY = "5wEmTdg0XoMU4LDgZ0h7AHCehMIzmZlrTq-8nc6mfaw"
#temp

def create_jwt_token(user_id: int, username: str, expires_in_minutes: int):
    now = datetime.datetime.now(datetime.timezone.utc)
    payload ={
        'user_id': user_id,
        'username':username,
        'exp': now + datetime.timedelta(minutes=expires_in_minutes),
        'iat': now,
        'sub': 'Login request'
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

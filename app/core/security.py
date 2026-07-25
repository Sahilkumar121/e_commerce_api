from app.core.config import setting
from jose import jwt
from datetime import datetime, timezone, timedelta

from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def get_hashed_password(plain_password: str):
    return password_hash.hash(plain_password)

def verify_hashed_password(plain_password: str, hashed_password) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def create_access_token(data: dict):

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=setting.ACCESS_TOKEN_TIME_EXPIRE)

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, setting.SECRETE_KEY, algorithm=setting.ALGORITHM)

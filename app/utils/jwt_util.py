import os
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

SECRET_KEY = os.getenv("SECRET_KEY", "happycat")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta = None, is_admin: bool = False) -> str:
    to_encode = data.copy()
    
    to_encode.update({"role": "ADMIN" if is_admin else "USER"})
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise JWTError("토큰 검증에 실패하였습니다.")

def is_admin_token(token: str) -> bool:
    try:
        payload = verify_access_token(token)
        return payload.get("role") == "ADMIN"
    except JWTError:
        return False
import os
from datetime import datetime, timedelta

from jose import jwt, JWTError
from passlib.context import CryptContext


# -------------------------------------------------
# Config
# -------------------------------------------------

SECRET_KEY = os.getenv("SF_JWT_SECRET", "dev-secret-change")
ALGO = "HS256"
ACCESS_TOKEN_MINUTES = 60

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -------------------------------------------------
# Password Handling (bcrypt-safe)
# -------------------------------------------------

def hash_pw(password: str) -> str:
    # bcrypt max = 72 bytes
    password = password[:72]
    return pwd.hash(password)


def verify_pw(password: str, hashed: str) -> bool:
    password = password[:72]
    return pwd.verify(password, hashed)


# -------------------------------------------------
# JWT Handling
# -------------------------------------------------

def create_access(username: str) -> str:
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGO)


def decode_access(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
    except JWTError:
        return None
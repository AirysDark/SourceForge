
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(p): return pwd_context.hash(p)
def verify_password(p, h): return pwd_context.verify(p, h)

def create_token(data, expires):
    payload = data.copy()
    payload.update({"exp": datetime.utcnow() + expires})
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

def create_access(data):
    return create_token(data, timedelta(minutes=settings.ACCESS_TOKEN_MINUTES))

def create_refresh(data):
    return create_token(data, timedelta(days=settings.REFRESH_DAYS))

def verify_token(token):
    return jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])

from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional

from app.db.db import SessionLocal, User, init_db
from app.core.auth import hash_pw, verify_pw, create_access, decode_access

router = APIRouter(prefix="/api")

# Ensure DB tables exist
init_db()


# ------------------------
# Database Dependency
# ------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------------
# Request Models
# ------------------------
class AuthRequest(BaseModel):
    username: str
    password: str


# ------------------------
# Auth Helpers
# ------------------------
def get_current_user(
    authorization: Optional[str] = Header(None)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    token = authorization.split(" ")[1]
    payload = decode_access(token)

    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload["sub"]


# ------------------------
# Register
# ------------------------
@router.post("/auth/register")
def register(data: AuthRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter_by(username=data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(
        username=data.username,
        password=hash_pw(data.password)
    )

    db.add(user)
    db.commit()

    return {"ok": True}


# ------------------------
# Login
# ------------------------
@router.post("/auth/login")
def login(data: AuthRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=data.username).first()

    if not user or not verify_pw(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access(user.username)

    return {
        "access_token": token,
        "token_type": "bearer"
    }
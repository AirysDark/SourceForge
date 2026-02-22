# backend/app/api/auth/me.py

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional

from app.db.db import SessionLocal, User
from app.core.auth import decode_access

router = APIRouter()  # 🚀 NO PREFIX HERE


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    token = authorization.split(" ")[1]
    payload = decode_access(token)

    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter_by(username=payload["sub"]).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.get("/me")
def get_me(user: User = Depends(get_current_user)):
    return {
        "id": user.id,
        "username": user.username,
        "role": getattr(user, "role", "user")
    }
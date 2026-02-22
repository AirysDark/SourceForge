from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.db import SessionLocal, User
from app.core.auth import verify_pw, create_access

router = APIRouter()  # 🚀 NO PREFIX HERE


class LoginRequest(BaseModel):
    username: str
    password: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter_by(username=data.username).first()

    if not user or not verify_pw(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access(user.username)

    return {
        "access_token": token,
        "token_type": "bearer"
    }
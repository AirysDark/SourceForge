from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.db import SessionLocal, User
from app.core.auth import hash_pw

router = APIRouter()  # 🚀 NO PREFIX HERE


class RegisterRequest(BaseModel):
    username: str
    password: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):

    existing = db.query(User).filter_by(username=data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(
        username=data.username,
        password=hash_pw(data.password)
    )

    db.add(user)
    db.commit()

    return {"message": "User created successfully"}
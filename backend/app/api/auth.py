from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from app.db.db import SessionLocal, User, init_db
from app.core.auth import hash_pw, verify_pw, create_access, decode_access

router = APIRouter()
init_db()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def get_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401)
    payload = decode_access(authorization.split(" ")[1])
    if not payload:
        raise HTTPException(status_code=401)
    return payload["sub"]

@router.post("/auth/register")
def register(data: dict, db: Session = Depends(get_db)):
    if db.query(User).filter_by(username=data["username"]).first():
        raise HTTPException(status_code=400)
    u = User(username=data["username"], password=hash_pw(data["password"]))
    db.add(u); db.commit()
    return {"ok": True}

@router.post("/auth/login")
def login(data: dict, db: Session = Depends(get_db)):
    u = db.query(User).filter_by(username=data["username"]).first()
    if not u or not verify_pw(data["password"], u.password):
        raise HTTPException(status_code=401)
    return {"access_token": create_access(u.username)}

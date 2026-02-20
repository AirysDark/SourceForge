
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.models.system_state import SystemState
from app.models.audit import AuditLog
from app.core.security import hash_password, verify_password, create_access, create_refresh, verify_token
from app.middleware.rate_limit import limiter

router = APIRouter()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/bootstrap")
def bootstrap(data: dict, db: Session = Depends(get_db)):
    state = db.query(SystemState).first()
    if state and state.initialized:
        raise HTTPException(400, "Already initialized")
    user = User(username=data["username"], password_hash=hash_password(data["password"]), role="admin")
    db.add(user)
    db.add(SystemState(initialized=True))
    db.add(AuditLog(action="bootstrap", actor=data["username"]))
    db.commit()
    return {"status": "initialized"}

@router.post("/login")
@limiter.limit("5/minute")
def login(data: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data["username"]).first()
    if not user or not verify_password(data["password"], user.password_hash):
        raise HTTPException(401, "Invalid credentials")
    access = create_access({"sub": user.username, "role": user.role})
    refresh = create_refresh({"sub": user.username})
    db.add(RefreshToken(user=user.username, token=refresh))
    db.add(AuditLog(action="login", actor=user.username))
    db.commit()
    return {"access_token": access, "refresh_token": refresh}

@router.post("/refresh")
def refresh(data: dict, db: Session = Depends(get_db)):
    payload = verify_token(data["refresh_token"])
    token = db.query(RefreshToken).filter(RefreshToken.token == data["refresh_token"], RefreshToken.revoked == False).first()
    if not token: raise HTTPException(401, "Revoked")
    return {"access_token": create_access({"sub": payload["sub"]})}

@router.post("/logout")
def logout(data: dict, db: Session = Depends(get_db)):
    token = db.query(RefreshToken).filter(RefreshToken.token == data["refresh_token"]).first()
    if token: token.revoked = True
    db.commit()
    return {"status": "revoked"}

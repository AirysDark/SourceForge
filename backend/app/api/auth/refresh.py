from fastapi import APIRouter, HTTPException, Header
from typing import Optional

from app.core.auth import decode_access, create_access

router = APIRouter()  # 🚀 NO PREFIX HERE


@router.post("/refresh")
def refresh_token(authorization: Optional[str] = Header(None)):

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.split(" ")[1]
    payload = decode_access(token)

    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    new_token = create_access(payload["sub"])

    return {
        "access_token": new_token,
        "token_type": "bearer"
    }

from fastapi import Depends, HTTPException, status
from app.core.deps import get_current_user

def require_role(role: str):
    def checker(user=Depends(get_current_user)):
        if user.get("role") != role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        return user
    return checker

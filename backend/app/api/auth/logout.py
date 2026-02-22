from fastapi import APIRouter

router = APIRouter()  # 🚀 NO PREFIX HERE


@router.post("/logout")
def logout():
    return {"message": "Logout successful (client should discard token)"}
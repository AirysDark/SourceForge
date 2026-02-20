from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import json

app = FastAPI()
CONFIG_PATH = "backend/data/config.json"
USERS_PATH = "backend/data/users.json"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def is_initialized():
    return os.path.exists(CONFIG_PATH)

@app.middleware("http")
async def first_run_check(request: Request, call_next):
    if not is_initialized() and not request.url.path.startswith("/setup"):
        return JSONResponse({"error": "System not initialized. Visit /setup"}, status_code=503)
    return await call_next(request)

@app.get("/setup/status")
def setup_status():
    return {"initialized": is_initialized()}

@app.post("/setup")
def run_setup(payload: dict):
    if is_initialized():
        raise HTTPException(status_code=400, detail="Already initialized")

    config = {
        "base_url": payload.get("base_url"),
        "storage_type": payload.get("storage_type"),
        "jwt_secret": payload.get("jwt_secret"),
        "region": payload.get("region")
    }

    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

    admin = {
        "username": payload.get("admin_user"),
        "password": payload.get("admin_pass"),  # (hash in production)
        "role": "admin"
    }

    with open(USERS_PATH, "w") as f:
        json.dump([admin], f, indent=2)

    return {"status": "initialized"}

@app.get("/health")
def health():
    return {"status": "ok"}

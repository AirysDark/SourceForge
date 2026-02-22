# backend/app/main.py

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.db.db import init_db

from app.api.auth import router as auth_router
from app.api import repos
from app.api import git
from app.api import git_http
from app.api import pr_api
from app.api import git_api
from app.api import metrics_api
from app.api import org_api
from app.api import replication_api
from app.api import storage_api
from app.api import ref_api
from app.api import conflict_api
from app.api import crdt_api
from app.api import gc_api


# ============================================
# App Instance
# ============================================

app = FastAPI(
    title="SourceForge API",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)


# ============================================
# Startup (CREATE TABLES HERE)
# ============================================

@app.on_event("startup")
def startup():
    init_db()


# ============================================
# CORS
# ============================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# API Router Group (Single /api Prefix)
# ============================================

api = APIRouter(prefix="/api")

# Auth
api.include_router(auth_router)

# Repo / PR
api.include_router(repos.router)
api.include_router(pr_api.router)

# Git Layer
api.include_router(git.router)
api.include_router(git_http.router)
api.include_router(git_api.router)

# System / Infra
api.include_router(metrics_api.router)
api.include_router(org_api.router)
api.include_router(replication_api.router)
api.include_router(storage_api.router)
api.include_router(ref_api.router)
api.include_router(conflict_api.router)
api.include_router(crdt_api.router)
api.include_router(gc_api.router)

# Register grouped router
app.include_router(api)


# ============================================
# Health
# ============================================

@app.get("/api/health")
def health():
    return {"status": "ok"}
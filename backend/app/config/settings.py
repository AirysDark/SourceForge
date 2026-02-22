# backend/app/config/settings.py

import os
from pathlib import Path


# ============================================
# Base Path
# ============================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


# ============================================
# Environment Mode
# ============================================

ENV = os.getenv("SF_ENV", "development")


# ============================================
# Redis
# ============================================

REDIS_URL = os.getenv(
    "SF_REDIS_URL",
    "redis://redis:6379/0"
)


# ============================================
# Database
# ============================================

DATABASE_URL = os.getenv(
    "SF_DATABASE_URL",
    f"sqlite:///{DATA_DIR / 'sourceforge.db'}"
)


# ============================================
# Storage Backend
# ============================================

STORAGE_BACKEND = os.getenv("SF_STORAGE_BACKEND", "local")

STORAGE_ROOT = os.getenv(
    "SF_STORAGE_ROOT",
    str(DATA_DIR / "repos")
)

Path(STORAGE_ROOT).mkdir(parents=True, exist_ok=True)


# ============================================
# JWT / Auth
# ============================================

JWT_SECRET = os.getenv("SF_JWT_SECRET", "dev-secret-change-me")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = int(os.getenv("SF_JWT_EXPIRE_MINUTES", "60"))


# ============================================
# Region / Replication
# ============================================

REGION_ID = os.getenv("SF_REGION_ID", "region-a")


# ============================================
# Debug
# ============================================

DEBUG = ENV == "development"
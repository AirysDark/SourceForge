from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import new API routers
try:
    from app.api import auth
except Exception:
    auth = None  # Allows boot even if auth temporarily missing

app = FastAPI(title="SourceForge API")

# CORS (Alpha-wide open)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers if available
if auth:
    app.include_router(auth.router)

# Health endpoint
@app.get("/api/health")
def health():
    return {"status": "ok"}

import logging
from fastapi import FastAPI, WebSocket
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from app.db.database import Base, engine
from app.routes import auth
from app.middleware.rate_limit import limiter
from app.core.security import verify_token
from app.models.audit import AuditLog
from app.db.database import SessionLocal
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sourceforge")

if settings.JWT_SECRET == "CHANGE_ME" and settings.ENV == "prod":
    raise RuntimeError("JWT secret not configured")

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.include_router(auth.router)

@app.exception_handler(Exception)
async def global_handler(request, exc):
    logger.error(str(exc))
    return JSONResponse(status_code=500, content={"detail": "Internal error"})

@app.websocket("/ws")
async def websocket(ws: WebSocket):
    token = ws.query_params.get("token")
    payload = verify_token(token)
    if payload.get("role") != "admin":
        await ws.close(code=1008)
        return
    await ws.accept()
    await ws.send_text("Authenticated WebSocket channel")

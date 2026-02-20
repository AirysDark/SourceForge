
import os

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sourceforge.db")
    JWT_SECRET = os.getenv("SF_JWT_SECRET", "CHANGE_ME")
    ENV = os.getenv("ENV", "dev")
    ACCESS_TOKEN_MINUTES = 30
    REFRESH_DAYS = 7

settings = Settings()

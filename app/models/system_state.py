
from sqlalchemy import Column, Integer, Boolean
from app.db.database import Base

class SystemState(Base):
    __tablename__ = "system_state"
    id = Column(Integer, primary_key=True)
    initialized = Column(Boolean, default=False)

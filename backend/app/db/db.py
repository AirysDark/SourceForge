import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

# ---------------------------------
# Database Configuration
# ---------------------------------

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://sourceforge:sourceforge@db:5432/sourceforge"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


# ---------------------------------
# User Model (for auth)
# ---------------------------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)


# ---------------------------------
# Pull Request Model
# ---------------------------------

class PullRequest(Base):
    __tablename__ = "pull_requests"

    id = Column(Integer, primary_key=True)
    repo_id = Column(Integer)
    title = Column(String)
    status = Column(String, default="open")  # open|train|merged|failed|rebasing


# ---------------------------------
# Merge Train Model
# ---------------------------------

class MergeTrain(Base):
    __tablename__ = "merge_train"

    id = Column(Integer, primary_key=True)
    repo_id = Column(Integer)
    pr_id = Column(Integer)
    position = Column(Integer)
    speculative_ok = Column(Boolean, default=False)
    needs_rebase = Column(Boolean, default=False)


# ---------------------------------
# Initialize DB
# ---------------------------------

def init_db():
    Base.metadata.create_all(bind=engine)
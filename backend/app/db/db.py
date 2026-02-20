from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///./sf.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class PullRequest(Base):
    __tablename__ = "pull_requests"
    id = Column(Integer, primary_key=True)
    repo_id = Column(Integer)
    title = Column(String)
    status = Column(String, default="open")  # open|train|merged|failed|rebasing

class MergeTrain(Base):
    __tablename__ = "merge_train"
    id = Column(Integer, primary_key=True)
    repo_id = Column(Integer)
    pr_id = Column(Integer)
    position = Column(Integer)
    speculative_ok = Column(Boolean, default=False)
    needs_rebase = Column(Boolean, default=False)

def init_db():
    Base.metadata.create_all(engine)

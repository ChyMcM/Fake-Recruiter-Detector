import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, JSON
from datetime import datetime

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://recruiter_user:recruiter_pass@localhost:5432/recruiter_db"
)

# Create engine
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


class AnalysisLog(Base):
    """Model for storing recruiter message analysis logs."""
    __tablename__ = "analysis_logs"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    message = Column(Text, nullable=False)
    score = Column(Integer, nullable=False)
    level = Column(String(50), nullable=False)
    flags = Column(JSON, nullable=True)  # List of matched flags
    highlights = Column(JSON, nullable=True)  # List of highlighted phrases
    ai_used = Column(Boolean, default=False)
    ai_score = Column(Float, nullable=True)
    ai_summary = Column(Text, nullable=True)
    confidence_score = Column(Integer, nullable=True)
    confidence_level = Column(String(50), nullable=True)
    confidence_explanation = Column(Text, nullable=True)
    confidence_factors = Column(JSON, nullable=True)

    def __repr__(self):
        return f"<AnalysisLog(id={self.id}, score={self.score}, level={self.level}, created_at={self.created_at})>"


def get_db():
    """Dependency for getting database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables initialized")

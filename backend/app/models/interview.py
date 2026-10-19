import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from backend.app.database import Base

class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    role = Column(String(100), default="Software Development Engineer")
    target_company = Column(String(100), default="General / Product Company")
    interview_mode = Column(String(50), default="Technical")  # Technical, HR, Aptitude, Project
    overall_score = Column(Float, nullable=True)  # Out of 100
    summary_report = Column(Text, nullable=True)
    status = Column(String(50), default="in_progress")  # in_progress, completed
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="interview_sessions")
    exchanges = relationship("InterviewExchange", back_populates="session", cascade="all, delete-orphan", order_by="InterviewExchange.round_number")

class InterviewExchange(Base):
    __tablename__ = "interview_exchanges"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey("interview_sessions.id", ondelete="CASCADE"), index=True, nullable=False)
    round_number = Column(Integer, nullable=False)
    question = Column(Text, nullable=False)
    user_answer = Column(Text, nullable=True)
    
    # Rubric Scores (0-10)
    clarity_score = Column(Float, nullable=True)
    correctness_score = Column(Float, nullable=True)
    communication_score = Column(Float, nullable=True)
    
    feedback = Column(Text, nullable=True)
    key_improvements = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("InterviewSession", back_populates="exchanges")

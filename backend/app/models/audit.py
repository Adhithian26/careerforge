import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Integer, Float, DateTime, Date, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from backend.app.database import Base

class WeeklyReport(Base):
    __tablename__ = "weekly_reports"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    
    week_start_date = Column(Date, nullable=False)
    week_end_date = Column(Date, nullable=False)
    
    # Quantitative verified metrics
    planned_tasks_count = Column(Integer, default=0)
    completed_tasks_count = Column(Integer, default=0)
    completion_rate_percentage = Column(Float, default=0.0)
    
    coding_problems_solved = Column(Integer, default=0)
    sql_exercises_completed = Column(Integer, default=0)
    assessments_completed = Column(Integer, default=0)
    average_assessment_score = Column(Float, default=0.0)
    applications_submitted = Column(Integer, default=0)
    interviews_completed = Column(Integer, default=0)
    
    # Qualitative insights (actual recorded data)
    key_weaknesses = Column(JSON, default=list)  # Top topics with lowest measured proficiency
    top_strengths = Column(JSON, default=list)
    next_week_priorities = Column(JSON, default=list)  # 3 distinct priorities
    
    ai_coach_summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="weekly_reports")

class ModelUsageAudit(Base):
    __tablename__ = "model_usage_audits"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=True)
    agent_name = Column(String(100), nullable=False)
    provider = Column(String(50), default="gemini")
    model_name = Column(String(100), default="gemini-2.5-flash")
    prompt_tokens = Column(Integer, default=0)
    completion_tokens = Column(Integer, default=0)
    status = Column(String(50), default="success")  # success, error, quota_exceeded
    error_details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

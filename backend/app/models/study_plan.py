import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Integer, Float, DateTime, Date, ForeignKey, Text, JSON, Boolean
from sqlalchemy.orm import relationship
from backend.app.database import Base

class StudyPlan(Base):
    __tablename__ = "study_plans"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    title = Column(String(255), default="Adaptive Weekly Preparation Plan")
    start_date = Column(Date, default=date.today)
    end_date = Column(Date, nullable=False)
    daily_allocated_hours = Column(Float, default=4.0)
    focus_objective = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="study_plans")
    tasks = relationship("StudyTask", back_populates="plan", cascade="all, delete-orphan", order_by="StudyTask.scheduled_date")

class StudyTask(Base):
    __tablename__ = "study_tasks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    plan_id = Column(String(36), ForeignKey("study_plans.id", ondelete="CASCADE"), index=True, nullable=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    
    scheduled_date = Column(Date, default=date.today, index=True)
    title = Column(String(255), nullable=False)
    topic = Column(String(100), nullable=False)  # DSA, Python, SQL, Aptitude, Core CS, Projects, Applications
    duration_minutes = Column(Integer, default=60)
    priority = Column(String(50), default="High")  # Urgent, High, Medium, Low
    
    # Status: pending, in_progress, completed, skipped, rescheduled
    status = Column(String(50), default="pending", index=True)
    
    notes = Column(Text, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    plan = relationship("StudyPlan", back_populates="tasks")
    user = relationship("User", back_populates="study_tasks")
    study_sessions = relationship("StudySession", back_populates="task", cascade="all, delete-orphan")

class StudySession(Base):
    __tablename__ = "study_sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id = Column(String(36), ForeignKey("study_tasks.id", ondelete="CASCADE"), index=True, nullable=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    reflection_notes = Column(Text, nullable=True)
    recorded_at = Column(DateTime, default=datetime.utcnow)

    task = relationship("StudyTask", back_populates="study_sessions")

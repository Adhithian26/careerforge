import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    assessment_attempts = relationship("AssessmentAttempt", back_populates="user", cascade="all, delete-orphan")
    coding_submissions = relationship("CodingSubmission", back_populates="user", cascade="all, delete-orphan")
    sql_submissions = relationship("SqlSubmission", back_populates="user", cascade="all, delete-orphan")
    interview_sessions = relationship("InterviewSession", back_populates="user", cascade="all, delete-orphan")
    study_plans = relationship("StudyPlan", back_populates="user", cascade="all, delete-orphan")
    study_tasks = relationship("StudyTask", back_populates="user", cascade="all, delete-orphan")
    job_applications = relationship("JobApplication", back_populates="user", cascade="all, delete-orphan")
    weekly_reports = relationship("WeeklyReport", back_populates="user", cascade="all, delete-orphan")
    skill_metrics = relationship("UserSkillMetric", back_populates="user", cascade="all, delete-orphan")

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    degree = Column(String(255), default="B.Tech Artificial Intelligence and Data Science")
    graduation_year = Column(Integer, default=2027)
    daily_study_hours = Column(Integer, default=4)
    target_roles = Column(String(500), default="Software Development Engineer, Backend Developer, AI Engineer")
    preferred_companies = Column(String(500), default="Zoho, TCS, Amazon, Google, PayPal, Tech Mahindra")
    
    # Subjective Confidence (1-5)
    python_confidence = Column(Integer, default=3)
    sql_confidence = Column(Integer, default=3)
    dsa_confidence = Column(Integer, default=1)
    
    # Portfolio & Long-term goals
    existing_projects = Column(Text, default="RAG Chatbot, Facial Recognition Attendance System")
    career_goals = Column(Text, default="Gain 2–4 years industry experience, achieve financial stability, and subsequently pursue credentials for professor career.")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="profile")

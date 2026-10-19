import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from backend.app.database import Base

class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    topic = Column(String(100), index=True, nullable=False)  # Python, SQL, DSA, Aptitude, OOP, DBMS, OS, Networks
    subtopic = Column(String(100), nullable=True)
    difficulty = Column(String(50), default="Medium")  # Easy, Medium, Hard
    question_text = Column(Text, nullable=False)
    code_snippet = Column(Text, nullable=True)
    options = Column(JSON, nullable=False)  # List of strings: ["A", "B", "C", "D"]
    correct_option_index = Column(Integer, nullable=False)  # 0, 1, 2, 3
    explanation = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class AssessmentAttempt(Base):
    __tablename__ = "assessment_attempts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    topic = Column(String(100), index=True, nullable=False)
    total_questions = Column(Integer, nullable=False)
    correct_count = Column(Integer, nullable=False)
    score_percentage = Column(Float, nullable=False)
    time_spent_seconds = Column(Integer, default=0)
    answers_summary = Column(JSON, nullable=True)  # Detail of question_id, selected, is_correct
    completed_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="assessment_attempts")

class UserSkillMetric(Base):
    __tablename__ = "user_skill_metrics"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    topic = Column(String(100), index=True, nullable=False)
    measured_proficiency = Column(Float, default=0.0)  # Calculated score 0-100
    subjective_confidence = Column(Integer, default=1)  # 1-5 rating
    attempts_count = Column(Integer, default=0)
    total_questions_answered = Column(Integer, default=0)
    total_correct_answered = Column(Integer, default=0)
    weak_subtopics = Column(JSON, default=list)
    strong_subtopics = Column(JSON, default=list)
    last_assessed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="skill_metrics")

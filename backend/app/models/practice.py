import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, JSON, Boolean
from sqlalchemy.orm import relationship
from backend.app.database import Base

class CodingProblem(Base):
    __tablename__ = "coding_problems"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    slug = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    difficulty = Column(String(50), default="Medium")  # Easy, Medium, Hard
    category = Column(String(100), default="Arrays")  # Arrays, Strings, HashMaps, Trees, DP, etc.
    description = Column(Text, nullable=False)
    starter_code = Column(Text, nullable=False)
    function_name = Column(String(100), nullable=False)
    # Test cases: [{"input": [1, 2], "expected": 3, "is_sample": True}, ...]
    test_cases = Column(JSON, nullable=False)
    hints = Column(JSON, default=list)
    solution_approach = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class CodingSubmission(Base):
    __tablename__ = "coding_submissions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    problem_id = Column(String(36), ForeignKey("coding_problems.id", ondelete="CASCADE"), index=True, nullable=False)
    submitted_code = Column(Text, nullable=False)
    passed = Column(Boolean, default=False)
    passed_tests_count = Column(Integer, default=0)
    total_tests_count = Column(Integer, default=0)
    runtime_ms = Column(Float, default=0.0)
    error_message = Column(Text, nullable=True)
    test_results = Column(JSON, nullable=True)  # List of test outcome summaries without revealing hidden data
    submitted_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="coding_submissions")
    problem = relationship("CodingProblem")

class SqlProblem(Base):
    __tablename__ = "sql_problems"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    slug = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    difficulty = Column(String(50), default="Medium")  # Easy, Medium, Hard
    category = Column(String(100), default="JOINs")  # Aggregations, Window Functions, Subqueries, GROUP BY, etc.
    prompt = Column(Text, nullable=False)
    schema_info = Column(Text, nullable=False)
    expected_sql = Column(Text, nullable=False)
    hints = Column(JSON, default=list)
    explanation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class SqlSubmission(Base):
    __tablename__ = "sql_submissions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    problem_id = Column(String(36), ForeignKey("sql_problems.id", ondelete="CASCADE"), index=True, nullable=False)
    submitted_query = Column(Text, nullable=False)
    passed = Column(Boolean, default=False)
    execution_time_ms = Column(Float, default=0.0)
    row_count = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    submitted_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="sql_submissions")
    problem = relationship("SqlProblem")

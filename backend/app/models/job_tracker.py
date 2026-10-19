import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Integer, Float, DateTime, Date, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from backend.app.database import Base

class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    
    company = Column(String(255), index=True, nullable=False)
    role = Column(String(255), nullable=False)
    job_url = Column(String(1000), nullable=True)
    location = Column(String(255), default="Remote / Hybrid / On-site")
    salary_range = Column(String(100), nullable=True)
    eligibility_notes = Column(Text, nullable=True)
    
    # Status: saved, planned, applied, assessment, interview, offer, rejected, withdrawn
    status = Column(String(50), default="saved", index=True)
    
    application_date = Column(Date, nullable=True)
    deadline = Column(Date, nullable=True)
    follow_up_date = Column(Date, nullable=True)
    
    is_verified_opening = Column(Boolean, default=True)  # Clearly distinguish verified from AI suggestions
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="job_applications")

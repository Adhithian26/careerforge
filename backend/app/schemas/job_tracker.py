from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel

class JobApplicationCreate(BaseModel):
    company: str
    role: str
    job_url: Optional[str] = None
    location: Optional[str] = "Remote / Hybrid / On-site"
    salary_range: Optional[str] = None
    eligibility_notes: Optional[str] = None
    status: str = "saved"
    application_date: Optional[date] = None
    deadline: Optional[date] = None
    follow_up_date: Optional[date] = None
    notes: Optional[str] = None
    is_verified_opening: bool = True

class JobApplicationUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    job_url: Optional[str] = None
    location: Optional[str] = None
    salary_range: Optional[str] = None
    eligibility_notes: Optional[str] = None
    status: Optional[str] = None
    application_date: Optional[date] = None
    deadline: Optional[date] = None
    follow_up_date: Optional[date] = None
    notes: Optional[str] = None
    is_verified_opening: Optional[bool] = None

class JobApplicationResponse(BaseModel):
    id: str
    company: str
    role: str
    job_url: Optional[str] = None
    location: Optional[str] = None
    salary_range: Optional[str] = None
    eligibility_notes: Optional[str] = None
    status: str
    application_date: Optional[date] = None
    deadline: Optional[date] = None
    follow_up_date: Optional[date] = None
    is_verified_opening: bool
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class JobPipelineStats(BaseModel):
    total_saved: int
    total_planned: int
    total_applied: int
    total_assessment: int
    total_interview: int
    total_offer: int
    total_rejected: int
    total_withdrawn: int

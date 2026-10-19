from typing import List, Optional
from datetime import date, datetime
from pydantic import BaseModel

class StudyTaskCreate(BaseModel):
    title: str
    topic: str
    duration_minutes: int = 60
    priority: str = "High"
    scheduled_date: date
    notes: Optional[str] = None

class StudyTaskUpdate(BaseModel):
    title: Optional[str] = None
    topic: Optional[str] = None
    duration_minutes: Optional[int] = None
    priority: Optional[str] = None
    scheduled_date: Optional[date] = None
    status: Optional[str] = None  # pending, in_progress, completed, skipped, rescheduled
    notes: Optional[str] = None

class StudyTaskResponse(BaseModel):
    id: str
    plan_id: Optional[str] = None
    scheduled_date: date
    title: str
    topic: str
    duration_minutes: int
    priority: str
    status: str
    notes: Optional[str] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class RecordSessionRequest(BaseModel):
    task_id: Optional[str] = None
    duration_minutes: int
    reflection_notes: Optional[str] = None

class GeneratePlanRequest(BaseModel):
    daily_hours: float = 4.0
    start_date: Optional[date] = None
    focus_objective: Optional[str] = None

class StudyPlanResponse(BaseModel):
    id: str
    title: str
    start_date: date
    end_date: date
    daily_allocated_hours: float
    focus_objective: Optional[str] = None
    is_active: bool
    tasks: List[StudyTaskResponse] = []

    class Config:
        from_attributes = True

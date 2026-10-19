from typing import List, Optional
from datetime import date, datetime
from pydantic import BaseModel

class WeeklyReportResponse(BaseModel):
    id: str
    week_start_date: date
    week_end_date: date
    planned_tasks_count: int
    completed_tasks_count: int
    completion_rate_percentage: float
    coding_problems_solved: int
    sql_exercises_completed: int
    assessments_completed: int
    average_assessment_score: float
    applications_submitted: int
    interviews_completed: int
    key_weaknesses: List[str]
    top_strengths: List[str]
    next_week_priorities: List[str]
    ai_coach_summary: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class GenerateWeeklyReportRequest(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None

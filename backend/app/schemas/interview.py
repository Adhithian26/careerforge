from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class StartInterviewRequest(BaseModel):
    role: str = "Software Development Engineer"
    target_company: str = "General / Product Company"
    interview_mode: str = "Technical"  # Technical, HR, Aptitude, Project

class AnswerInterviewQuestionRequest(BaseModel):
    user_answer: str

class InterviewExchangeResponse(BaseModel):
    id: str
    round_number: int
    question: str
    user_answer: Optional[str] = None
    clarity_score: Optional[float] = None
    correctness_score: Optional[float] = None
    communication_score: Optional[float] = None
    feedback: Optional[str] = None
    key_improvements: List[str] = []

    class Config:
        from_attributes = True

class InterviewSessionDetailResponse(BaseModel):
    id: str
    role: str
    target_company: str
    interview_mode: str
    status: str
    overall_score: Optional[float] = None
    summary_report: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    exchanges: List[InterviewExchangeResponse] = []

    class Config:
        from_attributes = True

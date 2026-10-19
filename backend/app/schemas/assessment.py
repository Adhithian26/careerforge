from typing import List, Optional, Any, Dict
from datetime import datetime
from pydantic import BaseModel

class QuestionOption(BaseModel):
    id: int
    text: str

class AssessmentQuestionResponse(BaseModel):
    id: str
    topic: str
    subtopic: Optional[str] = None
    difficulty: str
    question_text: str
    code_snippet: Optional[str] = None
    options: List[str]
    # Note: correct_option_index is NOT sent during assessment taking to prevent cheating

    class Config:
        from_attributes = True

class QuestionAnswerSubmission(BaseModel):
    question_id: str
    selected_option_index: int

class SubmitAssessmentRequest(BaseModel):
    topic: str
    answers: List[QuestionAnswerSubmission]
    time_spent_seconds: int = 0

class AnswerResultDetail(BaseModel):
    question_id: str
    question_text: str
    selected_option_index: int
    correct_option_index: int
    is_correct: bool
    explanation: str

class AssessmentResultResponse(BaseModel):
    id: str
    topic: str
    total_questions: int
    correct_count: int
    score_percentage: float
    time_spent_seconds: int
    completed_at: datetime
    breakdown: List[AnswerResultDetail]
    updated_measured_proficiency: float
    recommendation: str

class SkillMetricResponse(BaseModel):
    topic: str
    measured_proficiency: float
    subjective_confidence: int
    attempts_count: int
    total_questions_answered: int
    total_correct_answered: int
    weak_subtopics: List[str]
    strong_subtopics: List[str]
    last_assessed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UpdateConfidenceRequest(BaseModel):
    topic: str
    confidence: int  # 1 to 5

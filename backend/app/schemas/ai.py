from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class CoachChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[Dict[str, str]]] = None
    context_topic: Optional[str] = None

class CoachChatResponse(BaseModel):
    reply: str
    suggested_actions: List[str] = []
    agent_name: str = "Career Coach"
    model_used: str = "gemini-2.5-flash"

class ResumeAnalyzeRequest(BaseModel):
    resume_text: str
    job_description: str
    target_role: Optional[str] = None

class ResumeAnalyzeResponse(BaseModel):
    match_percentage: float
    matched_skills: List[str]
    missing_critical_skills: List[str]
    missing_bonus_skills: List[str]
    recommended_bullet_points: List[str]
    action_items: List[str]

class ProjectInterviewPrepRequest(BaseModel):
    project_title: str
    project_description: str
    tech_stack: str

class ProjectInterviewPrepResponse(BaseModel):
    architecture_questions: List[str]
    deep_dive_questions: List[str]
    tradeoff_challenges: List[str]
    recommended_talking_points: List[str]

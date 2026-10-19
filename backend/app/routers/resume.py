from fastapi import APIRouter, Depends
from backend.app.schemas.ai import (
    ResumeAnalyzeRequest,
    ResumeAnalyzeResponse,
    ProjectInterviewPrepRequest,
    ProjectInterviewPrepResponse
)
from backend.app.services.resume_assistant import (
    analyze_resume_alignment,
    get_project_interview_prep
)
from backend.app.services.auth_service import get_current_user

router = APIRouter(prefix="/resume", tags=["Resume & Project Assistant"])

@router.post("/analyze", response_model=ResumeAnalyzeResponse)
def analyze_resume(payload: ResumeAnalyzeRequest):
    """Analyzes resume text against target job description and identifies missing keywords."""
    return analyze_resume_alignment(
        resume_text=payload.resume_text,
        job_description=payload.job_description,
        target_role=payload.target_role or "Software Development Engineer"
    )

@router.post("/project-prep", response_model=ProjectInterviewPrepResponse)
def prepare_project_questions(payload: ProjectInterviewPrepRequest):
    """Generates probing architecture and tradeoff questions for the student's actual projects."""
    return get_project_interview_prep(payload.project_title)

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from backend.app.schemas.ai import (
    ResumeAnalyzeRequest,
    ResumeAnalyzeResponse,
    ProjectInterviewPrepRequest,
    ProjectInterviewPrepResponse,
    BulletEnhanceRequest,
    BulletEnhanceResponse
)
from backend.app.services.resume_assistant import (
    analyze_resume_alignment,
    get_project_interview_prep,
    enhance_resume_bullet
)
from backend.app.services.auth_service import get_current_user

router = APIRouter(prefix="/resume", tags=["Resume & Project Assistant"])

@router.post("/upload-pdf")
async def upload_resume_pdf(file: UploadFile = File(...)):
    """Extracts text content from an uploaded PDF, TXT, or Markdown resume document."""
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded.")
    contents = await file.read()
    filename = file.filename or "resume.pdf"

    if filename.lower().endswith((".txt", ".md")):
        extracted = contents.decode("utf-8", errors="ignore")
    else:
        from backend.app.services.pdf_extractor import extract_text_from_pdf_bytes
        extracted = extract_text_from_pdf_bytes(contents)

    words = extracted.split()
    return {
        "filename": filename,
        "extracted_text": extracted,
        "word_count": len(words),
        "message": f"Successfully extracted {len(words)} words from {filename}"
    }

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
    return get_project_interview_prep(
        project_title=payload.project_title,
        project_description=payload.project_description,
        tech_stack=payload.tech_stack
    )

@router.post("/enhance-bullet", response_model=BulletEnhanceResponse)
def enhance_bullet(payload: BulletEnhanceRequest):
    """Transforms raw bullet points into Google XYZ formula metric-driven statements."""
    return enhance_resume_bullet(
        raw_bullet=payload.raw_bullet,
        project_context=payload.project_context,
        target_role=payload.target_role
    )

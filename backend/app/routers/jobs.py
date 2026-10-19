from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.models.job_tracker import JobApplication
from backend.app.schemas.job_tracker import (
    JobApplicationCreate,
    JobApplicationUpdate,
    JobApplicationResponse,
    JobPipelineStats
)
from backend.app.mcp.tools import APPROVED_JOB_SOURCES, tool_search_approved_jobs
from backend.app.services.auth_service import get_current_user

router = APIRouter(prefix="/jobs", tags=["Job Application Tracker"])

@router.get("", response_model=List[JobApplicationResponse])
def get_job_applications(
    status_filter: Optional[str] = Query(None, alias="status"),
    search: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves the student's job applications with filtering and search."""
    query = db.query(JobApplication).filter(JobApplication.user_id == current_user.id)
    if status_filter:
        query = query.filter(JobApplication.status == status_filter)
    if search:
        query = query.filter(
            (JobApplication.company.ilike(f"%{search}%")) |
            (JobApplication.role.ilike(f"%{search}%"))
        )
    return query.order_by(JobApplication.updated_at.desc()).all()

@router.get("/pipeline-stats", response_model=JobPipelineStats)
def get_pipeline_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Returns application counts grouped by pipeline stage."""
    apps = db.query(JobApplication).filter(JobApplication.user_id == current_user.id).all()
    return JobPipelineStats(
        total_saved=sum(1 for a in apps if a.status == "saved"),
        total_planned=sum(1 for a in apps if a.status == "planned"),
        total_applied=sum(1 for a in apps if a.status == "applied"),
        total_assessment=sum(1 for a in apps if a.status == "assessment"),
        total_interview=sum(1 for a in apps if a.status == "interview"),
        total_offer=sum(1 for a in apps if a.status == "offer"),
        total_rejected=sum(1 for a in apps if a.status == "rejected"),
        total_withdrawn=sum(1 for a in apps if a.status == "withdrawn")
    )

@router.post("", response_model=JobApplicationResponse)
def create_job_application(
    payload: JobApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Creates a new job application record."""
    new_app = JobApplication(
        user_id=current_user.id,
        company=payload.company,
        role=payload.role,
        job_url=payload.job_url,
        location=payload.location,
        salary_range=payload.salary_range,
        eligibility_notes=payload.eligibility_notes,
        status=payload.status,
        application_date=payload.application_date,
        deadline=payload.deadline,
        follow_up_date=payload.follow_up_date,
        notes=payload.notes,
        is_verified_opening=payload.is_verified_opening
    )
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return new_app

@router.put("/{app_id}", response_model=JobApplicationResponse)
def update_job_application(
    app_id: str,
    payload: JobApplicationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Updates an existing job application status or dates."""
    app_record = db.query(JobApplication).filter(
        JobApplication.id == app_id,
        JobApplication.user_id == current_user.id
    ).first()

    if not app_record:
        raise HTTPException(status_code=404, detail="Job application not found.")

    update_dict = payload.model_dump(exclude_unset=True)
    for field, val in update_dict.items():
        setattr(app_record, field, val)

    db.commit()
    db.refresh(app_record)
    return app_record

@router.delete("/{app_id}")
def delete_job_application(
    app_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deletes a job application record."""
    app_record = db.query(JobApplication).filter(
        JobApplication.id == app_id,
        JobApplication.user_id == current_user.id
    ).first()

    if not app_record:
        raise HTTPException(status_code=404, detail="Job application not found.")

    db.delete(app_record)
    db.commit()
    return {"message": "Job application deleted successfully."}

@router.get("/approved-sources")
def get_approved_sources(query: Optional[str] = None):
    """Searches official career portals from approved target employers."""
    if query:
        return tool_search_approved_jobs(query=query)
    return APPROVED_JOB_SOURCES

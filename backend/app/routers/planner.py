from datetime import date, datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.models.study_plan import StudyPlan, StudyTask, StudySession
from backend.app.schemas.study_plan import (
    StudyPlanResponse,
    StudyTaskResponse,
    StudyTaskCreate,
    StudyTaskUpdate,
    RecordSessionRequest,
    GeneratePlanRequest
)
from backend.app.services.study_planner import generate_weekly_study_plan
from backend.app.services.auth_service import get_current_user

router = APIRouter(prefix="/planner", tags=["Study Planner"])

@router.get("/active-plan", response_model=Optional[StudyPlanResponse])
def get_active_study_plan(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves the student's currently active study plan, or auto-generates if none exists."""
    plan = db.query(StudyPlan).filter(
        StudyPlan.user_id == current_user.id,
        StudyPlan.is_active == True
    ).first()

    if not plan:
        plan = generate_weekly_study_plan(db=db, user_id=current_user.id)

    return plan

@router.post("/generate", response_model=StudyPlanResponse)
def generate_new_plan(
    payload: GeneratePlanRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generates a fresh adaptive weekly study plan with custom hours or start date."""
    plan = generate_weekly_study_plan(
        db=db,
        user_id=current_user.id,
        start_date=payload.start_date,
        daily_hours=payload.daily_hours,
        focus_objective=payload.focus_objective
    )
    return plan

@router.get("/tasks", response_model=List[StudyTaskResponse])
def get_study_tasks(
    date_filter: Optional[date] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves tasks, optionally filtered by scheduled date."""
    query = db.query(StudyTask).filter(StudyTask.user_id == current_user.id)
    if date_filter:
        query = query.filter(StudyTask.scheduled_date == date_filter)
    return query.order_by(StudyTask.scheduled_date.asc(), StudyTask.duration_minutes.desc()).all()

@router.post("/tasks", response_model=StudyTaskResponse)
def create_custom_task(
    payload: StudyTaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Allows user to add a custom study task to their calendar."""
    task = StudyTask(
        user_id=current_user.id,
        scheduled_date=payload.scheduled_date,
        title=payload.title,
        topic=payload.topic,
        duration_minutes=payload.duration_minutes,
        priority=payload.priority,
        status="pending",
        notes=payload.notes
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.patch("/tasks/{task_id}", response_model=StudyTaskResponse)
def update_task_status(
    task_id: str,
    payload: StudyTaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Updates task status (completed, skipped, rescheduled) and priority/notes."""
    task = db.query(StudyTask).filter(
        StudyTask.id == task_id,
        StudyTask.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Study task not found.")

    update_dict = payload.model_dump(exclude_unset=True)
    for field, val in update_dict.items():
        setattr(task, field, val)

    if payload.status == "completed" and not task.completed_at:
        task.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(task)
    return task

@router.post("/record-session")
def record_study_session(
    payload: RecordSessionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Records real time spent in minutes on a study session."""
    session = StudySession(
        user_id=current_user.id,
        task_id=payload.task_id,
        duration_minutes=payload.duration_minutes,
        reflection_notes=payload.reflection_notes,
        recorded_at=datetime.utcnow()
    )
    db.add(session)

    if payload.task_id:
        task = db.query(StudyTask).filter(StudyTask.id == payload.task_id, StudyTask.user_id == current_user.id).first()
        if task:
            task.status = "completed"
            task.completed_at = datetime.utcnow()

    db.commit()
    return {"message": f"Recorded {payload.duration_minutes} minutes study session."}

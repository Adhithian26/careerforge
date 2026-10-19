from datetime import date, datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.models.audit import WeeklyReport
from backend.app.schemas.weekly import WeeklyReportResponse, GenerateWeeklyReportRequest
from backend.app.mcp.tools import tool_generate_weekly_summary
from backend.app.services.auth_service import get_current_user

router = APIRouter(prefix="/weekly", tags=["Weekly Review"])

@router.get("/latest", response_model=Optional[WeeklyReportResponse])
def get_latest_weekly_report(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves the most recently generated weekly progress report."""
    report = db.query(WeeklyReport).filter(
        WeeklyReport.user_id == current_user.id
    ).order_by(WeeklyReport.created_at.desc()).first()

    if not report:
        # Generate one from verified metrics
        report = generate_report_for_user(current_user.id, db)

    return report

@router.post("/generate", response_model=WeeklyReportResponse)
def trigger_weekly_report_generation(
    payload: GenerateWeeklyReportRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Synthesizes verified weekly metrics into a persisted weekly review report."""
    report = generate_report_for_user(
        user_id=current_user.id,
        db=db,
        start_date=payload.start_date,
        end_date=payload.end_date
    )
    return report

def generate_report_for_user(user_id: str, db: Session, start_date=None, end_date=None) -> WeeklyReport:
    summary_data = tool_generate_weekly_summary(user_id=user_id)
    
    start_d = start_date or (date.today() - timedelta(days=6))
    end_d = end_date or date.today()

    report = WeeklyReport(
        user_id=user_id,
        week_start_date=start_d,
        week_end_date=end_d,
        planned_tasks_count=summary_data.get("tasks_planned", 0),
        completed_tasks_count=summary_data.get("tasks_completed", 0),
        completion_rate_percentage=summary_data.get("completion_rate_percentage", 0.0),
        coding_problems_solved=summary_data.get("coding_problems_solved", 0),
        sql_exercises_completed=summary_data.get("sql_exercises_completed", 0),
        assessments_completed=summary_data.get("assessments_completed", 0),
        average_assessment_score=summary_data.get("average_assessment_score", 0.0),
        applications_submitted=summary_data.get("verified_applications_count", 0),
        interviews_completed=0,
        key_weaknesses=summary_data.get("identified_weaknesses", []),
        top_strengths=summary_data.get("strengths", []),
        next_week_priorities=summary_data.get("next_week_priorities", []),
        ai_coach_summary=(
            f"Weekly Performance Synthesis: {summary_data.get('tasks_completed', 0)} of {summary_data.get('tasks_planned', 0)} tasks completed "
            f"({summary_data.get('completion_rate_percentage', 0.0)}% completion rate). "
            f"Solved {summary_data.get('coding_problems_solved', 0)} coding exercises and {summary_data.get('sql_exercises_completed', 0)} SQL challenges. "
            f"DSA remains the critical growth area."
        )
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

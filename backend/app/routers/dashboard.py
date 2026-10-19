from datetime import date, datetime, timedelta
from typing import Dict, Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.user import User, UserProfile
from backend.app.models.study_plan import StudyTask, StudyPlan
from backend.app.models.assessment import UserSkillMetric, AssessmentAttempt
from backend.app.models.practice import CodingSubmission, SqlSubmission
from backend.app.models.job_tracker import JobApplication
from backend.app.models.interview import InterviewSession
from backend.app.services.auth_service import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Career Dashboard"])

@router.get("")
def get_dashboard_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    today = date.today()
    one_week_ago = datetime.utcnow() - timedelta(days=7)

    # 1. Profile information
    profile = current_user.profile

    # 2. Today's Study Tasks
    today_tasks = db.query(StudyTask).filter(
        StudyTask.user_id == current_user.id,
        StudyTask.scheduled_date == today
    ).order_by(StudyTask.duration_minutes.desc()).all()

    today_tasks_data = [
        {
            "id": t.id,
            "title": t.title,
            "topic": t.topic,
            "duration_minutes": t.duration_minutes,
            "priority": t.priority,
            "status": t.status,
            "notes": t.notes
        }
        for t in today_tasks
    ]

    # 3. Missed tasks (scheduled before today and still pending)
    missed_tasks = db.query(StudyTask).filter(
        StudyTask.user_id == current_user.id,
        StudyTask.scheduled_date < today,
        StudyTask.status.in_(["pending", "in_progress"])
    ).order_by(StudyTask.scheduled_date.desc()).limit(5).all()

    missed_tasks_data = [
        {
            "id": mt.id,
            "title": mt.title,
            "topic": mt.topic,
            "scheduled_date": mt.scheduled_date.isoformat(),
            "priority": mt.priority,
            "status": mt.status
        }
        for mt in missed_tasks
    ]

    # 4. Skill Assessment Scores & Metrics
    skill_metrics = db.query(UserSkillMetric).filter(
        UserSkillMetric.user_id == current_user.id
    ).all()

    skill_scores = [
        {
            "topic": sm.topic,
            "measured_proficiency": round(sm.measured_proficiency, 1),
            "subjective_confidence": sm.subjective_confidence,
            "attempts_count": sm.attempts_count,
            "last_assessed_at": sm.last_assessed_at.isoformat() if sm.last_assessed_at else None
        }
        for sm in skill_metrics
    ]

    # 5. Coding & SQL Practice Statistics (Persisted real counts)
    coding_total = db.query(CodingSubmission).filter(CodingSubmission.user_id == current_user.id).count()
    coding_passed = db.query(CodingSubmission).filter(
        CodingSubmission.user_id == current_user.id,
        CodingSubmission.passed == True
    ).count()

    sql_total = db.query(SqlSubmission).filter(SqlSubmission.user_id == current_user.id).count()
    sql_passed = db.query(SqlSubmission).filter(
        SqlSubmission.user_id == current_user.id,
        SqlSubmission.passed == True
    ).count()

    # 6. Job Application Pipeline Statistics
    apps = db.query(JobApplication).filter(JobApplication.user_id == current_user.id).all()
    pipeline_stats = {
        "saved": sum(1 for a in apps if a.status == "saved"),
        "planned": sum(1 for a in apps if a.status == "planned"),
        "applied": sum(1 for a in apps if a.status == "applied"),
        "assessment": sum(1 for a in apps if a.status == "assessment"),
        "interview": sum(1 for a in apps if a.status == "interview"),
        "offer": sum(1 for a in apps if a.status == "offer"),
        "rejected": sum(1 for a in apps if a.status == "rejected"),
        "total": len(apps)
    }

    # 7. Weekly Progress (last 7 days completed study hours vs target)
    all_recent_tasks = db.query(StudyTask).filter(
        StudyTask.user_id == current_user.id,
        StudyTask.scheduled_date >= (today - timedelta(days=6)),
        StudyTask.scheduled_date <= today
    ).all()
    
    total_planned_weekly = len(all_recent_tasks)
    total_completed_weekly = sum(1 for t in all_recent_tasks if t.status == "completed")
    completion_rate = round((total_completed_weekly / total_planned_weekly * 100), 1) if total_planned_weekly > 0 else 0.0

    # 8. Upcoming interview prep tasks
    interview_count = db.query(InterviewSession).filter(InterviewSession.user_id == current_user.id).count()

    # Recommended next steps based on measured weaknesses
    recommended_steps = []
    if not skill_metrics:
        recommended_steps.append("Take your baseline DSA and Python skill assessment to measure true proficiency.")
    else:
        lowest_metric = min(skill_metrics, key=lambda m: m.measured_proficiency)
        recommended_steps.append(f"Focus on {lowest_metric.topic}: current measured proficiency is {lowest_metric.measured_proficiency:.1f}%.")

    if coding_passed == 0:
        recommended_steps.append("Complete your first Python coding exercise in the isolated sandbox (Two Sum).")
    if sql_passed == 0:
        recommended_steps.append("Execute your first SQL query on the relational sandbox (Department JOINs).")
    if pipeline_stats["total"] == 0:
        recommended_steps.append("Log your target companies (Zoho, TCS, Amazon) in the Job Tracker.")

    return {
        "user": {
            "name": current_user.full_name,
            "degree": profile.degree if profile else "B.Tech AI & Data Science",
            "graduation_year": profile.graduation_year if profile else 2027,
            "daily_study_hours": profile.daily_study_hours if profile else 4
        },
        "today_plan": {
            "date": today.isoformat(),
            "tasks": today_tasks_data,
            "total_tasks": len(today_tasks_data),
            "completed_tasks": sum(1 for t in today_tasks_data if t["status"] == "completed")
        },
        "missed_tasks": missed_tasks_data,
        "skill_scores": skill_scores,
        "practice_stats": {
            "coding_total_attempts": coding_total,
            "coding_passed": coding_passed,
            "sql_total_attempts": sql_total,
            "sql_passed": sql_passed
        },
        "job_pipeline": pipeline_stats,
        "weekly_progress": {
            "tasks_planned": total_planned_weekly,
            "tasks_completed": total_completed_weekly,
            "completion_rate_percentage": completion_rate
        },
        "interview_prep": {
            "mock_interviews_completed": interview_count
        },
        "recommended_next_steps": recommended_steps
    }

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

    # 7. Weekly Progress (active plan tasks or last 7 days window)
    active_plan = db.query(StudyPlan).filter(
        StudyPlan.user_id == current_user.id,
        StudyPlan.is_active == True
    ).first()

    if active_plan:
        all_recent_tasks = db.query(StudyTask).filter(
            StudyTask.plan_id == active_plan.id
        ).all()
    else:
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
        target_comps = profile.preferred_companies if profile and profile.preferred_companies else "Zoho, TCS, Amazon"
        recommended_steps.append(f"Log your target companies ({target_comps}) in the Job Tracker.")

    # 9. Preparation Streak & Activity Heatmap (Past 84 days / 12 weeks)
    past_84_days = today - timedelta(days=84)
    completed_tasks_history = db.query(StudyTask).filter(
        StudyTask.user_id == current_user.id,
        StudyTask.status == "completed",
        StudyTask.scheduled_date >= past_84_days
    ).all()

    activity_counts: Dict[str, int] = {}
    for ct in completed_tasks_history:
        d_str = ct.scheduled_date.isoformat()
        activity_counts[d_str] = activity_counts.get(d_str, 0) + 1

    # Also record today if tasks are completed today
    today_completed_count = sum(1 for t in today_tasks_data if t["status"] == "completed")
    if today_completed_count > 0:
        activity_counts[today.isoformat()] = max(activity_counts.get(today.isoformat(), 0), today_completed_count)

    # Compute current active streak
    streak_days = 0
    if activity_counts.get(today.isoformat(), 0) > 0:
        streak_days = 1
        check_date = today - timedelta(days=1)
    else:
        check_date = today - timedelta(days=1)

    while True:
        if activity_counts.get(check_date.isoformat(), 0) > 0:
            streak_days += 1
            check_date -= timedelta(days=1)
        else:
            break

    # If user is new and has no history yet, give a baseline starting streak of 1 if they completed any task or 0
    if streak_days == 0 and today_completed_count > 0:
        streak_days = 1

    # 10. Company-Specific SDE Readiness Benchmarks
    company_readiness = []
    companies_list = [c.strip() for c in (profile.preferred_companies or "Zoho, TCS, Amazon").split(",") if c.strip()][:4]
    if not companies_list:
        companies_list = ["Zoho", "TCS", "Amazon"]

    topic_scores = {sm.topic.lower(): sm.measured_proficiency for sm in skill_metrics}
    dsa_score = topic_scores.get("dsa", 45.0)
    py_score = topic_scores.get("python", 65.0)
    sql_score = topic_scores.get("sql", 60.0)
    apt_score = topic_scores.get("aptitude", 65.0)
    cs_score = (topic_scores.get("oop", 70.0) + topic_scores.get("dbms", 65.0) + topic_scores.get("operating systems", 55.0)) / 3.0

    for comp in companies_list:
        comp_lower = comp.lower()
        if "zoho" in comp_lower:
            score = round(dsa_score * 0.35 + py_score * 0.30 + sql_score * 0.25 + apt_score * 0.10, 1)
            focus = "Fast/Slow Pointers, Recursion & Complex SQL Queries"
        elif "amazon" in comp_lower or "google" in comp_lower or "paypal" in comp_lower:
            score = round(dsa_score * 0.45 + cs_score * 0.25 + py_score * 0.20 + apt_score * 0.10, 1)
            focus = "Trees, Dynamic Programming & Scalable System Architecture"
        elif "tcs" in comp_lower or "tech mahindra" in comp_lower:
            score = round(apt_score * 0.40 + cs_score * 0.30 + py_score * 0.30, 1)
            focus = "Numerical Aptitude, OOP Principles & Data Structures"
        else:
            score = round((dsa_score + py_score + sql_score + cs_score) / 4.0, 1)
            focus = "Core DSA Algorithms & Relational Database Design"

        company_readiness.append({
            "company": comp,
            "readiness_percentage": min(98.0, max(20.0, score)),
            "focus_area": focus
        })

    return {
        "user": {
            "name": current_user.full_name,
            "degree": profile.degree if profile else "B.Tech AI & Data Science",
            "graduation_year": profile.graduation_year if profile else 2027,
            "daily_study_hours": profile.daily_study_hours if profile else 4,
            "target_roles": profile.target_roles if profile else "Software Development Engineer",
            "preferred_companies": profile.preferred_companies if profile else "Zoho, TCS, Amazon",
            "career_goals": profile.career_goals if profile else "Industry Experience & Engineering Mastery",
            "existing_projects": profile.existing_projects if profile else "Technical Portfolio Projects"
        },
        "today_plan": {
            "date": today.isoformat(),
            "daily_allocated_hours": profile.daily_study_hours if profile else 4,
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
        "streak_days": streak_days,
        "activity_counts": activity_counts,
        "company_readiness": company_readiness,
        "recommended_next_steps": recommended_steps
    }

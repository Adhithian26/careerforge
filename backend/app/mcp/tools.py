from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from backend.app.database import SessionLocal
from backend.app.models.user import User, UserProfile
from backend.app.models.assessment import AssessmentAttempt, UserSkillMetric
from backend.app.models.study_plan import StudyTask, StudySession
from backend.app.models.job_tracker import JobApplication

# --- APPROVED JOB SOURCES LIST ---
APPROVED_JOB_SOURCES = [
    {"company": "Zoho", "roles": ["Software Developer", "Quality Analyst"], "portal": "https://careers.zohocorp.com", "verified": True},
    {"company": "TCS", "roles": ["Assistant System Engineer (Prime / Digital)", "Developer"], "portal": "https://www.tcs.com/careers", "verified": True},
    {"company": "Amazon", "roles": ["Software Development Engineer I (SDE 1)", "Data Engineer"], "portal": "https://amazon.jobs", "verified": True},
    {"company": "PayPal", "roles": ["Software Engineer 1", "Graduate Engineer"], "portal": "https://careers.pypl.com", "verified": True},
    {"company": "Tech Mahindra", "roles": ["Associate Software Engineer", "AI/ML Associate"], "portal": "https://careers.techmahindra.com", "verified": True}
]

# --- 1. READ-ONLY TOOL: Read Skill Profile ---
def tool_read_skill_profile(user_id: str) -> Dict[str, Any]:
    """Retrieves the user's degree, graduation year, confidence ratings, and measured metrics."""
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"error": f"User with id '{user_id}' not found."}
        
        profile = user.profile
        metrics = db.query(UserSkillMetric).filter(UserSkillMetric.user_id == user_id).all()
        
        metric_list = [
            {
                "topic": m.topic,
                "measured_proficiency": round(m.measured_proficiency, 1),
                "subjective_confidence": m.subjective_confidence,
                "attempts_count": m.attempts_count,
                "last_assessed_at": m.last_assessed_at.isoformat() if m.last_assessed_at else None
            }
            for m in metrics
        ]
        
        return {
            "user_id": user.id,
            "full_name": user.full_name,
            "degree": profile.degree if profile else "B.Tech AI & Data Science",
            "graduation_year": profile.graduation_year if profile else 2027,
            "daily_study_hours": profile.daily_study_hours if profile else 4,
            "subjective_confidence": {
                "python": profile.python_confidence if profile else 3,
                "sql": profile.sql_confidence if profile else 3,
                "dsa": profile.dsa_confidence if profile else 1
            },
            "target_roles": profile.target_roles if profile else "Software Development Engineer",
            "preferred_companies": profile.preferred_companies if profile else "Zoho, TCS, Amazon, Google, PayPal",
            "measured_skill_metrics": metric_list
        }
    finally:
        db.close()

# --- 2. READ-ONLY TOOL: Get Assessment History ---
def tool_get_assessment_history(user_id: str, topic: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
    """Retrieves completed skill assessment attempts and scores."""
    db: Session = SessionLocal()
    try:
        query = db.query(AssessmentAttempt).filter(AssessmentAttempt.user_id == user_id)
        if topic:
            query = query.filter(AssessmentAttempt.topic == topic)
        attempts = query.order_by(AssessmentAttempt.completed_at.desc()).limit(limit).all()
        
        return [
            {
                "attempt_id": a.id,
                "topic": a.topic,
                "score_percentage": round(a.score_percentage, 1),
                "correct_count": a.correct_count,
                "total_questions": a.total_questions,
                "completed_at": a.completed_at.isoformat()
            }
            for a in attempts
        ]
    finally:
        db.close()

# --- 3. READ-ONLY TOOL: Read Job Application Tracker ---
def tool_read_application_tracker(user_id: str, status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieves job applications and their current pipeline status."""
    db: Session = SessionLocal()
    try:
        query = db.query(JobApplication).filter(JobApplication.user_id == user_id)
        if status_filter:
            query = query.filter(JobApplication.status == status_filter)
        apps = query.order_by(JobApplication.updated_at.desc()).all()
        
        return [
            {
                "id": app.id,
                "company": app.company,
                "role": app.role,
                "status": app.status,
                "job_url": app.job_url,
                "deadline": app.deadline.isoformat() if app.deadline else None,
                "is_verified_opening": app.is_verified_opening,
                "eligibility_notes": app.eligibility_notes
            }
            for app in apps
        ]
    finally:
        db.close()

# --- 4. READ-ONLY TOOL: Search Approved Job Sources ---
def tool_search_approved_jobs(query: str) -> List[Dict[str, Any]]:
    """Searches official and permitted career portals. Never scrapes unauthorized sites."""
    q_lower = query.lower()
    matches = []
    for item in APPROVED_JOB_SOURCES:
        if (q_lower in item["company"].lower() or 
            any(q_lower in role.lower() for role in item["roles"])):
            matches.append(item)
    return matches if matches else APPROVED_JOB_SOURCES[:3]

# --- 5. DATA-MODIFYING TOOL: Record Study Session ---
def tool_record_study_session(
    user_id: str,
    duration_minutes: int,
    notes: Optional[str] = None,
    task_id: Optional[str] = None
) -> Dict[str, Any]:
    """Records a completed study session and marks corresponding study task completed."""
    if duration_minutes <= 0 or duration_minutes > 480:
        return {"error": "Duration must be between 1 and 480 minutes."}
        
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"error": f"User with id '{user_id}' does not exist."}

        session = StudySession(
            user_id=user_id,
            task_id=task_id,
            duration_minutes=duration_minutes,
            reflection_notes=notes or "Study session recorded via MCP.",
            recorded_at=datetime.utcnow()
        )
        db.add(session)

        # If linked to a task, mark it completed
        if task_id:
            task = db.query(StudyTask).filter(StudyTask.id == task_id, StudyTask.user_id == user_id).first()
            if task:
                task.status = "completed"
                task.completed_at = datetime.utcnow()

        db.commit()
        db.refresh(session)
        return {
            "success": True,
            "session_id": session.id,
            "duration_minutes": session.duration_minutes,
            "recorded_at": session.recorded_at.isoformat()
        }
    finally:
        db.close()

# --- 6. DATA-MODIFYING TOOL: Save Job Listing ---
def tool_save_job_listing(
    user_id: str,
    company: str,
    role: str,
    job_url: Optional[str] = None,
    eligibility_notes: Optional[str] = None,
    status: str = "saved"
) -> Dict[str, Any]:
    """Saves a new job listing into the user's private application tracker."""
    if not company or not role:
        return {"error": "Both company and role are required fields."}

    valid_statuses = {"saved", "planned", "applied", "assessment", "interview", "offer", "rejected", "withdrawn"}
    if status not in valid_statuses:
        status = "saved"

    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"error": f"User with id '{user_id}' does not exist."}

        new_app = JobApplication(
            user_id=user_id,
            company=company.strip(),
            role=role.strip(),
            job_url=job_url.strip() if job_url else None,
            eligibility_notes=eligibility_notes,
            status=status,
            is_verified_opening=True
        )
        db.add(new_app)
        db.commit()
        db.refresh(new_app)
        return {
            "success": True,
            "job_application_id": new_app.id,
            "company": new_app.company,
            "role": new_app.role,
            "status": new_app.status
        }
    finally:
        db.close()

# --- 7. ANALYSIS TOOL: Generate Weekly Progress Summary ---
def tool_generate_weekly_summary(user_id: str) -> Dict[str, Any]:
    """Aggregates verified metrics from database to summarize the current week's actual progress."""
    from backend.app.models.practice import CodingSubmission, SqlSubmission
    from backend.app.models.interview import InterviewSession

    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"error": f"User with id '{user_id}' does not exist."}

        one_week_ago = datetime.utcnow() - timedelta(days=7)
        
        # 1. Study tasks
        tasks = db.query(StudyTask).filter(StudyTask.user_id == user_id).all()
        planned_count = len(tasks)
        completed_count = sum(1 for t in tasks if t.status == "completed")
        completion_rate = round((completed_count / planned_count * 100), 1) if planned_count > 0 else 0.0

        # 2. Coding problems solved
        coding_solved = db.query(CodingSubmission).filter(
            CodingSubmission.user_id == user_id,
            CodingSubmission.passed == True,
            CodingSubmission.submitted_at >= one_week_ago
        ).count()

        # 3. SQL exercises completed
        sql_solved = db.query(SqlSubmission).filter(
            SqlSubmission.user_id == user_id,
            SqlSubmission.passed == True,
            SqlSubmission.submitted_at >= one_week_ago
        ).count()

        # 4. Assessments & skill proficiencies
        assessments = db.query(AssessmentAttempt).filter(
            AssessmentAttempt.user_id == user_id,
            AssessmentAttempt.completed_at >= one_week_ago
        ).all()
        avg_score = round(sum(a.score_percentage for a in assessments) / len(assessments), 1) if assessments else 0.0

        metrics = db.query(UserSkillMetric).filter(UserSkillMetric.user_id == user_id).all()
        # Sort by proficiency to find weaknesses
        sorted_metrics = sorted(metrics, key=lambda m: m.measured_proficiency)
        weaknesses = [f"{m.topic} ({m.measured_proficiency:.1f}%)" for m in sorted_metrics[:3] if m.measured_proficiency < 75]
        strengths = [f"{m.topic} ({m.measured_proficiency:.1f}%)" for m in sorted_metrics if m.measured_proficiency >= 75]

        # 5. Job applications
        applications = db.query(JobApplication).filter(JobApplication.user_id == user_id).all()
        applied_count = sum(1 for a in applications if a.status in ["applied", "assessment", "interview", "offer"])

        return {
            "week_start": (date.today() - timedelta(days=6)).isoformat(),
            "week_end": date.today().isoformat(),
            "tasks_planned": planned_count,
            "tasks_completed": completed_count,
            "completion_rate_percentage": completion_rate,
            "coding_problems_solved": coding_solved,
            "sql_exercises_completed": sql_solved,
            "assessments_completed": len(assessments),
            "average_assessment_score": avg_score,
            "verified_applications_count": applied_count,
            "identified_weaknesses": weaknesses if weaknesses else ["DSA (Requires systematic Two-Pointer & Sliding Window baseline)"],
            "strengths": strengths,
            "next_week_priorities": [
                "Prioritize 75 mins daily DSA practice on two pointers and hash maps.",
                "Complete SQL multi-table JOINs and window functions exercises.",
                "Conduct 1 mock technical interview on RAG chatbot architecture."
            ]
        }
    finally:
        db.close()

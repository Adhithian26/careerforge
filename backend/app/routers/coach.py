from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.models.assessment import UserSkillMetric
from backend.app.schemas.ai import CoachChatRequest, CoachChatResponse
from backend.app.ai.agent_adk import coach_orchestrator
from backend.app.services.auth_service import get_current_user

router = APIRouter(prefix="/coach", tags=["AI Career Coach"])

@router.post("/chat", response_model=CoachChatResponse)
def chat_with_career_coach(
    payload: CoachChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submits user message to the Google ADK Career Coach, grounded in the student's
    actual degree, target roles, confidence ratings, and measured skill metrics.
    """
    profile = current_user.profile
    profile_data = {
        "degree": profile.degree if profile else "B.Tech AI & Data Science",
        "graduation_year": profile.graduation_year if profile else 2027,
        "daily_study_hours": profile.daily_study_hours if profile else 4,
        "python_confidence": profile.python_confidence if profile else 3,
        "sql_confidence": profile.sql_confidence if profile else 3,
        "dsa_confidence": profile.dsa_confidence if profile else 1,
        "target_roles": profile.target_roles if profile else "Software Development Engineer"
    }

    metrics = db.query(UserSkillMetric).filter(UserSkillMetric.user_id == current_user.id).all()
    metrics_data = [
        {"topic": m.topic, "measured_proficiency": m.measured_proficiency, "confidence": m.subjective_confidence}
        for m in metrics
    ]

    response = coach_orchestrator.chat(
        message=payload.message,
        conversation_history=payload.conversation_history,
        user_profile=profile_data,
        skill_metrics=metrics_data
    )

    return CoachChatResponse(
        reply=response["reply"],
        suggested_actions=response.get("suggested_actions", []),
        agent_name=response.get("agent_name", "Career Coach"),
        model_used=response.get("model_used", "gemini-2.5-flash")
    )

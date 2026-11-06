from datetime import datetime
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.models.assessment import AssessmentQuestion, AssessmentAttempt, UserSkillMetric
from backend.app.schemas.assessment import (
    AssessmentQuestionResponse,
    SubmitAssessmentRequest,
    AssessmentResultResponse,
    AnswerResultDetail,
    SkillMetricResponse,
    UpdateConfidenceRequest,
    UpdateSkillMetricItem,
    CalibrateSkillMetricsRequest
)
from backend.app.services.auth_service import get_current_user

router = APIRouter(prefix="/assessment", tags=["Skill Assessment"])

SUPPORTED_TOPICS = ["Python", "SQL", "DSA", "Aptitude", "OOP", "DBMS", "Operating Systems", "Computer Networks"]

@router.get("/topics")
def get_topics() -> List[str]:
    """Returns list of supported skill assessment topics."""
    return SUPPORTED_TOPICS

@router.get("/metrics", response_model=List[SkillMetricResponse])
def get_user_skill_metrics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves measured proficiency vs subjective confidence across all topics."""
    metrics = db.query(UserSkillMetric).filter(UserSkillMetric.user_id == current_user.id).all()
    
    # Ensure all topics have a metric record
    existing_topics = {m.topic for m in metrics}
    for t in SUPPORTED_TOPICS:
        if t not in existing_topics:
            new_metric = UserSkillMetric(
                user_id=current_user.id,
                topic=t,
                measured_proficiency=0.0,
                subjective_confidence=1
            )
            db.add(new_metric)
            metrics.append(new_metric)
    db.commit()
    return metrics

@router.put("/confidence")
def update_subjective_confidence(
    payload: UpdateConfidenceRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Allows user to update their subjective confidence rating (1-5)."""
    if payload.confidence < 1 or payload.confidence > 5:
        raise HTTPException(status_code=400, detail="Confidence rating must be between 1 and 5.")

    metric = db.query(UserSkillMetric).filter(
        UserSkillMetric.user_id == current_user.id,
        UserSkillMetric.topic == payload.topic
    ).first()

    if not metric:
        metric = UserSkillMetric(
            user_id=current_user.id,
            topic=payload.topic,
            subjective_confidence=payload.confidence
        )
        db.add(metric)
    else:
        metric.subjective_confidence = payload.confidence

    db.commit()
    return {"message": f"Updated subjective confidence for {payload.topic} to {payload.confidence}/5."}

@router.post("/calibrate")
def calibrate_skill_metrics(
    payload: CalibrateSkillMetricsRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Allows user to customize/personalize their measured proficiency and subjective confidence for each topic."""
    updated_topics = []
    weak_topics = []

    for item in payload.metrics:
        topic_name = item.topic.strip()
        if not topic_name:
            continue
        prof = max(0.0, min(100.0, round(float(item.measured_proficiency), 1)))
        conf = max(1, min(5, int(item.subjective_confidence)))

        if prof < 50.0 or conf <= 2:
            weak_topics.append(topic_name)

        metric = db.query(UserSkillMetric).filter(
            UserSkillMetric.user_id == current_user.id,
            UserSkillMetric.topic.ilike(topic_name)
        ).first()

        if not metric:
            metric = UserSkillMetric(
                user_id=current_user.id,
                topic=topic_name,
                measured_proficiency=prof,
                subjective_confidence=conf,
                attempts_count=1,
                total_questions_answered=10,
                total_correct_answered=int(round(10 * (prof / 100.0))),
                last_assessed_at=datetime.utcnow()
            )
            db.add(metric)
        else:
            metric.measured_proficiency = prof
            metric.subjective_confidence = conf
            metric.attempts_count = max(metric.attempts_count, 1)
            metric.total_questions_answered = max(metric.total_questions_answered or 10, 10)
            metric.total_correct_answered = int(round(metric.total_questions_answered * (prof / 100.0)))
            metric.last_assessed_at = datetime.utcnow()
        updated_topics.append(topic_name)

    db.commit()

    if payload.regenerate_plan:
        from backend.app.services.study_planner import generate_weekly_study_plan
        profile = current_user.profile
        daily_hours = float(profile.daily_study_hours if profile and profile.daily_study_hours else 4.0)
        generate_weekly_study_plan(db=db, user_id=current_user.id, daily_hours=daily_hours)

    return {
        "message": f"Successfully personalized metrics for {len(updated_topics)} topics.",
        "updated_topics": updated_topics,
        "weak_topics": weak_topics
    }

@router.delete("/topic/{topic_name}")
def delete_user_skill_metric(
    topic_name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Removes a skill metric topic for the current user."""
    metric = db.query(UserSkillMetric).filter(
        UserSkillMetric.user_id == current_user.id,
        UserSkillMetric.topic.ilike(topic_name)
    ).first()
    if metric:
        db.delete(metric)
        db.commit()
        return {"message": f"Removed {topic_name} from skill metrics."}
    return {"message": "Topic not found."}

@router.get("/questions/{topic}", response_model=List[AssessmentQuestionResponse])
def get_assessment_questions(
    topic: str,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Retrieves questions for a test without leaking the correct answer index."""
    questions = db.query(AssessmentQuestion).filter(
        AssessmentQuestion.topic.ilike(f"%{topic}%")
    ).limit(limit).all()

    if not questions:
        # Fallback to all questions if specific topic has fewer
        questions = db.query(AssessmentQuestion).limit(limit).all()

    return questions

@router.post("/submit", response_model=AssessmentResultResponse)
def submit_assessment(
    payload: SubmitAssessmentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submits user answers, calculates true deterministic score, updates skill proficiency,
    and returns granular breakdown with explanations.
    """
    if not payload.answers:
        raise HTTPException(status_code=400, detail="No answers submitted.")

    breakdown: List[AnswerResultDetail] = []
    correct_count = 0

    for ans in payload.answers:
        q = db.query(AssessmentQuestion).filter(AssessmentQuestion.id == ans.question_id).first()
        if not q:
            continue

        is_correct = (ans.selected_option_index == q.correct_option_index)
        if is_correct:
            correct_count += 1

        breakdown.append(AnswerResultDetail(
            question_id=q.id,
            question_text=q.question_text,
            selected_option_index=ans.selected_option_index,
            correct_option_index=q.correct_option_index,
            is_correct=is_correct,
            explanation=q.explanation
        ))

    total_q = len(payload.answers)
    score_pct = round((correct_count / total_q * 100), 1)

    # Persist attempt record
    attempt = AssessmentAttempt(
        user_id=current_user.id,
        topic=payload.topic,
        total_questions=total_q,
        correct_count=correct_count,
        score_percentage=score_pct,
        time_spent_seconds=payload.time_spent_seconds,
        answers_summary=[b.model_dump() for b in breakdown]
    )
    db.add(attempt)

    # Update UserSkillMetric using moving average / cumulative performance
    metric = db.query(UserSkillMetric).filter(
        UserSkillMetric.user_id == current_user.id,
        UserSkillMetric.topic.ilike(f"%{payload.topic}%")
    ).first()

    if not metric:
        metric = UserSkillMetric(
            user_id=current_user.id,
            topic=payload.topic,
            measured_proficiency=score_pct,
            attempts_count=1,
            total_questions_answered=total_q,
            total_correct_answered=correct_count,
            last_assessed_at=datetime.utcnow()
        )
        db.add(metric)
    else:
        metric.attempts_count += 1
        metric.total_questions_answered += total_q
        metric.total_correct_answered += correct_count
        # Calculated cumulative proficiency percentage
        metric.measured_proficiency = round(
            (metric.total_correct_answered / metric.total_questions_answered * 100), 1
        )
        metric.last_assessed_at = datetime.utcnow()

    db.commit()
    db.refresh(attempt)

    recommendation = (
        f"Solid demonstration on {payload.topic}! Continue building speed and edge-case testing."
        if score_pct >= 70 else
        f"Demonstrated weakness identified in {payload.topic} ({score_pct}%). Review explanations for missed questions and focus next study session on core concepts."
    )

    return AssessmentResultResponse(
        id=attempt.id,
        topic=payload.topic,
        total_questions=total_q,
        correct_count=correct_count,
        score_percentage=score_pct,
        time_spent_seconds=payload.time_spent_seconds,
        completed_at=attempt.completed_at,
        breakdown=breakdown,
        updated_measured_proficiency=metric.measured_proficiency,
        recommendation=recommendation
    )

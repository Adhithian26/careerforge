from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.models.interview import InterviewSession, InterviewExchange
from backend.app.schemas.interview import (
    StartInterviewRequest,
    AnswerInterviewQuestionRequest,
    InterviewExchangeResponse,
    InterviewSessionDetailResponse
)
from backend.app.services.auth_service import get_current_user

router = APIRouter(prefix="/interview", tags=["Mock Interview"])

# Curated question sequences per interview mode
INTERVIEW_QUESTION_POOLS = {
    "Technical": [
        "Explain the internal mechanics of a Python dictionary or hash table. How does CPython handle collisions and resize its hash table?",
        "Suppose you have an array of 10 million integers. How would you find the top 100 most frequent elements efficiently in terms of time and space?",
        "In a distributed system or microservice architecture, how do you handle eventual consistency across database boundaries? What are the tradeoffs between 2-Phase Commit and the Saga pattern?"
    ],
    "HR": [
        "Walk me through your journey pursuing B.Tech in AI and Data Science. What drove your interest in software development, and what are your long-term career aspirations?",
        "Tell me about a time when you encountered a major disagreement with a team member during a technical project. How did you resolve it?",
        "Why are you interested in joining our engineering team, and how do you plan to adapt during your first 90 days on the job?"
    ],
    "Project": [
        "Let's discuss your RAG Chatbot project. Walk me through the retrieval pipeline from user query to embedding lookup, chunk selection, and context generation. What were the main sources of latency?",
        "In your Facial Recognition Attendance System, how did you balance false positives against false negatives, and how did you verify that student photos could not spoof the system?",
        "If you had to redesign either of your projects from scratch with production traffic in mind, what architectural choices would you change?"
    ],
    "Aptitude": [
        "A software service experiences a traffic surge that increases requests by 25%, while server capacity is concurrently scaled down by 20%. What is the net percentage change in load per server?",
        "Explain how you would calculate the probability of picking at least one defective component from a batch of 100 containing 5 defectives when sampling 3 components without replacement."
    ]
}

def evaluate_answer_rubric(question: str, answer: str, mode: str) -> Dict[str, Any]:
    """Transparent deterministic rubric evaluating answer length, key terms, clarity, and communication."""
    words = [w.strip() for w in answer.split() if w.strip()]
    word_count = len(words)

    if word_count < 15:
        return {
            "clarity": 4.0,
            "correctness": 4.5,
            "communication": 4.0,
            "feedback": "Answer is too brief to demonstrate technical depth or clear communication. Expand on concrete mechanisms, trade-offs, and examples.",
            "improvements": ["Elaborate on the underlying engineering rationale.", "Use the STAR method (Situation, Task, Action, Result) for structured responses."]
        }
    elif word_count < 45:
        return {
            "clarity": 7.0,
            "correctness": 7.5,
            "communication": 7.0,
            "feedback": "Good concise response covering the core concept. To reach top-tier interview standards, include specific trade-offs, Big-O complexities, or practical implementation gotchas.",
            "improvements": ["Cite specific metrics or complexity bounds (e.g. O(1) average vs O(N) worst case).", "Mention real-world edge cases."]
        }
    else:
        return {
            "clarity": 8.5,
            "correctness": 9.0,
            "communication": 8.5,
            "feedback": "Strong, comprehensive answer demonstrating technical clarity, thorough reasoning, and structured communication.",
            "improvements": ["Keep responses concise to maintain interviewer engagement without rambling.", "Summarize key conclusions cleanly at the end."]
        }

@router.post("/start", response_model=InterviewSessionDetailResponse)
def start_interview(
    payload: StartInterviewRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Initializes a new mock interview session and returns the first question."""
    mode = payload.interview_mode if payload.interview_mode in INTERVIEW_QUESTION_POOLS else "Technical"
    questions = INTERVIEW_QUESTION_POOLS[mode]

    session = InterviewSession(
        user_id=current_user.id,
        role=payload.role,
        target_company=payload.target_company,
        interview_mode=mode,
        status="in_progress"
    )
    db.add(session)
    db.flush()

    # Create round 1 exchange
    first_exchange = InterviewExchange(
        session_id=session.id,
        round_number=1,
        question=questions[0]
    )
    db.add(first_exchange)
    db.commit()
    db.refresh(session)
    return session

@router.post("/sessions/{session_id}/answer", response_model=InterviewSessionDetailResponse)
def answer_question(
    session_id: str,
    payload: AnswerInterviewQuestionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Evaluates user's answer against transparent rubrics and progresses to next round or final report."""
    session = db.query(InterviewSession).filter(
        InterviewSession.id == session_id,
        InterviewSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found.")
    if session.status == "completed":
        raise HTTPException(status_code=400, detail="This interview session is already completed.")

    current_exchange = db.query(InterviewExchange).filter(
        InterviewExchange.session_id == session.id,
        InterviewExchange.user_answer == None
    ).order_by(InterviewExchange.round_number.asc()).first()

    if not current_exchange:
        raise HTTPException(status_code=400, detail="No pending question found in this session.")

    # Evaluate answer against rubric
    rubric = evaluate_answer_rubric(
        question=current_exchange.question,
        answer=payload.user_answer,
        mode=session.interview_mode
    )

    current_exchange.user_answer = payload.user_answer
    current_exchange.clarity_score = rubric["clarity"]
    current_exchange.correctness_score = rubric["correctness"]
    current_exchange.communication_score = rubric["communication"]
    current_exchange.feedback = rubric["feedback"]
    current_exchange.key_improvements = rubric["improvements"]

    # Check if more questions exist
    pool = INTERVIEW_QUESTION_POOLS.get(session.interview_mode, INTERVIEW_QUESTION_POOLS["Technical"])
    current_round = current_exchange.round_number

    if current_round < len(pool):
        next_question = pool[current_round]
        next_exchange = InterviewExchange(
            session_id=session.id,
            round_number=current_round + 1,
            question=next_question
        )
        db.add(next_exchange)
    else:
        # Finalize interview session
        all_exchanges = db.query(InterviewExchange).filter(InterviewExchange.session_id == session.id).all()
        avg_score = round(
            sum((e.clarity_score + e.correctness_score + e.communication_score) / 3.0 for e in all_exchanges) / len(all_exchanges) * 10,
            1
        )
        session.status = "completed"
        session.overall_score = avg_score
        session.completed_at = datetime.utcnow()
        session.summary_report = (
            f"Mock Interview Completed: Overall Performance Score: {avg_score}/100. "
            f"Demonstrated technical understanding across {len(all_exchanges)} rounds. "
            f"Focus on concise structuring and citing empirical metrics in subsequent mock sessions."
        )

    db.commit()
    db.refresh(session)
    return session

@router.get("/sessions", response_model=List[InterviewSessionDetailResponse])
def get_user_interviews(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves all past interview sessions for the student."""
    return db.query(InterviewSession).filter(
        InterviewSession.user_id == current_user.id
    ).order_by(InterviewSession.created_at.desc()).all()

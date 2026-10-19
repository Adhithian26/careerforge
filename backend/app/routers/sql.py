from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.models.practice import SqlProblem, SqlSubmission
from backend.app.schemas.practice import (
    SqlProblemSummary,
    SqlProblemDetail,
    SqlExecuteRequest,
    SqlExecutionResponse
)
from backend.app.services.sql_sandbox import execute_sql_practice
from backend.app.services.auth_service import get_current_user

router = APIRouter(prefix="/sql", tags=["SQL Practice"])

@router.get("/problems", response_model=List[SqlProblemSummary])
def get_sql_problems(db: Session = Depends(get_db)):
    """Retrieves all available SQL query exercises."""
    return db.query(SqlProblem).all()

@router.get("/problems/{slug}", response_model=SqlProblemDetail)
def get_sql_problem_detail(slug: str, db: Session = Depends(get_db)):
    """Retrieves full SQL problem statement, schema context, and hints."""
    problem = db.query(SqlProblem).filter(SqlProblem.slug == slug).first()
    if not problem:
        raise HTTPException(status_code=404, detail=f"SQL Problem '{slug}' not found.")
    return problem

@router.post("/problems/{slug}/execute", response_model=SqlExecutionResponse)
def execute_query(
    slug: str,
    payload: SqlExecuteRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Executes learner query against an isolated read-only SQLite relational database,
    evaluates against expected query result set, and logs persisted submission.
    """
    problem = db.query(SqlProblem).filter(SqlProblem.slug == slug).first()
    if not problem:
        raise HTTPException(status_code=404, detail="SQL Problem not found.")

    res = execute_sql_practice(
        user_query=payload.query,
        expected_query=problem.expected_sql
    )

    # Persist attempt record
    submission = SqlSubmission(
        user_id=current_user.id,
        problem_id=problem.id,
        submitted_query=payload.query,
        passed=res["passed"],
        execution_time_ms=res["execution_time_ms"],
        row_count=res["row_count"],
        error_message=res.get("error")
    )
    db.add(submission)
    db.commit()

    if res["passed"]:
        res["explanation"] = problem.explanation

    return res

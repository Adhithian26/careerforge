from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.models.practice import CodingProblem, CodingSubmission
from backend.app.schemas.practice import (
    CodingProblemSummary,
    CodingProblemDetail,
    CodingRunRequest,
    CodingSubmitRequest,
    CodingExecutionResponse
)
from backend.app.services.code_executor import execute_coding_exercise
from backend.app.services.auth_service import get_current_user

router = APIRouter(prefix="/coding", tags=["Coding Practice"])

@router.get("/problems", response_model=List[CodingProblemSummary])
def get_coding_problems(db: Session = Depends(get_db)):
    """Retrieves all available Python coding exercises."""
    problems = db.query(CodingProblem).all()
    return problems

@router.get("/problems/{slug}", response_model=CodingProblemDetail)
def get_coding_problem_detail(slug: str, db: Session = Depends(get_db)):
    """Retrieves full problem statement, starter code, sample tests, and hints."""
    problem = db.query(CodingProblem).filter(CodingProblem.slug == slug).first()
    if not problem:
        raise HTTPException(status_code=404, detail=f"Problem '{slug}' not found.")
    
    sample_tests = [tc for tc in problem.test_cases if tc.get("is_sample", False)]
    return CodingProblemDetail(
        id=problem.id,
        slug=problem.slug,
        title=problem.title,
        difficulty=problem.difficulty,
        category=problem.category,
        description=problem.description,
        starter_code=problem.starter_code,
        function_name=problem.function_name,
        hints=problem.hints or [],
        sample_tests=sample_tests
    )

@router.post("/problems/{slug}/run", response_model=CodingExecutionResponse)
def run_sample_code(
    slug: str,
    payload: CodingRunRequest,
    db: Session = Depends(get_db)
):
    """Executes code against visible sample test cases only without recording submission."""
    problem = db.query(CodingProblem).filter(CodingProblem.slug == slug).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found.")

    sample_tests = [tc for tc in problem.test_cases if tc.get("is_sample", False)]
    result = execute_coding_exercise(
        user_code=payload.code,
        function_name=problem.function_name,
        test_cases=sample_tests,
        timeout_seconds=3.0
    )
    return result

@router.post("/problems/{slug}/submit", response_model=CodingExecutionResponse)
def submit_code(
    slug: str,
    payload: CodingSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Executes code against all test cases (both sample and hidden) in a restricted sandbox,
    records submission, and returns transparent feedback without leaking hidden test cases.
    """
    problem = db.query(CodingProblem).filter(CodingProblem.slug == slug).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found.")

    result = execute_coding_exercise(
        user_code=payload.code,
        function_name=problem.function_name,
        test_cases=problem.test_cases,
        timeout_seconds=3.0
    )

    # Persist attempt record
    submission = CodingSubmission(
        user_id=current_user.id,
        problem_id=problem.id,
        submitted_code=payload.code,
        passed=result["passed"],
        passed_tests_count=result["passed_tests"],
        total_tests_count=result["total_tests"],
        runtime_ms=result["runtime_ms"],
        error_message=result.get("error"),
        test_results=result.get("results")
    )
    db.add(submission)
    db.commit()

    if result["passed"]:
        result["solution_approach"] = problem.solution_approach

    return result

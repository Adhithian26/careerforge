from datetime import date, datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.app.models.user import User, UserProfile
from backend.app.models.study_plan import StudyPlan, StudyTask
from backend.app.models.assessment import UserSkillMetric

# Daily Topic Schedule Blueprint for a 4-Hour (240 min) Allocation
DEFAULT_CURRICULUM_WEEK = [
    # Day 0: Monday
    [
        {"title": "DSA: Two Pointers & Sliding Window Patterns", "topic": "DSA", "duration_minutes": 75, "priority": "Urgent", "notes": "Solve 2 LeetCode-style medium array/string problems. Focus on space-time complexity analysis."},
        {"title": "Python: Advanced Data Structures & Memory Model", "topic": "Python", "duration_minutes": 45, "priority": "High", "notes": "Practice list comprehensions, dict internals, and set operations."},
        {"title": "SQL: Multi-table INNER & LEFT JOINs", "topic": "SQL", "duration_minutes": 45, "priority": "High", "notes": "Solve 3 multi-table join exercises on employee/department schema."},
        {"title": "CS Fundamentals: OS Process Scheduling & Deadlocks", "topic": "Operating Systems", "duration_minutes": 45, "priority": "Medium", "notes": "Review CPU scheduling algorithms (Round Robin, FCFS) and Banker's algorithm."},
        {"title": "Project Prep: RAG Chatbot Architecture Documentation", "topic": "Projects", "duration_minutes": 30, "priority": "Medium", "notes": "Document chunking strategy, vector store embeddings, and retrieval trade-offs in README."}
    ],
    # Day 1: Tuesday
    [
        {"title": "DSA: Binary Search & Two-Pointer Extensions", "topic": "DSA", "duration_minutes": 75, "priority": "Urgent", "notes": "Focus on search in rotated sorted array and lower/upper bound."},
        {"title": "SQL: GROUP BY, HAVING & Aggregate Functions", "topic": "SQL", "duration_minutes": 45, "priority": "High", "notes": "Filter grouped metrics using HAVING versus WHERE."},
        {"title": "Python: Object-Oriented Design & Dunder Methods", "topic": "Python", "duration_minutes": 45, "priority": "High", "notes": "Implement inheritance, polymorphism, __repr__, and __call__."},
        {"title": "DBMS: ACID Properties & Transaction Isolation Levels", "topic": "DBMS", "duration_minutes": 45, "priority": "Medium", "notes": "Study Read Committed vs Repeatable Read and dirty reads."},
        {"title": "Job Search: Research Zoho & TCS Eligibility Criteria", "topic": "Applications", "duration_minutes": 30, "priority": "Medium", "notes": "Log 2 target off-campus/on-campus opening deadlines in Job Tracker."}
    ],
    # Day 2: Wednesday
    [
        {"title": "DSA: Fast & Slow Pointers, Linked List Cycles", "topic": "DSA", "duration_minutes": 75, "priority": "Urgent", "notes": "Implement cycle detection and reverse linked list iteratively."},
        {"title": "Python: Exception Handling, Generators & Iterators", "topic": "Python", "duration_minutes": 45, "priority": "High", "notes": "Write memory-efficient stream processing functions using yield."},
        {"title": "SQL: Subqueries, Correlated Subqueries & EXISTS", "topic": "SQL", "duration_minutes": 45, "priority": "High", "notes": "Practice scalar subqueries and correlated condition checks."},
        {"title": "Computer Networks: TCP vs UDP & Handshake", "topic": "Computer Networks", "duration_minutes": 45, "priority": "Medium", "notes": "Deep dive into 3-way handshake, congestion control, and TCP flow control."},
        {"title": "Project Prep: Facial Recognition System Edge Cases", "topic": "Projects", "duration_minutes": 30, "priority": "Medium", "notes": "Prepare explanations for lighting variation, false acceptance rate (FAR), and latency."}
    ],
    # Day 3: Thursday
    [
        {"title": "DSA: Stacks, Monotonic Stacks & Valid Parentheses", "topic": "DSA", "duration_minutes": 75, "priority": "Urgent", "notes": "Master next greater element pattern with monotonic stack."},
        {"title": "SQL: Window Functions (ROW_NUMBER, RANK, DENSE_RANK)", "topic": "SQL", "duration_minutes": 45, "priority": "High", "notes": "Partition and order data within analytical windows."},
        {"title": "Aptitude: Time & Work, Speed Distance Calculations", "topic": "Aptitude", "duration_minutes": 45, "priority": "High", "notes": "Solve 15 timed quantitative aptitude questions typical of TCS/Zoho rounds."},
        {"title": "Python: Concurrency, Multiprocessing vs Asyncio", "topic": "Python", "duration_minutes": 45, "priority": "Medium", "notes": "Understand the GIL, I/O-bound vs CPU-bound performance."},
        {"title": "Career Prep: Resume Tailoring for SDE Roles", "topic": "Applications", "duration_minutes": 30, "priority": "Medium", "notes": "Use Resume Assistant to match keywords against Amazon SDE job description."}
    ],
    # Day 4: Friday
    [
        {"title": "DSA: Binary Trees Traversals (Pre/In/Post/Level Order)", "topic": "DSA", "duration_minutes": 75, "priority": "Urgent", "notes": "Implement recursive and iterative tree BFS/DFS traversals."},
        {"title": "SQL: CTEs (Common Table Expressions) & Recursive CTEs", "topic": "SQL", "duration_minutes": 45, "priority": "High", "notes": "Simplify nested logic using clean WITH clauses."},
        {"title": "Python: Decorators, Context Managers & Closures", "topic": "Python", "duration_minutes": 45, "priority": "High", "notes": "Build custom @timer decorator and contextlib context manager."},
        {"title": "CS Fundamentals: Virtual Memory & Paging", "topic": "Operating Systems", "duration_minutes": 45, "priority": "Medium", "notes": "Page faults, TLB, and page replacement policies (LRU, FIFO)."},
        {"title": "Mock Interview: Technical Round Simulation", "topic": "Interview", "duration_minutes": 30, "priority": "High", "notes": "Complete 1 full technical mock interview round on Python & DSA."}
    ],
    # Day 5: Saturday
    [
        {"title": "DSA: Hash Maps & Frequency Counting Under Time Limits", "topic": "DSA", "duration_minutes": 75, "priority": "Urgent", "notes": "Solve 2 problems under 25-minute strict countdown."},
        {"title": "SQL Comprehensive Assessment & Query Optimization", "topic": "SQL", "duration_minutes": 45, "priority": "High", "notes": "Take SQL assessment in Skill Assessment module and examine execution plans."},
        {"title": "Aptitude: Logical Reasoning, Syllogisms & Seating", "topic": "Aptitude", "duration_minutes": 45, "priority": "High", "notes": "Complete 10 logical puzzles and seating arrangement questions."},
        {"title": "Core CS: Normalization (1NF, 2NF, 3NF, BCNF) & Indexing", "topic": "DBMS", "duration_minutes": 45, "priority": "Medium", "notes": "Understand B-Trees, B+ Trees, and foreign key constraints."},
        {"title": "Applications: Verify & Submit 2 Eligible Applications", "topic": "Applications", "duration_minutes": 30, "priority": "High", "notes": "Review eligibility requirements and update status to Applied."}
    ],
    # Day 6: Sunday
    [
        {"title": "Weekly Assessment Review & Weakness Deep Dive", "topic": "DSA", "duration_minutes": 60, "priority": "Urgent", "notes": "Re-solve every problem or quiz question failed during the week."},
        {"title": "Python Comprehensive Quiz & Error Analysis", "topic": "Python", "duration_minutes": 45, "priority": "High", "notes": "Attempt topic assessment and review mistake explanations."},
        {"title": "HR & Behavioral Interview Practice (STAR Method)", "topic": "Interview", "duration_minutes": 45, "priority": "Medium", "notes": "Practice answering 'Tell me about yourself' and 'Greatest technical challenge'."},
        {"title": "Career Reflection: Long-Term Academia & Industry Roadmap", "topic": "Career Strategy", "duration_minutes": 45, "priority": "Medium", "notes": "Align industry experience milestones with future M.Tech/Ph.D. professorship pathway."},
        {"title": "Weekly Progress Synthesis & Next Week Setup", "topic": "Weekly Review", "duration_minutes": 45, "priority": "High", "notes": "Generate verified weekly summary report and set top 3 next week targets."}
    ]
]

def generate_weekly_study_plan(
    db: Session,
    user_id: str,
    start_date: Optional[date] = None,
    daily_hours: float = 4.0,
    focus_objective: Optional[str] = None
) -> StudyPlan:
    """
    Generates a structured, persisted 7-day study plan allocating 4 hours daily,
    tailored to the student's B.Tech AI & Data Science profile and weak areas.
    """
    if not start_date:
        start_date = date.today()
        
    end_date = start_date + timedelta(days=6)
    
    # Deactivate any previous active plans
    db.query(StudyPlan).filter(StudyPlan.user_id == user_id, StudyPlan.is_active == True).update({"is_active": False})
    
    plan = StudyPlan(
        user_id=user_id,
        title=f"7-Day SDE Mastery Sprint ({start_date.strftime('%b %d')} - {end_date.strftime('%b %d, %Y')})",
        start_date=start_date,
        end_date=end_date,
        daily_allocated_hours=daily_hours,
        focus_objective=focus_objective or "Master DSA Arrays/Pointers, strengthen SQL aggregations, and prepare SDE campus interview profiles.",
        is_active=True
    )
    db.add(plan)
    db.flush()

    # Generate tasks for all 7 days
    for day_offset, day_tasks in enumerate(DEFAULT_CURRICULUM_WEEK):
        task_date = start_date + timedelta(days=day_offset)
        for t in day_tasks:
            # Scale duration if daily_hours is customized
            scaled_duration = int(t["duration_minutes"] * (daily_hours / 4.0))
            task = StudyTask(
                plan_id=plan.id,
                user_id=user_id,
                scheduled_date=task_date,
                title=t["title"],
                topic=t["topic"],
                duration_minutes=scaled_duration,
                priority=t["priority"],
                status="pending",
                notes=t["notes"]
            )
            db.add(task)

    db.commit()
    db.refresh(plan)
    return plan

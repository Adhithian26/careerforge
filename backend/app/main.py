import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.app.config import settings
from backend.app.database import engine, Base, SessionLocal
import backend.app.models  # Ensure all SQLAlchemy models are registered
from backend.app.services.question_bank import seed_assessment_questions
from backend.app.services.practice_bank import seed_practice_problems
from backend.app.services.study_planner import generate_weekly_study_plan
from backend.app.utils.security import hash_password

# Import Routers
from backend.app.routers import (
    auth_router,
    profile_router,
    dashboard_router,
    assessment_router,
    coding_router,
    sql_router,
    interview_router,
    planner_router,
    jobs_router,
    resume_router,
    weekly_router,
    coach_router,
    mcp_router
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("careerforge")

# Ensure tables exist immediately on import
Base.metadata.create_all(bind=engine)

def seed_initial_workspace_data():
    """Initializes tables and seeds the default student profile, questions, and curriculum."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        from backend.app.models.user import User, UserProfile
        from backend.app.models.assessment import UserSkillMetric
        from backend.app.models.job_tracker import JobApplication

        # 1. Seed or retrieve personal student user
        personal_email = "adhithian260506@gmail.com"
        user = db.query(User).filter(User.email == personal_email).first()
        if not user:
            # Check if legacy student@careerforge.ai exists to migrate
            legacy_user = db.query(User).filter(User.email == "student@careerforge.ai").first()
            if legacy_user:
                logger.info("Migrating legacy profile to adhithian260506@gmail.com...")
                legacy_user.email = personal_email
                legacy_user.hashed_password = hash_password("Adhi@2656")
                db.commit()
                user = legacy_user
            else:
                logger.info("Seeding initial student profile for adhithian260506@gmail.com...")
                user = User(
                    email=personal_email,
                    hashed_password=hash_password("Adhi@2656"),
                    full_name="Adhithian S",
                    is_admin=True
                )
                db.add(user)
                db.flush()

            profile = UserProfile(
                user_id=user.id,
                degree="B.Tech Artificial Intelligence and Data Science",
                graduation_year=2027,
                daily_study_hours=4,
                python_confidence=3,
                sql_confidence=3,
                dsa_confidence=1,
                target_roles="Software Development Engineer, AI Engineer, Backend Developer",
                preferred_companies="Zoho, TCS, Amazon, Google, PayPal, Tech Mahindra",
                existing_projects="RAG Chatbot, Facial Recognition Attendance System",
                career_goals="Gain 2–4 years industry software engineering experience, achieve financial stability, and subsequently pursue professorship qualifications."
            )
            db.add(profile)
            
            # Seed initial baseline skill metrics
            initial_metrics = [
                ("Python", 3, 65.0),
                ("SQL", 3, 60.0),
                ("DSA", 1, 30.0),
                ("Aptitude", 3, 65.0),
                ("OOP", 3, 70.0),
                ("DBMS", 3, 65.0),
                ("Operating Systems", 2, 55.0),
                ("Computer Networks", 2, 50.0)
            ]
            for topic, conf, prof in initial_metrics:
                metric = UserSkillMetric(
                    user_id=user.id,
                    topic=topic,
                    subjective_confidence=conf,
                    measured_proficiency=prof,
                    attempts_count=1,
                    total_questions_answered=5,
                    total_correct_answered=int(5 * (prof / 100))
                )
                db.add(metric)

            # Seed target job applications
            initial_apps = [
                JobApplication(
                    user_id=user.id,
                    company="Zoho",
                    role="Software Developer",
                    job_url="https://careers.zohocorp.com",
                    location="Chennai, India",
                    status="planned",
                    eligibility_notes="Targeting 2027 campus/off-campus recruitment drive. Focus on advanced C/Python problem solving.",
                    is_verified_opening=True
                ),
                JobApplication(
                    user_id=user.id,
                    company="Amazon",
                    role="Software Development Engineer I (SDE 1)",
                    job_url="https://amazon.jobs",
                    location="Bengaluru / Hyderabad",
                    status="saved",
                    eligibility_notes="2027 graduating batch eligible for summer internship & full-time conversion. Strong DSA bar.",
                    is_verified_opening=True
                ),
                JobApplication(
                    user_id=user.id,
                    company="TCS",
                    role="Digital / Prime Developer",
                    job_url="https://www.tcs.com/careers",
                    location="Pan India",
                    status="planned",
                    eligibility_notes="NQT high score required. Aptitude + 2 DSA coding problems.",
                    is_verified_opening=True
                )
            ]
            for app in initial_apps:
                db.add(app)

            db.commit()

            # Seed initial study plan
            generate_weekly_study_plan(db=db, user_id=user.id)

        # 2. Seed question catalog and practice catalog
        seed_assessment_questions(db)
        seed_practice_problems(db)
        logger.info("Database initialized and seeded successfully.")
    except Exception as e:
        logger.error(f"Error during startup data seeding: {e}")
        db.rollback()
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting CareerForge AI Backend Engine...")
    seed_initial_workspace_data()
    from backend.app.mongodb import ping_mongodb, close_mongodb_connection
    if await ping_mongodb():
        logger.info("MongoDB Atlas cluster connected successfully.")
    else:
        logger.info("MongoDB Atlas connection disabled or unavailable.")
    yield
    # Shutdown
    logger.info("Shutting down CareerForge AI Backend Engine.")
    close_mongodb_connection()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="CareerForge AI - The Autonomous Career Intelligence & Preparation Platform",
    lifespan=lifespan
)

# CORS Configuration
_cors_origins = settings.cors_origin_list
if "*" in _cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=r"https?://.*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# Health Check Endpoints
@app.get("/health")
@app.get(f"{settings.API_V1_PREFIX}/health")
async def health_check():
    """Health check endpoint for Docker container and Google Cloud Run deployment."""
    from backend.app.mongodb import ping_mongodb
    mongo_ok = await ping_mongodb()
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "mongodb": "connected" if mongo_ok else "disabled"
    }

# Mount all API Routers under both /api/v1 and root /
all_routers = [
    auth_router,
    profile_router,
    dashboard_router,
    assessment_router,
    coding_router,
    sql_router,
    interview_router,
    planner_router,
    jobs_router,
    resume_router,
    weekly_router,
    coach_router,
    mcp_router
]

for r in all_routers:
    app.include_router(r, prefix=settings.API_V1_PREFIX)
    app.include_router(r)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)

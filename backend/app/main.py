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
    """Initializes tables and seeds the global question bank, practice problems, and persistent accounts."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Seed question catalog and practice catalog
        seed_assessment_questions(db)
        seed_practice_problems(db)
        logger.info("Catalogs initialized and seeded successfully.")

        # Self-healing persistence: ensure primary student account exists across ephemeral container restarts
        from backend.app.models.user import User, UserProfile
        from backend.app.routers.auth import initialize_new_user_workspace

        primary_email = "adhithian260506@gmail.com"
        existing_user = db.query(User).filter(User.email == primary_email).first()
        if not existing_user:
            user = User(
                email=primary_email,
                hashed_password=hash_password("Adhi@2656"),
                full_name="Adhithian S"
            )
            db.add(user)
            db.flush()
            profile = UserProfile(
                user_id=user.id,
                degree="B.Tech Artificial Intelligence and Data Science",
                graduation_year=2027,
                daily_study_hours=4,
                target_roles="Software Development Engineer, AI Engineer",
                preferred_companies="Zoho, TCS, Amazon, Google, PayPal",
                existing_projects="RAG Chatbot, Facial Recognition Attendance",
                career_goals="Tier-1 SDE Placement & Engineering Leadership",
                python_confidence=4,
                sql_confidence=4,
                dsa_confidence=2
            )
            db.add(profile)
            db.commit()
            db.refresh(user)
            initialize_new_user_workspace(db=db, user=user, profile=profile)
            logger.info(f"Initialized persistent primary student account: {primary_email}")

        # Ensure demo account exists
        demo_email = "teststudent@careerforge.ai"
        existing_demo = db.query(User).filter(User.email == demo_email).first()
        if not existing_demo:
            demo_user = User(
                email=demo_email,
                hashed_password=hash_password("TestStudent@123"),
                full_name="Test Student"
            )
            db.add(demo_user)
            db.flush()
            demo_profile = UserProfile(
                user_id=demo_user.id,
                degree="B.Tech Computer Science",
                graduation_year=2027,
                daily_study_hours=4,
                target_roles="Software Development Engineer",
                preferred_companies="Zoho, TCS, Amazon",
                existing_projects="Technical Portfolio Project",
                career_goals="Software Engineering Mastery",
                python_confidence=3,
                sql_confidence=3,
                dsa_confidence=2
            )
            db.add(demo_profile)
            db.commit()
            db.refresh(demo_user)
            initialize_new_user_workspace(db=db, user=demo_user, profile=demo_profile)
            logger.info(f"Initialized persistent demo account: {demo_email}")

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

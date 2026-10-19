from backend.app.routers.auth import router as auth_router
from backend.app.routers.profile import router as profile_router
from backend.app.routers.dashboard import router as dashboard_router
from backend.app.routers.assessment import router as assessment_router
from backend.app.routers.coding import router as coding_router
from backend.app.routers.sql import router as sql_router
from backend.app.routers.interview import router as interview_router
from backend.app.routers.planner import router as planner_router
from backend.app.routers.jobs import router as jobs_router
from backend.app.routers.resume import router as resume_router
from backend.app.routers.weekly import router as weekly_router
from backend.app.routers.coach import router as coach_router
from backend.app.routers.mcp_router import router as mcp_router

__all__ = [
    "auth_router",
    "profile_router",
    "dashboard_router",
    "assessment_router",
    "coding_router",
    "sql_router",
    "interview_router",
    "planner_router",
    "jobs_router",
    "resume_router",
    "weekly_router",
    "coach_router",
    "mcp_router",
]

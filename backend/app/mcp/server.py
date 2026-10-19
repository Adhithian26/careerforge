import json
import logging
from typing import Dict, Any, List, Optional
from mcp.server.mcpserver import MCPServer
from backend.app.config import settings
from backend.app.mcp.tools import (
    tool_read_skill_profile,
    tool_get_assessment_history,
    tool_read_application_tracker,
    tool_search_approved_jobs,
    tool_record_study_session,
    tool_save_job_listing,
    tool_generate_weekly_summary
)

logger = logging.getLogger("careerforge.mcp")

mcp_server = MCPServer(
    name="careerforge-mcp",
    version="1.0.0",
    instructions="Official CareerForge AI Model Context Protocol (MCP) Server for Student Career Intelligence"
)

# Authentication validator
def verify_mcp_auth(token: Optional[str]) -> bool:
    """Verifies that remote MCP caller provides the authorized security token."""
    if not settings.MCP_AUTH_TOKEN:
        return True
    return token == settings.MCP_AUTH_TOKEN

# 1. Register: Read Skill Profile
@mcp_server.tool(name="read_skill_profile", description="Retrieve student degree, graduation year, confidence ratings, and measured skill metrics.")
def read_skill_profile(user_id: str) -> str:
    result = tool_read_skill_profile(user_id=user_id)
    return json.dumps(result)

# 2. Register: Get Assessment History
@mcp_server.tool(name="get_assessment_history", description="Retrieve completed assessment attempts, topic scores, and timestamps.")
def get_assessment_history(user_id: str, topic: Optional[str] = None, limit: int = 10) -> str:
    result = tool_get_assessment_history(user_id=user_id, topic=topic, limit=limit)
    return json.dumps(result)

# 3. Register: Read Application Tracker
@mcp_server.tool(name="read_application_tracker", description="Retrieve job application pipeline records, statuses, and deadlines.")
def read_application_tracker(user_id: str, status_filter: Optional[str] = None) -> str:
    result = tool_read_application_tracker(user_id=user_id, status_filter=status_filter)
    return json.dumps(result)

# 4. Register: Search Approved Jobs
@mcp_server.tool(name="search_approved_jobs", description="Search verified openings from permitted career portals (Zoho, TCS, Amazon, PayPal, etc.).")
def search_approved_jobs(query: str) -> str:
    result = tool_search_approved_jobs(query=query)
    return json.dumps(result)

# 5. Register: Record Study Session (Data-Modifying)
@mcp_server.tool(name="record_study_session", description="Record a completed study session with duration in minutes and reflection notes.")
def record_study_session(user_id: str, duration_minutes: int, notes: Optional[str] = None, task_id: Optional[str] = None) -> str:
    result = tool_record_study_session(user_id=user_id, duration_minutes=duration_minutes, notes=notes, task_id=task_id)
    return json.dumps(result)

# 6. Register: Save Job Listing (Data-Modifying)
@mcp_server.tool(name="save_job_listing", description="Save a job opportunity to the student's tracker with company, role, URL, and status.")
def save_job_listing(user_id: str, company: str, role: str, job_url: Optional[str] = None, eligibility_notes: Optional[str] = None, status: str = "saved") -> str:
    result = tool_save_job_listing(user_id=user_id, company=company, role=role, job_url=job_url, eligibility_notes=eligibility_notes, status=status)
    return json.dumps(result)

# 7. Register: Generate Weekly Summary
@mcp_server.tool(name="generate_weekly_summary", description="Synthesize verified weekly metrics, problem completion rates, and next week priorities.")
def generate_weekly_summary(user_id: str) -> str:
    result = tool_generate_weekly_summary(user_id=user_id)
    return json.dumps(result)

# Helper for direct programmatic invocation by ADK or REST endpoints
def invoke_mcp_tool(tool_name: str, arguments: Dict[str, Any], auth_token: Optional[str] = None) -> Dict[str, Any]:
    """Safely invokes an MCP tool with token authentication and argument validation."""
    if not verify_mcp_auth(auth_token):
        return {"error": "Unauthorized: Invalid or missing MCP authentication token."}

    registry = {
        "read_skill_profile": tool_read_skill_profile,
        "get_assessment_history": tool_get_assessment_history,
        "read_application_tracker": tool_read_application_tracker,
        "search_approved_jobs": tool_search_approved_jobs,
        "record_study_session": tool_record_study_session,
        "save_job_listing": tool_save_job_listing,
        "generate_weekly_summary": tool_generate_weekly_summary
    }

    fn = registry.get(tool_name)
    if not fn:
        return {"error": f"Tool '{tool_name}' not found on MCP Server."}

    try:
        return fn(**arguments)
    except Exception as e:
        logger.error(f"Error invoking MCP tool '{tool_name}': {e}")
        return {"error": f"Tool invocation error: {str(e)}"}

from typing import Dict, Any, Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Header, HTTPException, status
from backend.app.models.user import User
from backend.app.mcp.server import invoke_mcp_tool
from backend.app.services.auth_service import get_current_user
from backend.app.config import settings

router = APIRouter(prefix="/mcp", tags=["Model Context Protocol (MCP)"])

class MCPInvokeRequest(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]

@router.get("/tools")
def list_available_mcp_tools():
    """Lists registered tools on the CareerForge MCP server with permissions."""
    return [
        {
            "name": "read_skill_profile",
            "type": "read-only",
            "description": "Retrieve student degree, graduation year, confidence ratings, and measured skill metrics."
        },
        {
            "name": "get_assessment_history",
            "type": "read-only",
            "description": "Retrieve completed assessment attempts, topic scores, and timestamps."
        },
        {
            "name": "read_application_tracker",
            "type": "read-only",
            "description": "Retrieve job application pipeline records, statuses, and deadlines."
        },
        {
            "name": "search_approved_jobs",
            "type": "read-only",
            "description": "Search verified openings from permitted career portals (Zoho, TCS, Amazon, PayPal, etc.)."
        },
        {
            "name": "record_study_session",
            "type": "data-modifying",
            "description": "Record a completed study session with duration in minutes and reflection notes."
        },
        {
            "name": "save_job_listing",
            "type": "data-modifying",
            "description": "Save a job opportunity to the student's tracker with company, role, URL, and status."
        },
        {
            "name": "generate_weekly_summary",
            "type": "analysis",
            "description": "Synthesize verified weekly metrics, problem completion rates, and next week priorities."
        }
    ]

@router.post("/invoke")
def execute_mcp_tool(
    payload: MCPInvokeRequest,
    current_user: User = Depends(get_current_user),
    x_mcp_token: Optional[str] = Header(None)
):
    """
    Invokes an MCP tool with authenticated connection verification and parameter validation.
    Injects user_id automatically if not provided.
    """
    auth_token = x_mcp_token or settings.MCP_AUTH_TOKEN
    args = dict(payload.arguments)
    if "user_id" not in args:
        args["user_id"] = current_user.id

    result = invoke_mcp_tool(
        tool_name=payload.tool_name,
        arguments=args,
        auth_token=auth_token
    )
    if "error" in result and "Unauthorized" in result["error"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=result["error"])
    return result

from backend.app.mcp.tools import (
    tool_read_skill_profile,
    tool_search_approved_jobs,
    tool_generate_weekly_summary,
    tool_record_study_session
)
from backend.app.mcp.server import invoke_mcp_tool
from backend.app.models.user import User
from backend.app.database import SessionLocal

def test_mcp_read_skill_profile():
    db = SessionLocal()
    user = db.query(User).first()
    db.close()
    assert user is not None

    res = tool_read_skill_profile(user.id)
    assert "user_id" in res
    assert res["graduation_year"] == 2027
    assert res["daily_study_hours"] == 4
    assert res["subjective_confidence"]["dsa"] == 1

def test_mcp_search_approved_jobs():
    res = tool_search_approved_jobs("zoho")
    assert len(res) > 0
    assert "Zoho" in res[0]["company"]
    assert res[0]["verified"] is True

def test_mcp_generate_weekly_summary():
    db = SessionLocal()
    user = db.query(User).first()
    db.close()

    res = tool_generate_weekly_summary(user.id)
    assert "tasks_planned" in res
    assert "next_week_priorities" in res
    assert len(res["next_week_priorities"]) == 3

def test_mcp_authenticated_invocation():
    db = SessionLocal()
    user = db.query(User).first()
    db.close()

    # Valid token invocation
    res = invoke_mcp_tool(
        tool_name="read_skill_profile",
        arguments={"user_id": user.id},
        auth_token="local_mcp_dev_token_2026"
    )
    assert "user_id" in res

    # Invalid token invocation
    unauthorized = invoke_mcp_tool(
        tool_name="read_skill_profile",
        arguments={"user_id": user.id},
        auth_token="invalid_bad_token"
    )
    assert "error" in unauthorized
    assert "Unauthorized" in unauthorized["error"]

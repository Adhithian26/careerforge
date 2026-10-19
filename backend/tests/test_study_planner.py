from fastapi.testclient import TestClient

def test_active_study_plan_generation(client: TestClient):
    res = client.get("/api/v1/planner/active-plan")
    assert res.status_code == 200
    data = res.json()
    assert data["is_active"] is True
    assert data["daily_allocated_hours"] == 4.0
    assert len(data["tasks"]) == 35  # 7 days * 5 tasks/day

def test_mark_study_task_completed(client: TestClient):
    plan_res = client.get("/api/v1/planner/active-plan")
    tasks = plan_res.json()["tasks"]
    first_task = tasks[0]

    update_res = client.patch(f"/api/v1/planner/tasks/{first_task['id']}", json={
        "status": "completed",
        "notes": "Finished Two Pointers practice ahead of time."
    })
    assert update_res.status_code == 200
    updated_task = update_res.json()
    assert updated_task["status"] == "completed"

    # Verify dashboard reflects completed task
    dash_res = client.get("/api/v1/dashboard")
    assert dash_res.status_code == 200
    dash_data = dash_res.json()
    assert dash_data["weekly_progress"]["tasks_completed"] >= 1

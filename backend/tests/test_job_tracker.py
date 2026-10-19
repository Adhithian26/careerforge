from fastapi.testclient import TestClient

def test_job_application_lifecycle(client: TestClient):
    # 1. Create a job application
    create_res = client.post("/api/v1/jobs", json={
        "company": "PayPal",
        "role": "Software Engineer 1",
        "job_url": "https://careers.pypl.com",
        "location": "Chennai",
        "status": "planned",
        "is_verified_opening": True
    })
    assert create_res.status_code == 200
    job_data = create_res.json()
    job_id = job_data["id"]
    assert job_data["company"] == "PayPal"
    assert job_data["status"] == "planned"

    # 2. Update status to 'applied'
    update_res = client.put(f"/api/v1/jobs/{job_id}", json={
        "status": "applied",
        "notes": "Application confirmed via official portal."
    })
    assert update_res.status_code == 200
    assert update_res.json()["status"] == "applied"

    # 3. Check pipeline stats
    stats_res = client.get("/api/v1/jobs/pipeline-stats")
    assert stats_res.status_code == 200
    stats = stats_res.json()
    assert stats["total_applied"] >= 1

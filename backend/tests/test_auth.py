from fastapi.testclient import TestClient

def test_health_check(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "CareerForge AI" in data["service"]

def test_register_and_create_new_user(client: TestClient):
    # Test creating a brand new student user
    res = client.post("/api/v1/auth/register", json={
        "email": "newstudent@careerforge.ai",
        "password": "NewStudentPass2027!",
        "full_name": "New Student",
        "degree": "B.Tech Computer Science and Engineering",
        "graduation_year": 2027,
        "daily_study_hours": 4,
        "python_confidence": 4,
        "sql_confidence": 3,
        "dsa_confidence": 2,
        "preferred_companies": "Zoho, Amazon, TCS"
    })
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["email"] == "newstudent@careerforge.ai"
    assert data["full_name"] == "New Student"

def test_login_and_token(client: TestClient):
    # Login with the test student
    res = client.post("/api/v1/auth/login", json={
        "email": "teststudent@careerforge.ai",
        "password": "TestStudent@123"
    })
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["email"] == "teststudent@careerforge.ai"

def test_invalid_login(client: TestClient):
    res = client.post("/api/v1/auth/login", json={
        "email": "teststudent@careerforge.ai",
        "password": "WrongPassword123"
    })
    assert res.status_code == 401

def test_get_current_user_profile(client: TestClient):
    login_res = client.post("/api/v1/auth/login", json={
        "email": "teststudent@careerforge.ai",
        "password": "TestStudent@123"
    })
    token = login_res.json()["access_token"]
    
    res = client.get("/api/v1/profile", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert data["graduation_year"] == 2027
    assert data["daily_study_hours"] == 4
    assert data["dsa_confidence"] == 1

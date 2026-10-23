from fastapi.testclient import TestClient

def test_health_check(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "CareerForge AI" in data["service"]

def test_login_and_token(client: TestClient):
    # Default seeded personal user
    res = client.post("/api/v1/auth/login", json={
        "email": "adhithian260506@gmail.com",
        "password": "Adhi@2656"
    })
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["email"] == "adhithian260506@gmail.com"

def test_invalid_login(client: TestClient):
    res = client.post("/api/v1/auth/login", json={
        "email": "adhithian260506@gmail.com",
        "password": "WrongPassword123"
    })
    assert res.status_code == 401

def test_get_current_user_profile(client: TestClient):
    login_res = client.post("/api/v1/auth/login", json={
        "email": "adhithian260506@gmail.com",
        "password": "Adhi@2656"
    })
    token = login_res.json()["access_token"]
    
    res = client.get("/api/v1/profile", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert data["graduation_year"] == 2027
    assert data["daily_study_hours"] == 4
    assert data["dsa_confidence"] == 1

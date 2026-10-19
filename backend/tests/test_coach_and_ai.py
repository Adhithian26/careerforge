from fastapi.testclient import TestClient

def test_coach_chat_fallback(client: TestClient):
    res = client.post("/api/v1/coach/chat", json={
        "message": "What should be my DSA focus with 1/5 confidence?"
    })
    assert res.status_code == 200
    data = res.json()
    assert "reply" in data
    assert "DSA" in data["reply"]
    assert len(data["suggested_actions"]) > 0

def test_resume_analyzer(client: TestClient):
    sample_resume = """
    B.Tech in Artificial Intelligence and Data Science (2027).
    Proficient in Python, SQL, REST APIs, Git.
    Projects: Built a RAG chatbot using LangChain and embeddings.
    Built a facial recognition attendance system using OpenCV.
    """
    job_desc = """
    Software Development Engineer I (SDE 1)
    Requirements:
    - Strong proficiency in Python and SQL
    - Solid understanding of Data Structures and Algorithms (DSA)
    - Experience building web services with FastAPI or Django
    - Knowledge of Docker and CI/CD pipelines
    """
    res = client.post("/api/v1/resume/analyze", json={
        "resume_text": sample_resume,
        "job_description": job_desc
    })
    assert res.status_code == 200
    data = res.json()
    assert data["match_percentage"] > 0
    assert "PYTHON" in [s.upper() for s in data["matched_skills"]]
    assert len(data["recommended_bullet_points"]) > 0

def test_project_interview_prep(client: TestClient):
    res = client.post("/api/v1/resume/project-prep", json={
        "project_title": "RAG Chatbot with Vector Database",
        "project_description": "A semantic Q&A chatbot built with LangChain and vector store",
        "tech_stack": "Python, LangChain, FAISS, FastAPI"
    })
    assert res.status_code == 200
    data = res.json()
    assert len(data["architecture_questions"]) > 0
    assert len(data["deep_dive_questions"]) > 0

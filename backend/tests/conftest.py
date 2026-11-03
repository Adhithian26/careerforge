import os
os.environ["TESTING"] = "True"
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.database import Base, get_db, SessionLocal
from backend.app.main import app, seed_initial_workspace_data
from backend.app.models.user import User, UserProfile
from backend.app.routers.auth import initialize_new_user_workspace
from backend.app.utils.security import hash_password, create_access_token

# Test in-memory SQLite database
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def seed_test_student():
    """Seeds a designated test user with complete workspace curriculum for test sessions."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == "teststudent@careerforge.ai").first()
        if not user:
            user = User(
                email="teststudent@careerforge.ai",
                hashed_password=hash_password("TestStudent@123"),
                full_name="Test Student",
                is_admin=True
            )
            db.add(user)
            db.flush()

            profile = UserProfile(
                user_id=user.id,
                degree="B.Tech Artificial Intelligence and Data Science",
                graduation_year=2027,
                daily_study_hours=4,
                python_confidence=3,
                sql_confidence=3,
                dsa_confidence=1,
                target_roles="Software Development Engineer",
                preferred_companies="Zoho, TCS, Amazon"
            )
            db.add(profile)
            db.commit()
            db.refresh(user)

            initialize_new_user_workspace(db=db, user=user, profile=profile)
        return user.id
    finally:
        db.close()

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=test_engine)
    seed_initial_workspace_data()
    seed_test_student()
    yield
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def db_session():
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client():
    user_id = seed_test_student()
    token = create_access_token(subject=user_id)
    with TestClient(app) as test_client:
        test_client.headers["Authorization"] = f"Bearer {token}"
        yield test_client

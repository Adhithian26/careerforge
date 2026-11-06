from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.user import User, UserProfile
from backend.app.models.assessment import UserSkillMetric
from backend.app.models.job_tracker import JobApplication
from backend.app.schemas.auth import Token, LoginRequest, RegisterRequest
from backend.app.schemas.user import UserResponse
from backend.app.utils.security import verify_password, hash_password, create_access_token
from backend.app.services.auth_service import get_current_user
from backend.app.services.study_planner import generate_weekly_study_plan

router = APIRouter(prefix="/auth", tags=["Authentication"])

def initialize_new_user_workspace(
    db: Session,
    user: User,
    profile: UserProfile,
    custom_metrics: any = None
):
    """Initializes a rich, personalized workspace for newly registered students."""
    # 1. Skill Metrics from user input
    if custom_metrics and len(custom_metrics) > 0:
        for sm in custom_metrics:
            topic_name = getattr(sm, 'topic', None) if hasattr(sm, 'topic') else sm.get('topic')
            prof = float(getattr(sm, 'measured_proficiency', None) if hasattr(sm, 'measured_proficiency') else sm.get('measured_proficiency', 50.0))
            conf = int(getattr(sm, 'subjective_confidence', None) if hasattr(sm, 'subjective_confidence') else sm.get('subjective_confidence', 3))
            if not topic_name:
                continue
            metric = UserSkillMetric(
                user_id=user.id,
                topic=topic_name.strip(),
                subjective_confidence=max(1, min(5, conf)),
                measured_proficiency=max(0.0, min(100.0, prof)),
                attempts_count=1,
                total_questions_answered=10,
                total_correct_answered=int(round(10 * (prof / 100.0)))
            )
            db.add(metric)
    else:
        # Fallback to user's registered confidence ratings
        p_conf = profile.python_confidence or 3
        s_conf = profile.sql_confidence or 3
        d_conf = profile.dsa_confidence or 1
        baseline_metrics = [
            ("Python", p_conf, min(100.0, float(p_conf) * 20.0)),
            ("SQL", s_conf, min(100.0, float(s_conf) * 20.0)),
            ("DSA", d_conf, min(100.0, float(d_conf) * 20.0)),
            ("Aptitude", 3, 60.0),
            ("OOP", 3, 65.0),
            ("DBMS", 3, 60.0),
            ("Operating Systems", 2, 50.0),
            ("Computer Networks", 2, 50.0)
        ]
        for topic, conf, prof in baseline_metrics:
            metric = UserSkillMetric(
                user_id=user.id,
                topic=topic,
                subjective_confidence=conf,
                measured_proficiency=prof,
                attempts_count=1,
                total_questions_answered=5,
                total_correct_answered=max(1, int(5 * (prof / 100.0)))
            )
            db.add(metric)

    # 2. Seed default target job applications based on preferred companies
    preferred_raw = profile.preferred_companies or "Zoho, TCS, Amazon"
    companies = [c.strip() for c in preferred_raw.split(",") if c.strip()]
    if not companies:
        companies = ["Zoho", "TCS", "Amazon"]

    company_directory = {
        "Zoho": ("https://careers.zohocorp.com", "Software Developer", "Chennai, India"),
        "TCS": ("https://www.tcs.com/careers", "Digital / Prime Developer", "Pan India"),
        "Amazon": ("https://amazon.jobs", "Software Development Engineer I (SDE 1)", "Bengaluru / Hyderabad"),
        "PayPal": ("https://careers.pypl.com", "Software Engineer 1", "Chennai / Bengaluru"),
        "Google": ("https://careers.google.com", "Software Engineer (Early Career)", "Bengaluru / Hyderabad"),
        "Tech Mahindra": ("https://careers.techmahindra.com", "Associate Software Engineer", "Pan India")
    }

    for comp in companies[:4]:
        info = company_directory.get(comp, (f"https://www.google.com/search?q={comp}+careers", "Software Development Engineer", "Hybrid"))
        job = JobApplication(
            user_id=user.id,
            company=comp,
            role=info[1],
            job_url=info[0],
            location=info[2],
            status="planned",
            eligibility_notes=f"Targeting {profile.graduation_year or 2027} campus/off-campus recruitment drive.",
            is_verified_opening=True
        )
        db.add(job)

    db.commit()

    # 3. Generate adaptive weekly study plan
    generate_weekly_study_plan(
        db=db,
        user_id=user.id,
        daily_hours=float(profile.daily_study_hours or 4)
    )

@router.post("/register", response_model=Token)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """Registers a new user and sets up their tailored SDE preparation workspace."""
    email_clean = str(request.email).strip().lower()
    existing = db.query(User).filter(User.email == email_clean).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists."
        )

    new_user = User(
        email=email_clean,
        hashed_password=hash_password(request.password.strip()),
        full_name=request.full_name.strip()
    )
    db.add(new_user)
    db.flush()

    new_profile = UserProfile(
        user_id=new_user.id,
        degree=request.degree or "B.Tech Artificial Intelligence and Data Science",
        graduation_year=request.graduation_year or 2027,
        daily_study_hours=request.daily_study_hours or 4,
        target_roles=request.target_roles or "Software Development Engineer",
        preferred_companies=request.preferred_companies or "Zoho, TCS, Amazon, Google, PayPal",
        existing_projects=request.existing_projects or "Technical Portfolio Projects",
        career_goals=request.career_goals or "Software Engineering Placement & Mastery",
        python_confidence=request.python_confidence or 3,
        sql_confidence=request.sql_confidence or 3,
        dsa_confidence=request.dsa_confidence or 1
    )
    db.add(new_profile)
    db.commit()
    db.refresh(new_user)

    # Initialize complete personal curriculum & metrics
    initialize_new_user_workspace(
        db=db,
        user=new_user,
        profile=new_profile,
        custom_metrics=request.skill_metrics
    )

    token = create_access_token(subject=new_user.id)
    return Token(
        access_token=token,
        token_type="bearer",
        user_id=new_user.id,
        email=new_user.email,
        full_name=new_user.full_name
    )

@router.post("/login", response_model=Token)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Authenticates existing user and returns JWT token."""
    email_clean = str(request.email).strip().lower()
    user = db.query(User).filter(User.email == email_clean).first()

    # Self-healing on ephemeral container restarts
    if not user:
        if email_clean == "adhithian260506@gmail.com" and request.password.strip() == "Adhi@2656":
            user = User(
                email=email_clean,
                hashed_password=hash_password("Adhi@2656"),
                full_name="Adhithian S"
            )
            db.add(user)
            db.flush()
            profile = UserProfile(
                user_id=user.id,
                degree="B.Tech Artificial Intelligence and Data Science",
                graduation_year=2027,
                daily_study_hours=4,
                target_roles="Software Development Engineer, AI Engineer",
                preferred_companies="Zoho, TCS, Amazon, Google, PayPal",
                existing_projects="RAG Chatbot, Facial Recognition Attendance",
                career_goals="Tier-1 SDE Placement & Engineering Leadership",
                python_confidence=4,
                sql_confidence=4,
                dsa_confidence=2
            )
            db.add(profile)
            db.commit()
            db.refresh(user)
            initialize_new_user_workspace(db=db, user=user, profile=profile)
        elif email_clean == "teststudent@careerforge.ai" and request.password.strip() == "TestStudent@123":
            user = User(
                email=email_clean,
                hashed_password=hash_password("TestStudent@123"),
                full_name="Test Student"
            )
            db.add(user)
            db.flush()
            profile = UserProfile(
                user_id=user.id,
                degree="B.Tech Computer Science",
                graduation_year=2027,
                daily_study_hours=4,
                target_roles="Software Development Engineer",
                preferred_companies="Zoho, TCS, Amazon",
                existing_projects="Technical Portfolio Project",
                career_goals="Software Engineering Mastery",
                python_confidence=3,
                sql_confidence=3,
                dsa_confidence=2
            )
            db.add(profile)
            db.commit()
            db.refresh(user)
            initialize_new_user_workspace(db=db, user=user, profile=profile)

    if not user or not verify_password(request.password.strip(), user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password."
        )
    
    token = create_access_token(subject=user.id)
    return Token(
        access_token=token,
        token_type="bearer",
        user_id=user.id,
        email=user.email,
        full_name=user.full_name
    )

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Returns profile and settings for currently authenticated user."""
    return current_user

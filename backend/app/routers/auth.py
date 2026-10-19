from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.user import User, UserProfile
from backend.app.schemas.auth import Token, LoginRequest, RegisterRequest
from backend.app.schemas.user import UserResponse
from backend.app.utils.security import verify_password, hash_password, create_access_token
from backend.app.services.auth_service import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """Registers a new user and creates their tailored profile."""
    existing = db.query(User).filter(User.email == request.email.lower()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists."
        )

    new_user = User(
        email=request.email.lower(),
        hashed_password=hash_password(request.password),
        full_name=request.full_name
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
        python_confidence=request.python_confidence or 3,
        sql_confidence=request.sql_confidence or 3,
        dsa_confidence=request.dsa_confidence or 1
    )
    db.add(new_profile)
    db.commit()
    db.refresh(new_user)

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
    user = db.query(User).filter(User.email == request.email.lower()).first()
    if not user or not verify_password(request.password, user.hashed_password):
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

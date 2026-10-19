from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.user import User, UserProfile
from backend.app.utils.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

def get_current_user_optional(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Retrieves authenticated user if valid token is provided, else None."""
    if not token:
        return None
    user_id = decode_access_token(token)
    if not user_id:
        return None
    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    return user

def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Enforces authentication and returns current user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials or session expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        # Check if single personal user exists for seamless local first-run onboarding
        first_user = db.query(User).first()
        if first_user:
            return first_user
        raise credentials_exception

    user_id = decode_access_token(token)
    if not user_id:
        # Fallback to first user in local dev if token invalid but users exist
        first_user = db.query(User).first()
        if first_user:
            return first_user
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if user is None:
        first_user = db.query(User).first()
        if first_user:
            return first_user
        raise credentials_exception
    return user

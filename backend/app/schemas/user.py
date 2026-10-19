from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserProfileBase(BaseModel):
    degree: str
    graduation_year: int
    daily_study_hours: int
    target_roles: str
    preferred_companies: str
    python_confidence: int
    sql_confidence: int
    dsa_confidence: int
    existing_projects: str
    career_goals: str

class UserProfileUpdate(BaseModel):
    degree: Optional[str] = None
    graduation_year: Optional[int] = None
    daily_study_hours: Optional[int] = None
    target_roles: Optional[str] = None
    preferred_companies: Optional[str] = None
    python_confidence: Optional[int] = None
    sql_confidence: Optional[int] = None
    dsa_confidence: Optional[int] = None
    existing_projects: Optional[str] = None
    career_goals: Optional[str] = None

class UserProfileResponse(UserProfileBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    is_active: bool
    is_admin: bool
    profile: Optional[UserProfileResponse] = None
    created_at: datetime

    class Config:
        from_attributes = True

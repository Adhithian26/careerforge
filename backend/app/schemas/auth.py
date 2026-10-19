from typing import Optional
from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str
    full_name: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    degree: Optional[str] = "B.Tech Artificial Intelligence and Data Science"
    graduation_year: Optional[int] = 2027
    daily_study_hours: Optional[int] = 4
    python_confidence: Optional[int] = 3
    sql_confidence: Optional[int] = 3
    dsa_confidence: Optional[int] = 1
    target_roles: Optional[str] = "Software Development Engineer"
    preferred_companies: Optional[str] = "Zoho, TCS, Amazon, Google, PayPal, Tech Mahindra"

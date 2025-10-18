from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Auth Schemas
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    age: int
    weight: float
    height: float
    fitness_level: str  # beginner, intermediate, advanced

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    fitness_level: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    fitness_level: Optional[str] = None

# Progress Schemas
class ProgressResponse(BaseModel):
    level: int
    current_exp: int
    exp_to_next_level: int
    total_exercises_completed: int
    current_week: int
    total_days: int
    completed_exercises: dict

    class Config:
        from_attributes = True

class ProgressUpdate(BaseModel):
    level: Optional[int] = None
    current_exp: Optional[int] = None
    exp_to_next_level: Optional[int] = None
    total_exercises_completed: Optional[int] = None
    current_week: Optional[int] = None
    total_days: Optional[int] = None
    completed_exercises: Optional[dict] = None

from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from datetime import date
from .user import UserProfile
class ExerciseType(str, Enum):
    STRENGTH = "strength"
    CARDIO = "cardio"
    FLEXIBILITY = "flexibility"
    WARMUP = "warmup"
    COOLDOWN = "cooldown"
    CORE = "core"

class Exercise(BaseModel):
    name: str
    type: ExerciseType
    sets: Optional[int] = None
    reps: Optional[int] = None
    duration: Optional[int] = None  # seconds
    rest: Optional[int] = None  # seconds between sets
    equipment: Optional[str] = None
    instructions: Optional[str] = None

class WorkoutDay(BaseModel):
    day: int  # 1, 2, 3, etc.
    focus: str  # "Upper Body", "Lower Body", "Cardio", etc.
    exercises: List[Exercise]
    total_duration: int

class WorkoutWeek(BaseModel):
    week: int  # 1, 2, 3, 4
    daily_schedule: List[WorkoutDay]

class WorkoutPlan(BaseModel):
    id: str
    user_profile: UserProfile
    generated_date: date
    duration_weeks: int
    weekly_schedule: List[WorkoutDay]
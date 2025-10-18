from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class FitnessLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class Goal(str, Enum):
    WEIGHT_LOSS = "weight_loss"
    MUSCLE_GAIN = "muscle_gain"
    MAINTENANCE = "maintenance"
    ENDURANCE = "endurance"

class UserProfile(BaseModel):
    age: int
    weight: float  # kg
    height: float  # cm
    fitness_level: FitnessLevel
    goal: Goal
    available_equipment: List[str]
    workout_duration: int  # minutes
    days_per_week: int
    injuries: Optional[List[str]] = []
    preferences: Optional[List[str]] = []
# app/models/__init__.py
from .user import UserProfile, FitnessLevel, Goal
from .workout import WorkoutPlan, Exercise, ExerciseType

# Now you can import directly from models:
# from app.models import UserProfile, WorkoutPlan
# instead of:
# from app.models.user import UserProfile
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # User profile data
    age = Column(Integer, nullable=True)
    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    fitness_level = Column(String, nullable=True)  # beginner, intermediate, advanced

    # Relationships
    progress = relationship("UserProgress", back_populates="user", uselist=False)
    workouts = relationship("WorkoutPlan", back_populates="user")

class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    # Gamification stats
    level = Column(Integer, default=1)
    current_exp = Column(Integer, default=0)
    exp_to_next_level = Column(Integer, default=100)
    total_exercises_completed = Column(Integer, default=0)
    current_week = Column(Integer, default=0)
    total_days = Column(Integer, default=0)

    # Completed exercises stored as JSON
    # Format: {"week1-day1-exercise0": true, ...}
    completed_exercises = Column(JSON, default={})

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    user = relationship("User", back_populates="progress")

class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    # Workout plan data stored as JSON
    plan_data = Column(JSON, nullable=False)
    week_number = Column(Integer, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    user = relationship("User", back_populates="workouts")

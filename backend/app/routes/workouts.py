from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.db_models import WorkoutPlan, User
from app.auth import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/workouts", tags=["workouts"])

class WorkoutCreate(BaseModel):
    plan_data: dict
    week_number: int

class WorkoutResponse(BaseModel):
    id: int
    plan_data: dict
    week_number: int

    class Config:
        from_attributes = True

@router.post("/", response_model=WorkoutResponse, status_code=status.HTTP_201_CREATED)
async def save_workout(
    workout: WorkoutCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Save or update the user's current workout plan"""
    # Delete any existing current workout for this user
    db.query(WorkoutPlan).filter(WorkoutPlan.user_id == current_user.id).delete()

    # Create new workout
    new_workout = WorkoutPlan(
        user_id=current_user.id,
        plan_data=workout.plan_data,
        week_number=workout.week_number
    )

    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)

    return new_workout

@router.get("/current", response_model=Optional[WorkoutResponse])
async def get_current_workout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get the user's current workout plan"""
    workout = db.query(WorkoutPlan).filter(
        WorkoutPlan.user_id == current_user.id
    ).order_by(WorkoutPlan.created_at.desc()).first()

    return workout

@router.delete("/current", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_workout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete the user's current workout plan"""
    db.query(WorkoutPlan).filter(WorkoutPlan.user_id == current_user.id).delete()
    db.commit()

    return None

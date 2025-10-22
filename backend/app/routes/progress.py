from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.db_models import User, UserProgress
from app.models.schemas import ProgressResponse, ProgressUpdate
from app.auth import get_current_user

router = APIRouter(prefix="/progress", tags=["progress"])

@router.get("/", response_model=ProgressResponse)
def get_user_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's progress"""
    progress = db.query(UserProgress).filter(UserProgress.user_id == current_user.id).first()

    if not progress:
        #Create initial progress if doesn't exist
        progress = UserProgress(
            user_id=current_user.id,
            level=1,
            current_exp=0,
            exp_to_next_level=100,
            total_exercises_completed=0,
            current_week=0,
            total_days=0,
            completed_exercises={}
        )
        db.add(progress)
        db.commit()
        db.refresh(progress)

    return progress

@router.put("/", response_model=ProgressResponse)
def update_user_progress(
    progress_update: ProgressUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user's progress"""
    progress = db.query(UserProgress).filter(UserProgress.user_id == current_user.id).first()

    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progress not found"
        )

    #Update only provided fields
    update_data = progress_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(progress, field, value)

    db.commit()
    db.refresh(progress)

    return progress

@router.delete("/")
def reset_user_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Reset user's progress to initial state"""
    progress = db.query(UserProgress).filter(UserProgress.user_id == current_user.id).first()

    if progress:
        progress.level = 1
        progress.current_exp = 0
        progress.exp_to_next_level = 100
        progress.total_exercises_completed = 0
        progress.current_week = 0
        progress.total_days = 0
        progress.completed_exercises = {}

        db.commit()

    return {"message": "Progress reset successfully"}

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.database import get_db
from app.models.db_models import User, UserProgress
from app.auth import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])

class LeaderboardEntry(BaseModel):
    rank: int
    username: str
    level: int
    current_exp: int
    total_exercises_completed: int

    class Config:
        from_attributes = True

class LeaderboardResponse(BaseModel):
    top_users: List[LeaderboardEntry]
    current_user_rank: LeaderboardEntry | None

@router.get("/", response_model=LeaderboardResponse)
async def get_leaderboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get top 10 users by level and exp, plus current user's rank"""

    # Get all users with their progress, sorted by level desc, then exp desc
    all_users = db.query(
        User.username,
        UserProgress.level,
        UserProgress.current_exp,
        UserProgress.total_exercises_completed,
        User.id
    ).join(
        UserProgress, User.id == UserProgress.user_id
    ).order_by(
        UserProgress.level.desc(),
        UserProgress.current_exp.desc()
    ).all()

    # Create ranked list
    ranked_users = []
    current_user_entry = None

    for idx, user in enumerate(all_users, start=1):
        entry = LeaderboardEntry(
            rank=idx,
            username=user.username,
            level=user.level,
            current_exp=user.current_exp,
            total_exercises_completed=user.total_exercises_completed
        )

        # Store top 10
        if idx <= 10:
            ranked_users.append(entry)

        # Store current user's rank
        if user.id == current_user.id:
            current_user_entry = entry

    return LeaderboardResponse(
        top_users=ranked_users,
        current_user_rank=current_user_entry
    )

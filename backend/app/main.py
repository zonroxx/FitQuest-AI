from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uuid
from datetime import date
from dotenv import load_dotenv
from sqlalchemy.orm import Session

#Load environment variables from .env file
load_dotenv()

from app.models.user import UserProfile
from app.models.workout import WorkoutPlan, WorkoutDay
from app.services.ai_workout_generator import AIWorkoutGenerator
from app.database import engine, get_db, Base
from app.routes import auth, progress, workouts, leaderboard
from app.auth import get_current_user
from app.models.db_models import User

#Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FitQuest API")

#CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Include routers
app.include_router(auth.router)
app.include_router(progress.router)
app.include_router(workouts.router)
app.include_router(leaderboard.router)

#In-memory storage (replace with database later)
workout_plans = {}

@app.post("/generate-workout", response_model=WorkoutPlan)
async def generate_workout_plan(
    user_profile: UserProfile,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    generator = AIWorkoutGenerator()
    workout_plan = generator.generate_workout_plan(user_profile)

    #Store the plan (keeping in-memory for now, can be moved to DB later)
    workout_plans[workout_plan.id] = workout_plan

    return workout_plan

@app.get("/workout/{workout_id}", response_model=WorkoutPlan)
async def get_workout_plan(workout_id: str):
    if workout_id not in workout_plans:
        raise HTTPException(status_code=404, detail="Workout plan not found")
    return workout_plans[workout_id]

@app.post("/workout/{workout_id}/complete-exercise")
async def mark_exercise_complete(workout_id: str, day: int, exercise_name: str):
    #This will be used by the React todo list functionality
    if workout_id not in workout_plans:
        raise HTTPException(status_code=404, detail="Workout plan not found")
    
    #Implementation for tracking completed exercises
    return {"message": "Exercise marked as completed"}

@app.get("/")
async def root():
    return {"message": "AI Workout Planner API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
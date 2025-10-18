# FitQuest

A gamified AI-powered workout planner that helps users achieve their fitness goals through personalized workout plans and progression tracking.

## About

FitQuest combines AI-generated personalized workout plans with gamification mechanics to keep users motivated. Users gain experience points by completing exercises, level up through consistent training, and compete on a leaderboard.

## Key Features

- AI-generated personalized workout plans based on user fitness level, goals, and available equipment
- Gamification system with levels and experience points
- User authentication and profile management
- Week-based workout progression with exercise tracking
- Leaderboard to compete with other users
- Responsive design with monochromatic theme

## Tech Stack

### Backend
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT authentication
- Bcrypt password hashing
- Hugging Face API

### Frontend
- React
- CSS Variables
- Fetch API

## Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 16+
- PostgreSQL 14+

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file in backend directory with:
```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/fitquest
SECRET_KEY=your_secret_key_here
HUGGINGFACE_API_TOKEN=your_huggingface_token_here
```

5. Create database:
```bash
createdb fitquest
```

6. Start the server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm start
```

The application will open at `http://localhost:3000`

## Database Schema

The application uses three main tables:

- **users** - Authentication and profile data
- **user_progress** - Gamification stats and completed exercises
- **workout_plans** - AI-generated workout plans

## API Endpoints

### Authentication
- `POST /auth/signup` - Create new account
- `POST /auth/login` - User login
- `GET /auth/me` - Get user profile
- `PUT /auth/me` - Update profile

### Progress
- `GET /progress/` - Get user progress
- `PUT /progress/` - Update progress
- `DELETE /progress/` - Reset progress

### Workouts
- `POST /generate-workout` - Generate new workout
- `POST /workouts/` - Save workout
- `GET /workouts/current` - Get current workout
- `DELETE /workouts/current` - Delete workout

### Leaderboard
- `GET /leaderboard/` - Get rankings

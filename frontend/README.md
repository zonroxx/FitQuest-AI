# FitQuest Frontend

React-based frontend for the FitQuest AI-powered workout planner application.

## Features

- Day-by-day workout view
- Exercise completion tracking
- Progress bar with level and XP system
- User authentication (login/signup)
- User profile management
- Leaderboard rankings
- Responsive design

## Setup

1. Install dependencies:

```bash
npm install
```

2. Start the development server:

```bash
npm start
```

The application will open at http://localhost:3000

## API Integration

The frontend connects to the FastAPI backend running on `http://localhost:8000`

Endpoints used:

- `/auth/signup` - User registration
- `/auth/login` - User authentication
- `/auth/me` - Get/update user profile
- `/generate-workout` - Generate AI workout plan
- `/progress/` - Get/update user progress
- `/workouts/` - Save/retrieve workouts
- `/leaderboard/` - Get user rankings

## Technologies

- React
- CSS Variables for theming
- Fetch API for HTTP requests
- Local storage for token persistence

## Available Scripts

- `npm start` - Run development server
- `npm build` - Build for production
- `npm test` - Run tests

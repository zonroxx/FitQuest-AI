# FitQuest Frontend Prototype

A simple React prototype for displaying AI-generated workouts in a todo list format.

## Features

- 📅 Day-by-day workout view
- ✅ Todo-style exercise checklist
- 📊 Progress tracking with visual progress bar
- 🎯 Exercise categorization with icons
- 📱 Responsive design

## Quick Start

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm start
```

3. Open http://localhost:3000 in your browser

## Structure

- `App.js` - Main component with sample workout data
- `components/WorkoutTodoList.js` - Daily workout display with progress tracking
- `components/ExerciseItem.js` - Individual exercise item with completion status
- `App.css` - Styling for the entire application

## Sample Data

The prototype uses sample data matching your AI workout generator format. To connect with real data, replace the `sampleWorkout` in `App.js` with API calls to your backend.
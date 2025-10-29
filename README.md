## Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/zonroxx/FitQuest-AI.git
cd FitQuest-AI
```

### Step 2: Database Setup

1. Install PostgreSQL if you haven't already

2. Create a new database:
```bash
createdb fitquest
```

Or using PostgreSQL command line:
```sql
CREATE DATABASE fitquest;
```

### Step 3: Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file in the backend directory:
```bash
# backend/.env - This is important, I didn't include the .env file from our project because that includes sensitive information such as my huggingface API, secretkey, and database password.
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/fitquest
SECRET_KEY=your_secret_key_here
HUGGINGFACE_API_TOKEN=your_huggingface_token_here
```

**Important Notes:**
- Replace `your_password` with your PostgreSQL password
- Generate a secure SECRET_KEY (you can use: `python -c "import secrets; print(secrets.token_hex(32))"`)
- For Hugging Face API token:
  1. Create a free account at https://huggingface.co/join
  2. Go to https://huggingface.co/settings/tokens
  3. Click "Create new token"
  4. Name it "FitQuest" and select "Read" as token type
  5. Copy the token and paste it in your `.env` file

6. The database tables will be created automatically when you start the server

### Step 4: Frontend Setup

1. Open a new terminal and navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

## Running the Application

You need to run both backend and frontend servers simultaneously.

### Terminal 1 - Backend Server

```bash
cd backend
venv\Scripts\activate  #for Windows
source venv/bin/activate  #for MacOS/Linux
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at: http://localhost:8000

### Terminal 2 - Frontend Server (Open a new terminal [Do not close the backend terminal])

```bash
cd frontend
npm start
```

The frontend application will automatically open at: http://localhost:3000

## Using the Application

1. **Sign Up**: Create a new account with your email, username, password, and fitness details (age, weight, height, fitness level) (please do not use any similar passwords with your other accounts. Although the passwords are hashed, it is better to take causion)

2. **Generate Workout**: After signing up, you'll be prompted to generate your first workout plan by selecting:
   - Goal (weight loss, muscle gain, maintenance, endurance)
   - Workout duration (15-120 minutes)
   - Days per week (1-7 days)
   - Available equipment

3. **Complete Exercises**: Mark exercises as complete to gain XP and level up

4. **View Progress**: See your level, XP, and progress bar at the top of the page

5. **Check Leaderboard**: Click the "Leaderboard" button to see top 10 users and your rank

6. **Manage Profile**: Click "Profile" to view and edit your fitness information

## Project Structure

```
FitQuest/
├── backend/
│   ├── app/
│   │   ├── models/          # Database models and schemas
│   │   ├── routes/          # API endpoints
│   │   ├── services/        # Business logic
│   │   ├── auth.py          # JWT authentication
│   │   ├── database.py      # Database configuration
│   │   └── main.py          # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # You have to create the env file yourself as it is not included in the github repo
|                            # .env file is IMPORTANT and the AI generation won't work without it
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── utils/           # Utility functions
│   │   ├── App.js           # Main app component
│   │   ├── App.css          # Styles
│   │   └── index.js         # Entry point
│   └── package.json         # Node dependencies
└── README.md
```

## Database Schema

The application uses three main tables:

- **users**: Authentication and profile data (email, username, password, age, weight, height, fitness_level)
- **user_progress**: Gamification stats (level, XP, completed exercises, weeks, days)
- **workout_plans**: AI-generated workout plans stored as JSON

## Troubleshooting

### Backend won't start
- Make sure PostgreSQL is running
- Verify database credentials in `.env` file
- Check if port 8000 is already in use

### Frontend won't start
- Delete `node_modules` and run `npm install` again
- Check if port 3000 is already in use
- Clear browser cache

### Database connection error
- Verify PostgreSQL is running: `pg_isready`
- Check database exists: `psql -l | grep fitquest`
- Verify credentials in `.env` file

### Can't generate workouts
- Check if Hugging Face API token is valid
- App will use fallback generator if AI fails
- Check backend console for error messages

## Environment Variables

Create a `.env` file in the `backend` directory with:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/fitquest
SECRET_KEY=your-secret-key-here
HUGGINGFACE_API_TOKEN=your-huggingface-token-here
```

**Note**: The `.env` file is gitignored and should never be committed to version control.

## License

MIT License

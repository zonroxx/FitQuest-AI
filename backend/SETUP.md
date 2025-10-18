# FitQuest Backend Setup

## PostgreSQL Installation & Setup

### 1. Install PostgreSQL

**Windows:**
- Download PostgreSQL from https://www.postgresql.org/download/windows/
- Run the installer
- Remember the password you set for the `postgres` user
- Default port is 5432

**Mac:**
```bash
brew install postgresql
brew services start postgresql
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### 2. Create the Database

Open PostgreSQL command line (psql):

**Windows:**
- Open "SQL Shell (psql)" from Start Menu
- Press Enter for default values, enter your postgres password

**Mac/Linux:**
```bash
psql -U postgres
```

Then run:
```sql
CREATE DATABASE fitquest;
```

Exit psql:
```
\q
```

### 3. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Configure Environment Variables

1. Copy `.env.example` to `.env`:
```bash
copy .env.example .env   # Windows
cp .env.example .env     # Mac/Linux
```

2. Edit `.env` and update:
```
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/fitquest
SECRET_KEY=generate-a-random-secret-key
```

To generate a secure secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. Run the Backend

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The tables will be created automatically when the app starts!

## API Endpoints

### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/login` - Login and get token
- `GET /auth/me` - Get current user info

### Progress
- `GET /progress/` - Get user progress
- `PUT /progress/` - Update user progress
- `DELETE /progress/` - Reset progress

### Workouts
- `POST /generate-workout` - Generate workout plan (requires authentication)

## Testing with cURL

### Register a user:
```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"password123"}'
```

### Login:
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

This returns a token. Use it in subsequent requests:

### Get user info:
```bash
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

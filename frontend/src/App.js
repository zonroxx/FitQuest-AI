import React, { useState, useEffect } from 'react';
import WorkoutTodoList from './components/WorkoutTodoList';
import UserProgress from './components/UserProgress';
import UserProfile from './components/UserProfile';
import Leaderboard from './components/Leaderboard';
import Login from './components/Login';
import Signup from './components/Signup';
import { getInitialProgress, saveProgress, processLevelUp } from './utils/progressSystem';
import './App.css';

// Use environment variable for API URL, fallback to localhost for local development
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [showLogin, setShowLogin] = useState(true);
  const [token, setToken] = useState(null);
  const [userProfile, setUserProfile] = useState(null);
  const [showProfile, setShowProfile] = useState(false);
  const [showLeaderboard, setShowLeaderboard] = useState(false);

  const [selectedDay, setSelectedDay] = useState(1);
  const [workout, setWorkout] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false); // Changed to false - only show if no workout
  const [showEquipmentPopup, setShowEquipmentPopup] = useState(false);
  const [userProgress, setUserProgress] = useState(getInitialProgress());
  const [workoutStartDay, setWorkoutStartDay] = useState(0); // Track starting day for current workout

  // Fetch user profile from backend with retry logic for cold starts
  const fetchUserProfile = async (authToken, retries = 3, delay = 2000) => {
    for (let attempt = 1; attempt <= retries; attempt++) {
      try {
        console.log(`Fetching user profile (attempt ${attempt}/${retries})...`);
        const response = await fetch(`${API_URL}/auth/me`, {
          headers: {
            'Authorization': `Bearer ${authToken}`
          }
        });

        if (response.ok) {
          const profile = await response.json();
          console.log('Fetched user profile:', profile);
          setUserProfile(profile);
          return; // Success, exit retry loop
        } else if (attempt < retries) {
          console.log(`Profile fetch failed, retrying in ${delay}ms...`);
          await new Promise(resolve => setTimeout(resolve, delay));
          delay *= 1.5; // Exponential backoff
        }
      } catch (error) {
        console.error(`Error fetching user profile (attempt ${attempt}):`, error);
        if (attempt < retries) {
          console.log(`Retrying in ${delay}ms...`);
          await new Promise(resolve => setTimeout(resolve, delay));
          delay *= 1.5; // Exponential backoff
        }
      }
    }
    console.error('Failed to fetch user profile after all retries');
  };

  // Fetch user's current workout from backend with retry logic for cold starts
  const fetchCurrentWorkout = async (authToken, retries = 3, delay = 2000) => {
    for (let attempt = 1; attempt <= retries; attempt++) {
      try {
        console.log(`Fetching current workout (attempt ${attempt}/${retries})...`);
        const response = await fetch(`${API_URL}/workouts/current`, {
          headers: {
            'Authorization': `Bearer ${authToken}`
          }
        });

        if (response.ok) {
          const workoutData = await response.json();
          if (workoutData && workoutData.plan_data) {
            console.log('Fetched current workout:', workoutData);
            setWorkout(workoutData.plan_data);
            setShowForm(false);
            // Calculate workout start day based on saved week number
            const daysInWorkout = workoutData.plan_data.weekly_schedule ? workoutData.plan_data.weekly_schedule.length : 0;
            const startDay = (workoutData.week_number - 1) * daysInWorkout;
            setWorkoutStartDay(startDay);
            return; // Success, exit retry loop
          } else {
            setShowForm(true);
            return; // No workout found, exit retry loop
          }
        } else if (attempt < retries) {
          console.log(`Workout fetch failed, retrying in ${delay}ms...`);
          await new Promise(resolve => setTimeout(resolve, delay));
          delay *= 1.5; // Exponential backoff
        } else {
          setShowForm(true);
        }
      } catch (error) {
        console.error(`Error fetching current workout (attempt ${attempt}):`, error);
        if (attempt < retries) {
          console.log(`Retrying in ${delay}ms...`);
          await new Promise(resolve => setTimeout(resolve, delay));
          delay *= 1.5; // Exponential backoff
        } else {
          setShowForm(true);
        }
      }
    }
    console.error('Failed to fetch current workout after all retries');
  };

  // Fetch user progress from backend with retry logic for cold starts
  const fetchUserProgress = async (authToken, retries = 3, delay = 2000) => {
    for (let attempt = 1; attempt <= retries; attempt++) {
      try {
        console.log(`Fetching user progress (attempt ${attempt}/${retries})...`);
        const response = await fetch(`${API_URL}/progress/`, {
          headers: {
            'Authorization': `Bearer ${authToken}`
          }
        });

        if (response.ok) {
          const progress = await response.json();
          console.log('Fetched progress:', progress);
          // Ensure all fields exist with defaults
          const completeProgress = {
            level: progress.level || 1,
            current_exp: progress.current_exp || 0,
            currentExp: progress.current_exp || 0,
            exp_to_next_level: progress.exp_to_next_level || 100,
            expToNextLevel: progress.exp_to_next_level || 100,
            total_exercises_completed: progress.total_exercises_completed || 0,
            totalExercisesCompleted: progress.total_exercises_completed || 0,
            current_week: progress.current_week || 0,
            currentWeek: progress.current_week || 0,
            total_days: progress.total_days || 0,
            totalDays: progress.total_days || 0,
            completed_exercises: progress.completed_exercises || {},
            completedExercises: progress.completed_exercises || {}
          };
          setUserProgress(completeProgress);
          return; // Success, exit retry loop
        } else if (attempt < retries) {
          console.log(`Progress fetch failed, retrying in ${delay}ms...`);
          await new Promise(resolve => setTimeout(resolve, delay));
          delay *= 1.5; // Exponential backoff
        }
      } catch (error) {
        console.error(`Error fetching user progress (attempt ${attempt}):`, error);
        if (attempt < retries) {
          console.log(`Retrying in ${delay}ms...`);
          await new Promise(resolve => setTimeout(resolve, delay));
          delay *= 1.5; // Exponential backoff
        }
      }
    }
    console.error('Failed to fetch user progress after all retries');
  };

  // Check for existing token on mount
  useEffect(() => {
    const savedToken = localStorage.getItem('token');
    if (savedToken) {
      setToken(savedToken);
      setIsAuthenticated(true);
      fetchUserProgress(savedToken);
      fetchUserProfile(savedToken);
      fetchCurrentWorkout(savedToken);
    }
  }, []);

  // Form state - only contains workout-specific fields
  // User profile data (age, weight, height, fitness_level) will come from userProfile
  const [formData, setFormData] = useState({
    goal: "weight_loss",
    available_equipment: [],
    workout_duration: 30,
    days_per_week: 3,
    injuries: [],
    preferences: []
  });

  const goals = [
    { value: "weight_loss", label: "Weight Loss" },
    { value: "muscle_gain", label: "Muscle Gain" },
    { value: "maintenance", label: "Maintenance" },
    { value: "endurance", label: "Endurance" }
  ];

  const equipmentOptions = [
    "dumbbells",
    "barbells",
    "resistance_bands",
    "kettlebells",
    "pull_up_bar",
    "yoga_mat",
    "bodyweight",
    "treadmill",
    "stationary_bike"
  ];

  const handleInputChange = (e) => {
    const { name, value, type } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'number' ? parseFloat(value) || 0 : value
    }));
  };

  const handleEquipmentChange = (equipment) => {
    setFormData(prev => ({
      ...prev,
      available_equipment: prev.available_equipment.includes(equipment)
        ? prev.available_equipment.filter(item => item !== equipment)
        : [...prev.available_equipment, equipment]
    }));
  };

  // Save progress to backend whenever it changes
  useEffect(() => {
    const syncProgress = async () => {
      if (token && isAuthenticated && userProgress.level) {
        try {
          // Convert camelCase to snake_case for backend
          const backendProgress = {
            level: userProgress.level,
            current_exp: userProgress.currentExp,
            exp_to_next_level: userProgress.expToNextLevel,
            total_exercises_completed: userProgress.totalExercisesCompleted,
            current_week: userProgress.currentWeek,
            total_days: userProgress.totalDays,
            completed_exercises: userProgress.completedExercises
          };

          await fetch(`${API_URL}/progress/`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(backendProgress)
          });
        } catch (error) {
          console.error('Error syncing progress:', error);
        }
      }
    };

    syncProgress();
  }, [userProgress, token, isAuthenticated]);

  const handleExpGain = (expGained, exerciseKey) => {
    setUserProgress(prev => {
      const newExp = prev.currentExp + expGained;
      const result = processLevelUp(prev.level, newExp);

      return {
        ...prev,
        level: result.level,
        currentExp: result.exp,
        expToNextLevel: result.expToNextLevel,
        totalExercisesCompleted: prev.totalExercisesCompleted + 1,
        completedExercises: {
          ...prev.completedExercises,
          [exerciseKey]: true
        }
      };
    });
  };

  const handleLevelUp = () => {
    // This is called when the user levels up - can add additional effects here
    console.log(`Congratulations! You reached level ${userProgress.level}!`);
  };

  const handleResetProgress = async () => {
    if (window.confirm('Are you sure you want to reset all progress? This will clear your level, XP, weeks, completed exercises, and current workout.')) {
      try {
        // Reset progress on backend
        await fetch(`${API_URL}/progress/`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        // Delete current workout from backend
        await fetch(`${API_URL}/workouts/current`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        // Reset local state
        const resetProgress = {
          level: 1,
          currentExp: 0,
          expToNextLevel: 100,
          totalExercisesCompleted: 0,
          completedExercises: {},
          currentWeek: 0,
          totalDays: 0
        };
        setUserProgress(resetProgress);
        setWorkout(null);
        setShowForm(true);
        setWorkoutStartDay(0);
      } catch (error) {
        console.error('Error resetting progress:', error);
      }
    }
  };

  const handleLogin = (accessToken) => {
    localStorage.setItem('token', accessToken);
    setToken(accessToken);
    setIsAuthenticated(true);
    fetchUserProgress(accessToken);
    fetchUserProfile(accessToken);
    fetchCurrentWorkout(accessToken);
  };

  const handleSignup = (accessToken) => {
    localStorage.setItem('token', accessToken);
    setToken(accessToken);
    setIsAuthenticated(true);
    fetchUserProgress(accessToken);
    fetchUserProfile(accessToken);
    setShowForm(true); // New users need to create their first workout
  };

  const handleLogout = () => {
    // Clear all localStorage data to prevent mixing user data
    localStorage.clear();
    setToken(null);
    setIsAuthenticated(false);
    setWorkout(null);
    setShowForm(true);
    setUserProfile(null);
    setUserProgress(getInitialProgress());
  };

  const handleProfileUpdate = (updatedProfile) => {
    setUserProfile(updatedProfile);
  };

  const generateWorkout = async () => {
    try {
      setIsLoading(true);
      setError(null);

      // Get the latest token from localStorage to ensure we have it
      const currentToken = localStorage.getItem('token') || token;

      if (!currentToken) {
        throw new Error('No authentication token found. Please log in again.');
      }

      if (!userProfile) {
        throw new Error('User profile not loaded. Please refresh the page.');
      }

      // Combine form data with user profile data
      const workoutRequest = {
        ...formData,
        age: userProfile.age,
        weight: userProfile.weight,
        height: userProfile.height,
        fitness_level: userProfile.fitness_level
      };

      const response = await fetch(`${API_URL}/generate-workout`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${currentToken}`
        },
        body: JSON.stringify(workoutRequest)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const workoutPlan = await response.json();

      // Calculate the starting day number for this workout
      const daysInWorkout = workoutPlan.weekly_schedule ? workoutPlan.weekly_schedule.length : 0;
      const previousTotalDays = userProgress.totalDays;
      const newWeekNumber = userProgress.currentWeek + 1;

      setWorkout(workoutPlan);
      setShowForm(false);
      setSelectedDay(1);
      setWorkoutStartDay(previousTotalDays); // Store the starting day for this workout

      // Save workout to database
      try {
        await fetch(`${API_URL}/workouts/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${currentToken}`
          },
          body: JSON.stringify({
            plan_data: workoutPlan,
            week_number: newWeekNumber
          })
        });
      } catch (err) {
        console.error('Error saving workout to database:', err);
      }

      // Increment week number and total days when generating new workout
      setUserProgress(prev => ({
        ...prev,
        currentWeek: newWeekNumber,
        totalDays: prev.totalDays + daysInWorkout
      }));
    } catch (err) {
      console.error('Error fetching workout:', err);
      setError('Failed to generate workout. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  // Show login/signup if not authenticated
  if (!isAuthenticated) {
    if (showLogin) {
      return <Login onLogin={handleLogin} onSwitchToSignup={() => setShowLogin(false)} />;
    } else {
      return <Signup onSignup={handleSignup} onSwitchToLogin={() => setShowLogin(true)} />;
    }
  }

  return (
    <div className="App">
      <header className="app-header">
        <h1>FitQuest</h1>
        <p>{showForm ? 'Create Your Personalized Workout Plan' : 'Your AI-Generated Workout Plan'}</p>
        <div className="header-buttons">
          <button onClick={() => setShowLeaderboard(true)} className="leaderboard-btn">Leaderboard</button>
          <button onClick={() => setShowProfile(true)} className="profile-btn">Profile</button>
          <button onClick={handleLogout} className="logout-btn">Logout</button>
        </div>
      </header>

      {!showForm && (
        <UserProgress
          level={userProgress.level}
          currentExp={userProgress.currentExp}
          expToNextLevel={userProgress.expToNextLevel}
          onLevelUp={handleLevelUp}
        />
      )}

      {showEquipmentPopup && (
        <div className="popup-overlay" onClick={() => setShowEquipmentPopup(false)}>
          <div className="equipment-popup" onClick={(e) => e.stopPropagation()}>
            <div className="popup-header">
              <h3>Select Equipment</h3>
              <button
                className="close-popup"
                onClick={() => setShowEquipmentPopup(false)}
              >
                ×
              </button>
            </div>
            <div className="equipment-options">
              {equipmentOptions.map(equipment => (
                <label key={equipment} className="equipment-checkbox">
                  <input
                    type="checkbox"
                    checked={formData.available_equipment.includes(equipment)}
                    onChange={() => handleEquipmentChange(equipment)}
                  />
                  <span>{equipment.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}</span>
                </label>
              ))}
            </div>
            <div className="popup-footer">
              <button
                className="done-btn"
                onClick={() => setShowEquipmentPopup(false)}
              >
                Done
              </button>
            </div>
          </div>
        </div>
      )}

      {showForm ? (
        <div className="workout-form">
          <form onSubmit={(e) => { e.preventDefault(); generateWorkout(); }}>
            <div className="form-grid">
              <div className="form-group">
                <label htmlFor="goal">Goal</label>
                <select
                  id="goal"
                  name="goal"
                  value={formData.goal}
                  onChange={handleInputChange}
                  required
                >
                  {goals.map(goal => (
                    <option key={goal.value} value={goal.value}>
                      {goal.label}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="workout_duration">Workout Duration (minutes)</label>
                <input
                  type="number"
                  id="workout_duration"
                  name="workout_duration"
                  value={formData.workout_duration}
                  onChange={handleInputChange}
                  min="15"
                  max="120"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="days_per_week">Days per Week</label>
                <input
                  type="number"
                  id="days_per_week"
                  name="days_per_week"
                  value={formData.days_per_week}
                  onChange={handleInputChange}
                  min="1"
                  max="7"
                  required
                />
              </div>
            </div>

            <div className="form-group equipment-group">
              <label>Available Equipment</label>
              <div className="equipment-display">
                {formData.available_equipment.length > 0 ? (
                  <div className="selected-equipment">
                    {formData.available_equipment.map(equipment => (
                      <span key={equipment} className="equipment-tag">
                        {equipment.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                        <button
                          type="button"
                          className="remove-equipment"
                          onClick={() => handleEquipmentChange(equipment)}
                        >
                          ×
                        </button>
                      </span>
                    ))}
                  </div>
                ) : (
                  <p className="no-equipment">No equipment selected</p>
                )}
                <button
                  type="button"
                  className="add-equipment-btn"
                  onClick={() => setShowEquipmentPopup(true)}
                >
                  Add Equipment
                </button>
              </div>
            </div>

            <div className="form-actions">
              <button
                type="submit"
                className="generate-btn"
                disabled={isLoading}
              >
                {isLoading ? 'Generating Workout...' : 'Generate My Workout Plan'}
              </button>

              {workout && (
                <button
                  type="button"
                  className="cancel-btn"
                  onClick={() => setShowForm(false)}
                  disabled={isLoading}
                >
                  Cancel
                </button>
              )}
            </div>

            {error && <div className="error">{error}</div>}
          </form>
        </div>
      ) : (
        <>
          <div className="workout-header">
            <div className="workout-actions">
              <button
                className="new-workout-btn"
                onClick={() => setShowForm(true)}
              >
                New Weekly Workout
              </button>
              <button
                className="reset-progress-btn"
                onClick={handleResetProgress}
              >
                Reset Progress
              </button>
            </div>
          </div>

          {workout && workout.weekly_schedule && (
            <>
              <div className="week-label">
                Week {userProgress.currentWeek}
              </div>

              <div className="day-selector">
                {workout.weekly_schedule.map((day) => {
                  const cumulativeDay = workoutStartDay + day.day;
                  return (
                    <button
                      key={day.day}
                      className={`day-btn ${selectedDay === day.day ? 'active' : ''}`}
                      onClick={() => setSelectedDay(day.day)}
                    >
                      Day {cumulativeDay}
                      <span className="day-focus">{day.focus}</span>
                    </button>
                  );
                })}
              </div>

              <WorkoutTodoList
                workout={workout.weekly_schedule.find(day => day.day === selectedDay)}
                onExpGain={handleExpGain}
                userProgress={userProgress}
                currentWeek={userProgress.currentWeek}
              />
            </>
          )}
        </>
      )}

      {showProfile && (
        <UserProfile
          userProfile={userProfile}
          token={token}
          onProfileUpdate={handleProfileUpdate}
          onClose={() => setShowProfile(false)}
        />
      )}

      {showLeaderboard && (
        <Leaderboard
          token={token}
          onClose={() => setShowLeaderboard(false)}
        />
      )}
    </div>
  );
}

export default App;
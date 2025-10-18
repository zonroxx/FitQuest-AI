// Calculate EXP required for the next level (exponential growth)
export const calculateExpForLevel = (level) => {
  // Base EXP is 100, grows by 50 per level
  return Math.floor(100 * Math.pow(1.5, level - 1));
};

// Calculate EXP gained from completing an exercise
export const calculateExpGain = (exercise) => {
  let baseExp = 10;

  // More EXP for strength exercises
  if (exercise.type === 'strength') {
    baseExp = 15;
  } else if (exercise.type === 'cardio') {
    baseExp = 12;
  } else if (exercise.type === 'core') {
    baseExp = 13;
  }

  // Bonus EXP for multiple sets
  if (exercise.sets > 1) {
    baseExp += exercise.sets * 2;
  }

  return baseExp;
};

// Check if user should level up and return new stats
export const processLevelUp = (currentLevel, currentExp) => {
  let level = currentLevel;
  let exp = currentExp;
  let expToNextLevel = calculateExpForLevel(level);
  let levelsGained = 0;

  // Handle multiple level-ups if enough EXP
  while (exp >= expToNextLevel) {
    exp -= expToNextLevel;
    level += 1;
    levelsGained += 1;
    expToNextLevel = calculateExpForLevel(level);
  }

  return {
    level,
    exp,
    expToNextLevel,
    levelsGained,
    didLevelUp: levelsGained > 0
  };
};

// Initialize user progress
export const getInitialProgress = () => {
  const saved = localStorage.getItem('fitquest_progress');
  if (saved) {
    try {
      return JSON.parse(saved);
    } catch (e) {
      console.error('Error loading progress:', e);
    }
  }

  return {
    level: 1,
    currentExp: 0,
    expToNextLevel: calculateExpForLevel(1),
    totalExercisesCompleted: 0,
    completedExercises: {},
    currentWeek: 0,
    totalDays: 0
  };
};

// Save user progress to localStorage
export const saveProgress = (progress) => {
  try {
    localStorage.setItem('fitquest_progress', JSON.stringify(progress));
  } catch (e) {
    console.error('Error saving progress:', e);
  }
};

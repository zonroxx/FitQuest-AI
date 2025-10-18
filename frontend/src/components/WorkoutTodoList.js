import React, { useState, useEffect } from 'react';
import { IoTimeOutline, IoStatsChartOutline } from 'react-icons/io5';
import ExerciseItem from './ExerciseItem';
import { calculateExpGain } from '../utils/progressSystem';

const WorkoutTodoList = ({ workout, onExpGain, userProgress, currentWeek }) => {
  const [completedExercises, setCompletedExercises] = useState(() => {
    // Load permanently completed exercises from userProgress for current week only
    if (userProgress && userProgress.completedExercises) {
      return new Set(Object.keys(userProgress.completedExercises).filter(
        key => key.startsWith(`week${currentWeek}-`) && userProgress.completedExercises[key] === true
      ));
    }
    return new Set();
  });

  if (!workout) return <div>Select a day to view workout</div>;

  const completeExercise = (exerciseIndex) => {
    const uniqueKey = `week${currentWeek}-day${workout.day}-exercise${exerciseIndex}`;

    // Only allow completion if not already completed
    if (!completedExercises.has(uniqueKey)) {
      const exercise = workout.exercises[exerciseIndex];
      const newCompleted = new Set(completedExercises);
      newCompleted.add(uniqueKey);
      setCompletedExercises(newCompleted);

      // Gain EXP only once
      if (onExpGain) {
        const expGained = calculateExpGain(exercise);
        onExpGain(expGained, uniqueKey);
      }
    }
  };

  const getCompletedCount = () => {
    return workout.exercises.filter((_, index) =>
      completedExercises.has(`week${currentWeek}-day${workout.day}-exercise${index}`)
    ).length;
  };

  const completedCount = getCompletedCount();
  const completionPercentage = Math.round((completedCount / workout.exercises.length) * 100);

  return (
    <div className="workout-todo-container">
      <div className="workout-header">
        <h2>Day {workout.day}: {workout.focus}</h2>
        <div className="workout-stats">
          <span className="duration">
            <IoTimeOutline className="stat-icon" />
            {workout.total_duration} min
          </span>
          <span className="progress">
            <IoStatsChartOutline className="stat-icon" />
            {completedCount}/{workout.exercises.length} completed ({completionPercentage}%)
          </span>
        </div>
        <div className="progress-bar">
          <div
            className="progress-fill"
            style={{ width: `${completionPercentage}%` }}
          ></div>
        </div>
      </div>

      <div className="exercise-list">
        {workout.exercises.map((exercise, index) => (
          <ExerciseItem
            key={index}
            exercise={exercise}
            isCompleted={completedExercises.has(`week${currentWeek}-day${workout.day}-exercise${index}`)}
            onComplete={() => completeExercise(index)}
          />
        ))}
      </div>

      {completedCount === workout.exercises.length && (
        <div className="completion-message">
          Great job! You've completed today's workout!
        </div>
      )}
    </div>
  );
};

export default WorkoutTodoList;
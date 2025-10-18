import React from 'react';
import { calculateExpGain } from '../utils/progressSystem';

const ExerciseItem = ({ exercise, isCompleted, onComplete }) => {
  const getExerciseIcon = (type) => {
    const icons = {
      strength: '•',
      cardio: '•',
      core: '•',
      flexibility: '•',
      warmup: '•',
      cooldown: '•'
    };
    return icons[type] || '•';
  };

  const formatReps = (exercise) => {
    if (exercise.reps && exercise.sets) {
      return `${exercise.sets} sets × ${exercise.reps} reps`;
    }
    if (exercise.duration && exercise.sets) {
      return `${exercise.sets} sets × ${exercise.reps || exercise.duration}${typeof exercise.reps === 'number' ? ' sec' : ''}`;
    }
    return `${exercise.sets || 1} sets`;
  };

  return (
    <div className={`exercise-item ${isCompleted ? 'completed' : ''}`}>
      <div className="exercise-content">
        <div className="exercise-header">
          <span className="exercise-icon">{getExerciseIcon(exercise.type)}</span>
          <h3 className="exercise-name">{exercise.name}</h3>
          <span className={`exercise-type ${exercise.type}`}>{exercise.type}</span>
        </div>

        <div className="exercise-details">
          <span className="exercise-reps">{formatReps(exercise)}</span>
          {exercise.rest > 0 && (
            <span className="exercise-rest">Rest: {exercise.rest}s</span>
          )}
          <span className="exercise-exp">+{calculateExpGain(exercise)} XP</span>
        </div>
      </div>

      <button
        className="complete-btn"
        onClick={onComplete}
        disabled={isCompleted}
      >
        {isCompleted ? 'Completed' : 'Mark as Complete'}
      </button>
    </div>
  );
};

export default ExerciseItem;
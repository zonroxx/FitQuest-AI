import React, { useEffect, useState } from 'react';
import { IoTrophyOutline, IoFlashOutline } from 'react-icons/io5';

const UserProgress = ({ level, currentExp, expToNextLevel, onLevelUp }) => {
  const [showLevelUp, setShowLevelUp] = useState(false);
  const expPercentage = Math.round((currentExp / expToNextLevel) * 100);

  useEffect(() => {
    if (currentExp >= expToNextLevel && onLevelUp) {
      setShowLevelUp(true);
      onLevelUp();

      // Hide the level-up message after 3 seconds
      setTimeout(() => {
        setShowLevelUp(false);
      }, 3000);
    }
  }, [currentExp, expToNextLevel, onLevelUp]);

  return (
    <>
      <div className="user-progress-container">
        <div className="user-stats">
          <div className="user-level">
            <IoTrophyOutline className="level-icon" />
            <div className="level-info">
              <span className="level-label">Level</span>
              <span className="level-number">{level}</span>
            </div>
          </div>

          <div className="exp-container">
            <div className="exp-info">
              <div className="exp-label">
                <IoFlashOutline className="exp-icon" />
                <span>Experience</span>
              </div>
              <span className="exp-numbers">
                {currentExp} / {expToNextLevel} XP
              </span>
            </div>
            <div className="exp-bar">
              <div
                className="exp-fill"
                style={{ width: `${expPercentage}%` }}
              ></div>
            </div>
          </div>
        </div>
      </div>

      {showLevelUp && (
        <div className="level-up-notification">
          <div className="level-up-content">
            <IoTrophyOutline className="level-up-icon" />
            <h3>Level Up!</h3>
            <p>You reached level {level}!</p>
          </div>
        </div>
      )}
    </>
  );
};

export default UserProgress;

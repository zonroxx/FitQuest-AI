import React, { useState, useEffect } from 'react';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const Leaderboard = ({ token, onClose }) => {
  const [leaderboardData, setLeaderboardData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchLeaderboard();
  }, []);

  const fetchLeaderboard = async () => {
    try {
      setIsLoading(true);
      const response = await fetch(`${API_URL}/leaderboard/`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setLeaderboardData(data);
      } else {
        setError('Failed to load leaderboard');
      }
    } catch (err) {
      setError('Error fetching leaderboard');
      console.error('Error fetching leaderboard:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="leaderboard-overlay" onClick={onClose}>
      <div className="leaderboard-container" onClick={(e) => e.stopPropagation()}>
        <div className="leaderboard-header">
          <h2>Leaderboard</h2>
          <button className="close-leaderboard-btn" onClick={onClose}>×</button>
        </div>

        <div className="leaderboard-content">
          {isLoading ? (
            <div className="leaderboard-loading">Loading leaderboard...</div>
          ) : error ? (
            <div className="leaderboard-error">{error}</div>
          ) : leaderboardData ? (
            <>
              <div className="leaderboard-section">
                <h3>Top 10 Players</h3>
                <div className="leaderboard-list">
                  {leaderboardData.top_users.map((user) => (
                    <div key={user.rank} className="leaderboard-entry">
                      <div className="leaderboard-rank-circle">
                        {user.rank}
                      </div>
                      <div className="leaderboard-info">
                        <div className="leaderboard-username">{user.username}</div>
                        <div className="leaderboard-stats">
                          Level {user.level} • {user.current_exp} XP • {user.total_exercises_completed} exercises
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {leaderboardData.current_user_rank && leaderboardData.current_user_rank.rank > 10 && (
                <div className="leaderboard-section your-rank-section">
                  <h3>Your Rank</h3>
                  <div className="leaderboard-list">
                    <div className="leaderboard-entry your-rank">
                      <div className="leaderboard-rank-circle">
                        {leaderboardData.current_user_rank.rank}
                      </div>
                      <div className="leaderboard-info">
                        <div className="leaderboard-username">
                          {leaderboardData.current_user_rank.username} (You)
                        </div>
                        <div className="leaderboard-stats">
                          Level {leaderboardData.current_user_rank.level} • {leaderboardData.current_user_rank.current_exp} XP • {leaderboardData.current_user_rank.total_exercises_completed} exercises
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </>
          ) : null}
        </div>
      </div>
    </div>
  );
};

export default Leaderboard;

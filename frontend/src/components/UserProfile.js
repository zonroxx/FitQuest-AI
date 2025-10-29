import React, { useState } from 'react';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const UserProfile = ({ userProfile, token, onProfileUpdate, onClose }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editedProfile, setEditedProfile] = useState({
    age: userProfile?.age || 25,
    weight: userProfile?.weight || 70,
    height: userProfile?.height || 170,
    fitness_level: userProfile?.fitness_level || 'beginner'
  });
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    const { name, value, type } = e.target;
    setEditedProfile(prev => ({
      ...prev,
      [name]: type === 'number' ? parseFloat(value) || 0 : value
    }));
  };

  const handleSave = async () => {
    try {
      setIsSaving(true);
      setError('');

      const response = await fetch(`${API_URL}/auth/me`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(editedProfile)
      });

      if (!response.ok) {
        throw new Error('Failed to update profile');
      }

      const updatedProfile = await response.json();
      onProfileUpdate(updatedProfile);
      setIsEditing(false);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsSaving(false);
    }
  };

  const handleCancel = () => {
    setEditedProfile({
      age: userProfile?.age || 25,
      weight: userProfile?.weight || 70,
      height: userProfile?.height || 170,
      fitness_level: userProfile?.fitness_level || 'beginner'
    });
    setIsEditing(false);
    setError('');
  };

  if (!userProfile) {
    return (
      <div className="profile-overlay" onClick={onClose}>
        <div className="profile-container" onClick={(e) => e.stopPropagation()}>
          <div className="profile-header">
            <h2>User Profile</h2>
            <button className="close-profile-btn" onClick={onClose}>×</button>
          </div>
          <p>Loading profile...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="profile-overlay" onClick={onClose}>
      <div className="profile-container" onClick={(e) => e.stopPropagation()}>
        <div className="profile-header">
          <h2>User Profile</h2>
          <button className="close-profile-btn" onClick={onClose}>×</button>
        </div>

        <div className="profile-content">
          <div className="profile-section">
            <h3>Account Information</h3>
            <div className="profile-field">
              <label>Email</label>
              <span>{userProfile.email}</span>
            </div>
            <div className="profile-field">
              <label>Username</label>
              <span>{userProfile.username}</span>
            </div>
          </div>

          <div className="profile-section">
            <div className="section-header">
              <h3>Fitness Details</h3>
              {!isEditing && (
                <button className="edit-btn" onClick={() => setIsEditing(true)}>
                  Edit
                </button>
              )}
            </div>

            {isEditing ? (
              <div className="edit-form">
                <div className="profile-field">
                  <label htmlFor="age">Age</label>
                  <input
                    type="number"
                    id="age"
                    name="age"
                    value={editedProfile.age}
                    onChange={handleInputChange}
                    min="13"
                    max="100"
                    required
                  />
                </div>

                <div className="profile-field">
                  <label htmlFor="weight">Weight (kg)</label>
                  <input
                    type="number"
                    id="weight"
                    name="weight"
                    value={editedProfile.weight}
                    onChange={handleInputChange}
                    min="30"
                    max="300"
                    step="0.1"
                    required
                  />
                </div>

                <div className="profile-field">
                  <label htmlFor="height">Height (cm)</label>
                  <input
                    type="number"
                    id="height"
                    name="height"
                    value={editedProfile.height}
                    onChange={handleInputChange}
                    min="100"
                    max="250"
                    step="0.1"
                    required
                  />
                </div>

                <div className="profile-field">
                  <label htmlFor="fitness_level">Fitness Level</label>
                  <select
                    id="fitness_level"
                    name="fitness_level"
                    value={editedProfile.fitness_level}
                    onChange={handleInputChange}
                    required
                  >
                    <option value="beginner">Beginner</option>
                    <option value="intermediate">Intermediate</option>
                    <option value="advanced">Advanced</option>
                  </select>
                </div>

                {error && <div className="error">{error}</div>}

                <div className="profile-actions">
                  <button
                    className="save-btn"
                    onClick={handleSave}
                    disabled={isSaving}
                  >
                    {isSaving ? 'Saving...' : 'Save Changes'}
                  </button>
                  <button
                    className="cancel-btn"
                    onClick={handleCancel}
                    disabled={isSaving}
                  >
                    Cancel
                  </button>
                </div>
              </div>
            ) : (
              <>
                <div className="profile-field">
                  <label>Age</label>
                  <span>{userProfile.age || 'Not set'}</span>
                </div>
                <div className="profile-field">
                  <label>Weight</label>
                  <span>{userProfile.weight ? `${userProfile.weight} kg` : 'Not set'}</span>
                </div>
                <div className="profile-field">
                  <label>Height</label>
                  <span>{userProfile.height ? `${userProfile.height} cm` : 'Not set'}</span>
                </div>
                <div className="profile-field">
                  <label>Fitness Level</label>
                  <span>
                    {userProfile.fitness_level
                      ? userProfile.fitness_level.charAt(0).toUpperCase() + userProfile.fitness_level.slice(1)
                      : 'Not set'}
                  </span>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserProfile;

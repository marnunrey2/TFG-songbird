import React, { useState } from 'react';
import UsersTemplate from '../../components/UsersTemplate';
import '../../styles/Colors.css';
import '../../styles/UserStyles.css';
import { useFetchAdminDashboard } from '../../components/useFetchData';
import { Button } from 'react-bootstrap';

function Dashboard() {
  const AdminDashboard = useFetchAdminDashboard();
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const populateDatabase = async () => {
    setLoading(true);
    setMessage('The database is being populated... This may take a few minutes.');

    const response = await fetch('http://localhost:8000/api/admin/populate/', { method: 'POST' });
    const data = await response.json();

    setLoading(false);
    setMessage(data.message);
  };

  return (
    <UsersTemplate>
      <h1>Welcome to your Dashboard</h1>
      <div className="statistics" >
        <div className="statistic-card statistic-card-small">
          <h2>Number of Users:</h2>
          <h3>{AdminDashboard.num_users}</h3>
        </div>
      </div>
      <div className="statistics" >
        <div className="statistic-card-4 statistic-card-small">
          <h2>Number of Songs:</h2>
          <h3>{AdminDashboard.num_songs}</h3>
        </div>
        <div className="statistic-card-4 statistic-card-small">
          <h2>Number of Artists:</h2>
          <h3>{AdminDashboard.num_artists}</h3>
        </div>
        <div className="statistic-card-4 statistic-card-small">
          <h2>Number of Albums:</h2>
          <h3>{AdminDashboard.num_artists}</h3>
        </div>
        <div className="statistic-card-4 statistic-card-small">
          <h2>Number of Playlists:</h2>
          <h3>{AdminDashboard.num_artists}</h3>
        </div>
      </div>
      
      <Button onClick={populateDatabase} disabled={loading} className='populate-button'>
          Populate database
      </Button>
      {message && <p className='populate-message'>{message}</p>}
    </UsersTemplate>
  );
}

export default Dashboard;

import React from 'react';
import UsersTemplate from '../../components/UsersTemplate';
import '../../styles/Colors.css';
import '../../styles/UserStyles.css';

function Dashboard() {
  const user = JSON.parse(localStorage.getItem('user'));
  console.log(user);

  return (
    <UsersTemplate background={true}>
      <h1>Welcome to your Dashboard</h1>
      <div className="statistics">
        <div className="statistic-card">
          <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" class="bi bi-music-note-beamed" viewBox="0 0 16 16">
            <path d="M6 13c0 1.105-1.12 2-2.5 2S1 14.105 1 13s1.12-2 2.5-2 2.5.896 2.5 2m9-2c0 1.105-1.12 2-2.5 2s-2.5-.895-2.5-2 1.12-2 2.5-2 2.5.895 2.5 2"/>
            <path fillRule="evenodd" d="M14 11V2h1v9zM6 3v10H5V3z"/>
            <path d="M5 2.905a1 1 0 0 1 .9-.995l8-.8a1 1 0 0 1 1.1.995V3L5 4z"/>
          </svg>
          <h2>{user.liked_songs.length} Liked Songs</h2>
        </div>
        <div className="statistic-card">
          <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" class="bi bi-vinyl-fill" viewBox="0 0 16 16">
            <path d="M8 6a2 2 0 1 0 0 4 2 2 0 0 0 0-4m0 3a1 1 0 1 1 0-2 1 1 0 0 1 0 2"/>
            <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M4 8a4 4 0 1 0 8 0 4 4 0 0 0-8 0"/>
          </svg>
          <h2>{user.liked_albums.length} Liked Albums</h2>
        </div>
        <div className="statistic-card">
          <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" class="bi bi-person-heart" viewBox="0 0 16 16">
            <path d="M9 5a3 3 0 1 1-6 0 3 3 0 0 1 6 0m-9 8c0 1 1 1 1 1h10s1 0 1-1-1-4-6-4-6 3-6 4m13.5-8.09c1.387-1.425 4.855 1.07 0 4.277-4.854-3.207-1.387-5.702 0-4.276Z"/>
          </svg>
          <h2>{user.liked_artists.length} Liked Artists</h2>
        </div>
      </div>
      <div className="statistics" style={{marginTop: '70px'}}>
        <div className="statistic-card-4">
          <h2>Favourite Song:</h2>
          {user.liked_songs.length > 0 ? <h3>{user.liked_songs[0].name}</h3> : <h3>No favourite song yet</h3>}
        </div>
        <div className="statistic-card-4">
          <h2>Favourite Album:</h2>
          {user.liked_albums.length > 0 ? <h3>{user.liked_albums[0].name}</h3> : <h3>No favourite album yet</h3>}
        </div>
        <div className="statistic-card-4">
          <h2>Favourite Artist:</h2>
          {user.liked_artists.length > 0 ? <h3>{user.liked_artists[0].name}</h3> : <h3>No favourite artist yet</h3>}
        </div>
        <div className="statistic-card-4">
          <h2>Favourite Genre:</h2>
          {user.liked_artists.length > 0 ? <h3>{user.liked_artists[0].name}</h3> : <h3>No favourite genre yet</h3>}
        </div>
      </div>
    </UsersTemplate>
  );
}

export default Dashboard;

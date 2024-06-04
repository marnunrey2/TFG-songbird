import React from 'react';
import UsersTemplate from '../../components/UsersTemplate';
import '../../styles/Colors.css';
import '../../styles/UserStyles.css';
import { MusicNoteBeamed, VinylFill, PersonHeart } from 'react-bootstrap-icons';

function Dashboard() {
  const user = JSON.parse(localStorage.getItem('user'));
  console.log(user);

  return (
    <UsersTemplate background={true}>
      <h1>Welcome to your Dashboard</h1>
      <div className="statistics">
        <div className="statistic-card">
          <MusicNoteBeamed color="black" size={50} />
          <h2>{user.liked_songs.length} Liked Songs</h2>
        </div>
        {/* <div className="statistic-card">
          <VinylFill color="black" size={50} />
          <h2>{user.liked_albums.length} Liked Albums</h2>
        </div>
        <div className="statistic-card">
          <PersonHeart color="black" size={50} />
          <h2>{user.liked_artists.length} Liked Artists</h2>
        </div> */}
        <div className="statistic-card">
          <VinylFill color="black" size={50} />
          <h2>0 Liked Albums</h2>
        </div>
        <div className="statistic-card">
          <PersonHeart color="black" size={50} />
          <h2>0 Liked Artists</h2>
        </div>
      </div>
      <div className="statistics" style={{marginTop: '70px'}}>
        <div className="statistic-card-4">
          <h2>Favourite Song:</h2>
          {user.liked_songs.length > 0 ? <h3>{user.liked_songs[0].name}</h3> : <h3>No favourite song yet</h3>}
        </div>
        {/* <div className="statistic-card-4">
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
        </div> */}
        <div className="statistic-card-4">
          <h2>Favourite Album:</h2>
          <h3>No favourite album yet</h3>
        </div>
        <div className="statistic-card-4">
          <h2>Favourite Artist:</h2>
          <h3>No favourite artist yet</h3>
        </div>
        <div className="statistic-card-4">
          <h2>Favourite Genre:</h2>
          <h3>No favourite genre yet</h3>
        </div>
      </div>
    </UsersTemplate>
  );
}

export default Dashboard;

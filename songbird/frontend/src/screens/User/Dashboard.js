import React from 'react';
import UsersTemplate from '../../components/UsersTemplate';
import '../../styles/Colors.css';
import '../../styles/UserStyles.css';
import { MusicNoteBeamed, VinylFill, PersonHeart } from 'react-bootstrap-icons';

function Dashboard() {
  const user = JSON.parse(localStorage.getItem('user'));
  console.log(user.liked_songs);

  // Liked albums
  const albumIds = user.liked_songs.map(song => song.album.id);
  const uniqueAlbumIds = [...new Set(albumIds)];

  // Liked artists
  const artistIds = user.liked_songs.flatMap(song => [song.main_artist.name, ...song.collaborators.map(artist => artist.name)]);
  const uniqueArtistIds = [...new Set(artistIds)];

  // Favourite album
  const albumCounts = albumIds.reduce((counts, id) => {
    counts[id] = (counts[id] || 0) + 1;
    return counts;
  }, {});
  const favouriteAlbumId = Object.keys(albumCounts).reduce((a, b) => albumCounts[a] > albumCounts[b] ? a : b);
  const favouriteAlbum = user.liked_songs.find(song => song.album.id === Number(favouriteAlbumId)).album;

  // Favourite artist
  const artistCounts = artistIds.reduce((counts, id) => {
    counts[id] = (counts[id] || 0) + 1;
    return counts;
  }, {});
  const favouriteArtistId = Object.keys(artistCounts).reduce((a, b) => artistCounts[a] > artistCounts[b] ? a : b);
  const favouriteArtist = user.liked_songs.find(song => song.main_artist.name === favouriteArtistId).main_artist;
  if (!favouriteArtist) {
    for (let song of user.liked_songs) {
      const favouriteArtist = song.collaborators.find(artist => artist.id === Number(favouriteArtistId));
      if (favouriteArtist) break;
    }
  }

  // Favourite genre
  let genreNames = user.liked_songs.flatMap(song => song.album.genres.map(genre => genre.name));
  if (genreNames.length === 0){
    genreNames = user.liked_songs.flatMap(song => [song.main_artist.genres.map(genre => genre.name), ...song.collaborators.flatMap(artist => artist.genres.map(genre => genre.name))]).flat();
  }
  const genreCounts = genreNames.reduce((counts, name) => {
    counts[name] = (counts[name] || 0) + 1;
    return counts;
  }, {});
  const favouriteGenreName = Object.keys(genreCounts).reduce((a, b) => genreCounts[a] > genreCounts[b] ? a : b);

  console.log(genreNames);
  console.log(genreCounts);
  console.log(favouriteGenreName);

  return (
    <UsersTemplate>
      <h1>Welcome to your Dashboard</h1>
      <div className="statistics">
        <div className="statistic-card">
          <MusicNoteBeamed color="black" size={50} />
          <h2>{user.liked_songs.length} Liked Songs</h2>
        </div>
        <div className="statistic-card">
          <VinylFill color="black" size={50} />
          <h2>{uniqueAlbumIds.length} Liked Albums</h2>
        </div>
        <div className="statistic-card">
          <PersonHeart color="black" size={50} />
          <h2>{uniqueArtistIds.length} Liked Artists</h2>
        </div>
      </div>
      <div className="statistics" style={{marginTop: '70px'}}>
        <div className="statistic-card-4">
          <h2>Current favourite Song:</h2>
          {user.liked_songs.length > 0 ? <h3>{user.liked_songs[user.liked_songs.length - 1].name}</h3> : <h3>No favourite song yet</h3>}
        </div>
        <div className="statistic-card-4">
          <h2>Favourite Album:</h2>
          {favouriteAlbum ? <h3>{favouriteAlbum.name}</h3> : <h3>No favourite album yet</h3>}
        </div>
        <div className="statistic-card-4">
          <h2>Favourite Artist:</h2>
          {favouriteArtist ? <h3>{favouriteArtist.name}</h3> : <h3>No favourite artist yet</h3>}
        </div>
        <div className="statistic-card-4">
          <h2>Favourite Genre:</h2>
          {favouriteGenreName ? <h3>{favouriteGenreName}</h3> : <h3>No favourite genre yet</h3>}
        </div>
      </div>
    </UsersTemplate>
  );
}

export default Dashboard;

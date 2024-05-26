import React, { useEffect, useState } from 'react';
import axios from 'axios';
import CustomNavbar from './Navbar';
import '../styles/App.css';

function Albums() {
  const [albums, setAlbums] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/api/albums/?limit=30')
      .then(response => {
        setAlbums(response.data['results']);
        console.log(response.data['results']);
        console.log(response);
      })
      .catch(error => {
        console.error('There was an error fetching the albums!', error);
      });
  }, []);

  return (
    <div className='App'>
      <CustomNavbar />
      <h1>Albums</h1>
      <ul>
        {albums.map(album => (
          <li key={album.id}>{album.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default Albums;

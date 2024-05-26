import React, { useEffect, useState } from 'react';
import axios from 'axios';
import CustomNavbar from './Navbar';

function Artists() {
  const [artists, setArtists] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/api/artists/?limit=10')
      .then(response => {
        setArtists(response.data['results']);
        console.log(response.data['results']);
      })
      .catch(error => {
        console.error('There was an error fetching the artists!', error);
      });
  }, []);

  return (
    <div className='App'>
      <CustomNavbar />
      <h1>Artists</h1>
      <ul>
        {artists.map(artist => (
          <li key={artist.id}>{artist.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default Artists;

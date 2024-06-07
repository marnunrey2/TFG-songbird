import React from 'react';
import CustomNavbar from '../../components/Navbar';
import '../../styles/App.css';

function Homepage() {
  return (
    <div className='App bg-homepage'>
      <CustomNavbar />
      
      <div className="card">
        <div className="card-body">
          <h1 className="card-title card-title-large">♩♪♫ Welcome to Songbird ♫♪♩</h1>
          <h1 className="card-title card-title-small">Welcome to Songbird</h1>
          <h1 className="card-title card-title-small">♫♪♩</h1>
          <p className="card-text">Find your favourite songs, artist and albums here!</p>
          <p className="card-text">
            Sign up and have unlimited access to the latest tracks from all around 
            the globe. Give likes to songs and get recommendations. You can access 
            song lyrics, artist information, have a wrapped-up list of your favourite 
            songs, and so much more!
          </p>
          <a href='/signup' className="btn btn-primary btn-lg">Sign Up Now</a>
        </div>
      </div>
    </div>
  );
}

export default Homepage;

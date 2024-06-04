import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';

import ProtectedRoute from '../components/ProtectedRoute';

// HOMEPAGE
import Homepage from './Homepage/Homepage';
import SignUp from './Homepage/SignUp';
import Login from './Homepage/Login';

// USER SCREENS
import Dashboard from './User/Dashboard';
import UserSongs from './User/UserSongs';
import UserArtists from './User/UserArtists';
import UserAlbums from './User/UserAlbums';
import SongDetails from './User/SongDetails';
import ArtistDetails from './User/ArtistDetails';

function App() {
  return (
    <Router>
      <Routes>
        {/* HOMEPAGE */}
        <Route path="/" element={<Homepage />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/login" element={<Login />} />

        {/* USER ROUTES */}
        <Route path="/dashboard" element={<ProtectedRoute component={Dashboard} />} />
        <Route path="/user/songs" element={<ProtectedRoute component={UserSongs} />} />
        <Route path="/user/artists" element={<ProtectedRoute component={UserArtists} />} />
        <Route path="/user/albums" element={<ProtectedRoute component={UserAlbums} />} />
        <Route path="/song/:id" element={<SongDetails />} />
        <Route path='/artist/:name' element={<ArtistDetails />} />

      </Routes>
    </Router>
  );
}

export default App;
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';

import ProtectedRoute from '../components/ProtectedRoute';

// HOMEPAGE
import Homepage from './Homepage/Homepage';
import Songs from '../components/Songs';
import Artists from '../components/Artists';
import Albums from '../components/Albums';
import Recommendations from '../components/Recommendations';
import SignUp from './Homepage/SignUp';
import Login from './Homepage/Login';

// USER SCREENS
import Dashboard from './User/Dashboard';
import UserSongs from './User/UserSongs';
import UserArtists from './User/UserArtists';
import UserAlbums from './User/UserAlbums';

function App() {
  return (
    <Router>
      <Routes>
        {/* HOMEPAGE */}
        <Route path="/" element={<Homepage />} />
        <Route path="/songs" element={<Songs />} />
        <Route path="/artists" element={<Artists />} />
        <Route path="/albums" element={<Albums />} />
        <Route path="/recommendations" element={<Recommendations />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/login" element={<Login />} />

        {/* USER ROUTES */}
        <Route path="/dashboard" element={<ProtectedRoute component={Dashboard} />} />
        <Route path="/user/songs" element={<ProtectedRoute component={UserSongs} />} />
        <Route path="/user/artists" element={<ProtectedRoute component={UserArtists} />} />
        <Route path="/user/albums" element={<ProtectedRoute component={UserAlbums} />} />
      </Routes>
    </Router>
  );
}

export default App;
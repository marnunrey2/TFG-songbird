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

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="/songs" element={<Songs />} />
        <Route path="/artists" element={<Artists />} />
        <Route path="/albums" element={<Albums />} />
        <Route path="/recommendations" element={<Recommendations />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/login" element={<Login />} />

        
        <Route path="/dashboard" element={<ProtectedRoute component={Dashboard} />} />
      </Routes>
    </Router>
  );
}

export default App;
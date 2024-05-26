import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import Songs from '../components/Songs';
import Artists from '../components/Artists';
import Albums from '../components/Albums';
import Recommendations from '../components/Recommendations';
import Homepage from './Homepage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="/songs" element={<Songs />} />
        <Route path="/artists" element={<Artists />} />
        <Route path="/albums" element={<Albums />} />
        <Route path="/recommendations" element={<Recommendations />} />
      </Routes>
    </Router>
  );
}

export default App;
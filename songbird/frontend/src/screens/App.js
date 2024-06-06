import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';

import ProtectedRoute from '../components/ProtectedRoute';

// HOMEPAGE
import Homepage from './Homepage/Homepage';
import SignUp from './Homepage/SignUp';
import Login from './Homepage/Login';

// USER SCREENS
import Profile from './User/Profile';
import Dashboard from './User/Dashboard';
import UserSongs from './User/UserSongs';
import UserArtists from './User/UserArtists';
import UserAlbums from './User/UserAlbums';
import SongDetails from './User/SongDetails';
import ArtistDetails from './User/ArtistDetails';
import AlbumDetails from './User/AlbumDetails';

// TOPS
import AllTimeTop from './User/tops/AllTimeTop';
import TopGlobal from './User/tops/TopGlobal';
import TopUSA from './User/tops/TopUSA';
import TopUK from './User/tops/TopUK';
import TopSpain from './User/tops/TopSpain';
import TopArgentina from './User/tops/TopArgentina';
import TopAustralia from './User/tops/TopAustralia';
import TopCanada from './User/tops/TopCanada';
import TopColombia from './User/tops/TopColombia';
import TopFrance from './User/tops/TopFrance';
import TopGermany from './User/tops/TopGermany';
import TopItaly from './User/tops/TopItaly';
import TopJapan from './User/tops/TopJapan';
import TopSouthKorea from './User/tops/TopSouthKorea';


function App() {
  return (
    <Router>
      <Routes>
        {/* HOMEPAGE */}
        <Route path="/" element={<Homepage />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/login" element={<Login />} />

        {/* USER ROUTES */}
        <Route path='/profile' element={<ProtectedRoute component={Profile} />} />
        <Route path="/dashboard" element={<ProtectedRoute component={Dashboard} />} />
        <Route path="/user/songs" element={<ProtectedRoute component={UserSongs} />} />
        <Route path="/user/artists" element={<ProtectedRoute component={UserArtists} />} />
        <Route path="/user/albums" element={<ProtectedRoute component={UserAlbums} />} />
        <Route path="/song/:id" element={<SongDetails />} />
        <Route path='/artist/:name' element={<ArtistDetails />} />
        <Route path='/album/:id' element={<AlbumDetails />} />

        {/* TOPS */}
        <Route path="/all-time-top" element={<ProtectedRoute component={AllTimeTop} />} />
        <Route path='/top-global' element={<TopGlobal />} />
        <Route path="/top-usa" element={<ProtectedRoute component={TopUSA} />} />
        <Route path="/top-uk" element={<ProtectedRoute component={TopUK} />} />
        <Route path="/top-spain" element={<ProtectedRoute component={TopSpain} />} />
        <Route path="/top-argentina" element={<ProtectedRoute component={TopArgentina} />} />
        <Route path="/top-australia" element={<ProtectedRoute component={TopAustralia} />} />
        <Route path="/top-canada" element={<ProtectedRoute component={TopCanada} />} />
        <Route path="/top-colombia" element={<ProtectedRoute component={TopColombia} />} />
        <Route path="/top-france" element={<ProtectedRoute component={TopFrance} />} />
        <Route path="/top-germany" element={<ProtectedRoute component={TopGermany} />} />
        <Route path="/top-italy" element={<ProtectedRoute component={TopItaly} />} />
        <Route path="/top-japan" element={<ProtectedRoute component={TopJapan} />} />
        <Route path="/top-south-korea" element={<ProtectedRoute component={TopSouthKorea} />} />


      </Routes>
    </Router>
  );
}

export default App;
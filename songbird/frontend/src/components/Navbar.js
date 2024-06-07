import React from 'react';
import { Navbar, Nav, Button } from 'react-bootstrap';
import { Link, useLocation } from 'react-router-dom';
import '../styles/Navbar.css';
import 'bootstrap/dist/css/bootstrap.min.css';

const CustomNavbar = () => {
    const location = useLocation();

  return (
    <Navbar expand="lg" className="custom-navbar" fixed="top">
        <Navbar.Brand
            as={Link}
            to="/"
            className="text-white navbar-brand"
        >
          <img src={`${process.env.PUBLIC_URL}/logo-bg.png`} height={40} alt="Songbird" />
        </Navbar.Brand>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav" className="justify-content-center">
        <Nav className="ml-auto" style={{paddingTop: '20px'}}>
          <Nav.Link
            as={Link}
            to="/top-spotify"
            className={`nav-link text-white ${location.pathname === '/top-spotify' ? 'active-link' : ''}`}
          >
            Top Spotify
          </Nav.Link>
          <Nav.Link
            as={Link}
            to="/top-apple-music"
            className={`nav-link text-white ${location.pathname === '/top-apple-music' ? 'active-link' : ''}`}
          >
            Top Apple Music
          </Nav.Link>
          <Nav.Link
            as={Link}
            to="/top-shazam"
            className={`nav-link text-white ${location.pathname === '/top-shazam' ? 'active-link' : ''}`}
          >
            Top Shazam
          </Nav.Link>
          <Nav.Link
            as={Link}
            to="/top-deezer"
            className={`nav-link text-white ${location.pathname === '/top-deezer' ? 'active-link' : ''}`}
          >
            Top Deezer
          </Nav.Link>
          <Nav.Link
            as={Link}
            to="/top-youtube"
            className={`nav-link text-white ${location.pathname === '/top-youtube' ? 'active-link' : ''}`}
          >
            Top YouTube
          </Nav.Link>
          <Button as={Link} to="/signup" variant="outline-light" className="mr-2 d-lg-none">Sign up</Button>
          <Nav.Link
            href="/login"
            className="text-white d-lg-none login-link"
          >
            Log in
          </Nav.Link>
        </Nav>
    </Navbar.Collapse>
      <Nav className="ml-auto d-none d-lg-flex" style={{marginRight: '30px'}}>
        <Button as={Link} to="/signup" variant="outline-light" className="mr-2">Sign up</Button>
        <Nav.Link
          href="/login"
          className="text-white"
        >
          Log in
        </Nav.Link>
      </Nav>
    </Navbar>
  );
};

export default CustomNavbar;

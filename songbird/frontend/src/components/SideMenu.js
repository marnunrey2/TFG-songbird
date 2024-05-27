import React from 'react';
import { Navbar, Nav } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import '../styles/SideMenu.css';

const SideMenu = () => {

    return (
        <Navbar expand="lg" className="custom-menu" >
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="side-navbar-nav" className="justify-content-start">
                <Nav className="flex-column custom-menu-nav" >
                    <Nav.Link as={Link} to="/dashboard">Dashboard</Nav.Link>
                    <Nav.Link as={Link} to="/songs">Songs</Nav.Link>
                    <Nav.Link as={Link} to="/artists">Artists</Nav.Link>
                </Nav>
            </Navbar.Collapse>
        </Navbar>
    );
};

export default SideMenu;
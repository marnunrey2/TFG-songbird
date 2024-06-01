import React from 'react';
import { Navbar, Nav, NavDropdown } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import '../styles/SideMenu.css';

const SideMenu = () => {
    return (
        <Navbar expand="lg" className="custom-menu">
            <Navbar.Toggle aria-controls="basic-navbar-nav"/>
            <Navbar.Collapse id="side-navbar-nav" className="justify-content-start">
                <Nav className="flex-column custom-menu-nav">
                    <Nav.Link as={Link} to="/dashboard">Dashboard</Nav.Link>
                    <Nav.Link as={Link} to="/user/songs">Songs</Nav.Link>
                    <Nav.Link as={Link} to="/user/artists">Artists</Nav.Link>
                    <Nav.Link as={Link} to="/user/albums">Albums</Nav.Link>
                    <NavDropdown title={<span className="menu-dropdown-title">Top</span>} id="basic-nav-dropdown" className="menu-dropdown">
                        <NavDropdown.Item as={Link} to="/all-time-top">All time top</NavDropdown.Item>
                        <NavDropdown.Item as={Link} to="/top-global">Top Global</NavDropdown.Item>
                        <NavDropdown.Item as={Link} to="/top-usa">Top USA</NavDropdown.Item>
                        <NavDropdown.Item as={Link} to="/top-spain">Top Spain</NavDropdown.Item>
                        <NavDropdown.Item as={Link} to="/top-uk">Top UK</NavDropdown.Item>
                        <NavDropdown.Item as={Link} to="/top-canada">Top Canada</NavDropdown.Item>
                        <NavDropdown.Item as={Link} to="/top-south-korea">Top South Korea</NavDropdown.Item>
                        <NavDropdown.Item as={Link} to="/top-france">Top France</NavDropdown.Item>
                        <NavDropdown.Item as={Link} to="/top-germany">Top Germany</NavDropdown.Item>
                        <NavDropdown.Item as={Link} to="/top-australia">Top Australia</NavDropdown.Item>
                        <NavDropdown.Item as={Link} to="/top-colombia">Top Colombia</NavDropdown.Item>
                        <NavDropdown.Item as={Link} to="/top-argentina">Top Argentina</NavDropdown.Item>
                        <NavDropdown.Item as={Link} to="/top-italy">Top Italy</NavDropdown.Item>
                        <NavDropdown.Item as={Link} to="/top-japan">Top Japan</NavDropdown.Item>
                    </NavDropdown>
                </Nav>
            </Navbar.Collapse>
        </Navbar>
    );
};

export default SideMenu;

import React from 'react';
import { Navbar, Nav, NavDropdown } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import '../styles/SideMenu.css';

const SideMenu = () => {
    const handleClick = () => {
        window.scrollTo(0, 0);
    };

    return (
        <Navbar expand="lg" className="custom-menu">
            <Navbar.Toggle aria-controls="basic-navbar-nav"/>
            <Navbar.Collapse id="side-navbar-nav" className="justify-content-start">
                <Nav className="flex-column custom-menu-nav">
                    <Nav.Link as={Link} to="/dashboard" onClick={handleClick}>Dashboard</Nav.Link>
                    <Nav.Link as={Link} to="/user/songs" onClick={handleClick}>Songs</Nav.Link>
                    <Nav.Link as={Link} to="/user/artists" onClick={handleClick}>Artists</Nav.Link>
                    <Nav.Link as={Link} to="/user/albums" onClick={handleClick}>Albums</Nav.Link>
                    <NavDropdown title={<span className="menu-dropdown-title">Top</span>} id="basic-nav-dropdown" className="menu-dropdown">
                        <NavDropdown.Item as={Link} to="/all-time-top" onClick={handleClick}>All time top</NavDropdown.Item>
                        <NavDropdown.Item as={Link} to="/top-global" onClick={handleClick}>Top Global</NavDropdown.Item>
                        <NavDropdown.Item as={Link} to="/top-usa" onClick={handleClick}>Top USA</NavDropdown.Item>
                        <NavDropdown.Item as={Link} to="/top-spain" onClick={handleClick}>Top Spain</NavDropdown.Item>
                        <NavDropdown.Item as={Link} to="/top-uk" onClick={handleClick}>Top UK</NavDropdown.Item>
                        <NavDropdown.Item as={Link} to="/top-argentina" onClick={handleClick}>Top Argentina</NavDropdown.Item>
                        <NavDropdown.Item as={Link} to="/top-australia" onClick={handleClick}>Top Australia</NavDropdown.Item>
                        <NavDropdown.Item as={Link} to="/top-canada" onClick={handleClick}>Top Canada</NavDropdown.Item>
                        <NavDropdown.Item as={Link} to="/top-colombia" onClick={handleClick}>Top Colombia</NavDropdown.Item>
                        <NavDropdown.Item as={Link} to="/top-france" onClick={handleClick}>Top France</NavDropdown.Item>
                        <NavDropdown.Item as={Link} to="/top-germany" onClick={handleClick}>Top Germany</NavDropdown.Item>
                        <NavDropdown.Item as={Link} to="/top-italy" onClick={handleClick}>Top Italy</NavDropdown.Item>
                        <NavDropdown.Item as={Link} to="/top-japan" onClick={handleClick}>Top Japan</NavDropdown.Item>
                        <NavDropdown.Item as={Link} to="/top-south-korea" onClick={handleClick}>Top South Korea</NavDropdown.Item>
                    </NavDropdown>
                </Nav>
            </Navbar.Collapse>
        </Navbar>
    );
};

export default SideMenu;
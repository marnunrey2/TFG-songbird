import React from 'react';
import { Navbar, Button, Dropdown } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';
import '../styles/Navbar.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import avatar from '../media/avatar.png';

const CustomNavbarUsers = () => {
    const navigate = useNavigate();
    const user = JSON.parse(localStorage.getItem('user'));  

    const logout = () => {
      localStorage.removeItem('user');  
      navigate('/');
    };

  return (
    <>
      <Navbar className="custom-navbar" fixed="top" >
        <Navbar.Brand
            as={Link}
            to="/dashboard"
            className="navbar-brand-users"
        >
          <img src={`${process.env.PUBLIC_URL}/logo-bg.png`} height={40} alt="Songbird" />
        </Navbar.Brand>
      </Navbar>
      <Dropdown>
        <Dropdown.Toggle variant="outline-light" id="dropdown-basic" className="custom-dropdown">
            <img src={avatar} alt="avatar" style={{width: '30px', height: '30px', borderRadius: '50%'}} /> {user.username}
        </Dropdown.Toggle>

        <Dropdown.Menu style={{maxHeight: '110px'}}>
            <Dropdown.Item as={Link} to="/profile">Profile</Dropdown.Item>
            <Button className='dropdown-button' variant="primary" onClick={logout}>Logout</Button>
        </Dropdown.Menu>
      </Dropdown>
    </>
  );
};

export default CustomNavbarUsers;

import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Alert, Button, Form, Container, Row, Col } from 'react-bootstrap';
import CustomNavbar from '../../components/Navbar';

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    const formGroupStyle = { marginTop: '20px' };
    const navigate = useNavigate();

    const handleSubmit = (event) => {
        event.preventDefault();

        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);

        axios.post('http://localhost:8000/api/login/', formData)
            .then(response => {
                console.log(response);
                console.log(JSON.stringify(response.data));
                localStorage.setItem('user', JSON.stringify(response.data)); 
                navigate('/dashboard');
            })
            .catch(error => {
                if (error.response && error.response.status === 400) {
                    setErrorMessage('Invalid username or password');
                } else {
                    console.log(error);
                }
            });
    };

    return (
        <div className='App'>
            <CustomNavbar />
            <Container>
                <Row className="justify-content-md-center">
                    <Col md={4}>
                        <h1>Login</h1>
                        <Form onSubmit={handleSubmit}>
                            {errorMessage && <Alert variant="danger">{errorMessage}</Alert>}

                            <Form.Group controlId="formBasicUsername" style={formGroupStyle}>
                                <Form.Label>Username</Form.Label>
                                <Form.Control type="text" placeholder="Enter username" value={username} onChange={e => setUsername(e.target.value)} required />
                            </Form.Group>

                            <Form.Group controlId="formBasicPassword" style={formGroupStyle}>
                                <Form.Label>Password</Form.Label>
                                <Form.Control type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
                            </Form.Group>

                            <Button variant="primary" type="submit">
                                Login
                            </Button>
                        </Form>
                    </Col>
                </Row>
            </Container>
        </div>
    );
}

export default Login;
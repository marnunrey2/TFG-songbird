import React, { useState } from 'react';
import { Form, Button, Alert, Container, Row, Col } from 'react-bootstrap';
import axios from 'axios';
import CustomNavbar from '../../components/Navbar';
import '../../styles/RegisterForms.css'; 

function SignUp() {
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [successMessage, setSuccessMessage] = useState('');

    const formGroupStyle = { marginTop: '20px' };

    const handleSubmit = (event) => {
        event.preventDefault();

        if (!firstName || !lastName || !username || !email || !password) {
            setErrorMessage('Fill in all required fields');
            window.scrollTo(0, 0);  
            return;
        }

        if (password !== confirmPassword) {
            setErrorMessage('Passwords do not match');
            window.scrollTo(0, 0);  
            return;
        }

        const formData = new FormData();
        formData.append('username', username);
        formData.append('email', email);
        formData.append('password', password);
        formData.append('first_name', firstName);
        formData.append('last_name', lastName);

        axios.post('http://localhost:8000/api/signup/', formData)
            .then(response => {
                setErrorMessage('');
                setSuccessMessage('User created successfully');
                setFirstName('');
                setLastName('');
                setUsername('');
                setEmail('');
                setPassword('');
                setConfirmPassword('');
                window.scrollTo(0, 0);
            })
            .catch(error => { 
                setSuccessMessage('');
                if (error.response && error.response.data && error.response.data.password) {
                    setErrorMessage(error.response.data.password.join(' '));
                    window.scrollTo(0, 0);  
                } else if (error.response && error.response.data && error.response.data.email) {
                    setErrorMessage(error.response.data.email);
                    window.scrollTo(0, 0);  
                } else if (error.response && error.response.data && error.response.data.username) {
                    setErrorMessage(error.response.data.username);
                    window.scrollTo(0, 0);  
                } else {
                    console.error(error);
                    setErrorMessage(error.message);
                    window.scrollTo(0, 0);  
                }
            });
    };

    return (
        <div className='App'>
            <CustomNavbar />
            <Container>
            <Row className="justify-content-md-center">
            <Col md={4}>
            <h1  className='white-text'>Sign Up</h1>
            <Form onSubmit={handleSubmit}>
                {errorMessage && <Alert variant="danger">{errorMessage}</Alert>}
                {successMessage && <Alert variant="success">{successMessage}</Alert>}

                <Form.Group controlId="formBasicFirstName" style={formGroupStyle}>
                    <Form.Label className='white-text'>First Name*</Form.Label>
                    <Form.Control type="text" placeholder="Enter first name" value={firstName} onChange={e => setFirstName(e.target.value)} />
                </Form.Group>
                
                <Form.Group controlId="formBasicLastName" style={formGroupStyle}>
                    <Form.Label className='white-text'>Last Name*</Form.Label>
                    <Form.Control type="text" placeholder="Enter last name" value={lastName} onChange={e => setLastName(e.target.value)} />
                </Form.Group>
                
                <Form.Group controlId="formBasicUsername" style={formGroupStyle}>
                    <Form.Label className='white-text'>Username*</Form.Label>
                    <Form.Control type="text" placeholder="Enter username" value={username} onChange={e => setUsername(e.target.value)} />
                </Form.Group>
                
                <Form.Group controlId="formBasicEmail" style={formGroupStyle}>
                    <Form.Label className='white-text'>Email address*</Form.Label>
                    <Form.Control type="email" placeholder="Enter email" value={email} onChange={e => setEmail(e.target.value)} />
                    <Form.Text className="text-muted white-text">
                        We'll never share your email with anyone else.
                    </Form.Text>
                </Form.Group>

                <Form.Group controlId="formBasicPassword" style={formGroupStyle}>
                    <Form.Label className='white-text'>Password*</Form.Label>
                    <Form.Control type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
                </Form.Group>

                <Form.Group controlId="formBasicPasswordConfirm" style={formGroupStyle}>
                    <Form.Label className='white-text'>Confirm Password*</Form.Label>
                    <Form.Control type="password" placeholder="Confirm Password" value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} />
                </Form.Group>
                
                <Button variant="primary" type="submit">
                    Register
                </Button>
            </Form>
            </Col>
            </Row>
            </Container>
        </div>
    );
}

export default SignUp;
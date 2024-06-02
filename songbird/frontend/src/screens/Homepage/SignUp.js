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
    const [avatar, setAvatar] = useState(null);
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
        if (avatar) {
            const newFile = new File([avatar], `${username}_avatar.png}`, { type: avatar.type });
            formData.append('avatar', newFile);
        } else {
            formData.append('avatar', null);
        }
        axios.post('http://localhost:8000/api/signup/', formData)
            .then(response => {
                console.log(response);
                setSuccessMessage('User created successfully');
                setFirstName('');
                setLastName('');
                setUsername('');
                setEmail('');
                setPassword('');
                setConfirmPassword('');
                setAvatar(null);
                window.scrollTo(0, 0);
            })
            .catch(error => {
                if (error.response && error.response.data && error.response.data.email) {
                    setErrorMessage('This email is already in use');
                    window.scrollTo(0, 0);  
                } else if (error.response && error.response.data && error.response.data.username) {
                    setErrorMessage('This username is already in use');
                    window.scrollTo(0, 0);  
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
            <h1>Sign Up</h1>
            <Form onSubmit={handleSubmit}>
                {errorMessage && <Alert variant="danger">{errorMessage}</Alert>}
                {successMessage && <Alert variant="success">{successMessage}</Alert>}

                <Form.Group controlId="formBasicFirstName" style={formGroupStyle}>
                    <Form.Label>First Name*</Form.Label>
                    <Form.Control type="text" placeholder="Enter first name" value={firstName} onChange={e => setFirstName(e.target.value)} />
                </Form.Group>
                
                <Form.Group controlId="formBasicLastName" style={formGroupStyle}>
                    <Form.Label>Last Name*</Form.Label>
                    <Form.Control type="text" placeholder="Enter last name" value={lastName} onChange={e => setLastName(e.target.value)} />
                </Form.Group>
                
                <Form.Group controlId="formBasicUsername" style={formGroupStyle}>
                    <Form.Label>Username*</Form.Label>
                    <Form.Control type="text" placeholder="Enter username" value={username} onChange={e => setUsername(e.target.value)} />
                </Form.Group>
                
                <Form.Group controlId="formBasicEmail" style={formGroupStyle}>
                    <Form.Label>Email address*</Form.Label>
                    <Form.Control type="email" placeholder="Enter email" value={email} onChange={e => setEmail(e.target.value)} />
                    <Form.Text className="text-muted">
                        We'll never share your email with anyone else.
                    </Form.Text>
                </Form.Group>

                <Form.Group controlId="formBasicPassword" style={formGroupStyle}>
                    <Form.Label>Password*</Form.Label>
                    <Form.Control type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
                </Form.Group>

                <Form.Group controlId="formBasicPasswordConfirm" style={formGroupStyle}>
                    <Form.Label>Confirm Password*</Form.Label>
                    <Form.Control type="password" placeholder="Confirm Password" value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} />
                </Form.Group>
                
                <Form.Group controlId="formBasicAvatar" style={formGroupStyle}>
                    <Form.Label>Avatar</Form.Label>
                    <Form.Control type="file" placeholder="Enter avatar" value={avatar} onChange={e => setAvatar(e.target.value)} />
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
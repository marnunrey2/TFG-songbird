import React from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';
import UsersTemplate from '../../components/UsersTemplate';

function Profile() {
    const user = JSON.parse(localStorage.getItem('user'));

    return (
        <UsersTemplate>
        <Container style={{marginTop: '40px'}}>
            <Row className="justify-content-md-center">
                <Col md={6}>
                    <Card>
                        <Card.Body>
                            <Card.Title>Profile</Card.Title>
                            <Card.Text>
                                <strong>First Name:</strong> {user.first_name} <br />
                                <strong>Last Name:</strong> {user.last_name} <br />
                                <strong>Username:</strong> {user.username} <br />
                                <strong>Email:</strong> {user.email} <br />
                                <strong>Password:</strong> {'*'.repeat(8)}
                            </Card.Text>
                        </Card.Body>
                    </Card>
                </Col>
            </Row>
        </Container>
        </UsersTemplate>
    );
}

export default Profile;
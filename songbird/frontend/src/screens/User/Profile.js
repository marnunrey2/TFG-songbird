import React from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';
import UsersTemplate from '../../components/UsersTemplate';
import '../../styles/UserStyles.css';

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
                            <Card.Text style={{display: 'flex', justifyContent: 'center'}}>
                                <table>
                                    <tbody>
                                        <tr>
                                            <td className='table-td-1'><strong>First Name:</strong></td>
                                            <td className='table-td-2'>{user.first_name}</td>
                                        </tr>
                                        <tr>
                                            <td className='table-td-1'><strong>Last Name:</strong></td>
                                            <td className='table-td-2'>{user.last_name}</td>
                                        </tr>
                                        <tr>
                                            <td className='table-td-1'><strong>Username:</strong></td>
                                            <td className='table-td-2'>{user.username}</td>
                                        </tr>
                                        <tr>
                                            <td className='table-td-1'><strong>Email:</strong></td>
                                            <td className='table-td-2'>{user.email}</td>
                                        </tr>
                                        <tr>
                                            <td className='table-td-1'><strong>Password:</strong></td>
                                            <td className='table-td-2'>{'*'.repeat(8)}</td>
                                        </tr>
                                    </tbody>
                                </table>
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
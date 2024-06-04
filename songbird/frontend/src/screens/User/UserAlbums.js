import React, { useState } from 'react';
import UsersTemplate from '../../components/UsersTemplate';
import '../../styles/Colors.css';
import '../../styles/UserStyles.css';
import cd from '../../media/cd.png';
import { useFetchAlbums } from '../../components/useFetchData'; 
import { Container, Row, Col, Image } from 'react-bootstrap';


function UserAlbums() {
    const [searchTerm, setSearchTerm] = useState('');
    const albums = useFetchAlbums(searchTerm);

    console.log(albums);

    const handleSearchChange = (event) => {
        setSearchTerm(event.target.value);
    };

    return (
        <UsersTemplate>
        <div className="search-container">
            <input 
                type="text" 
                value={searchTerm} 
                onChange={handleSearchChange} 
                className="search-input" 
                placeholder="Search for albums..." 
            />
        </div>
        <Container className="info">
        {albums.map((album, index) => (
            <div key={index}  className="info-card">
                <Row className="card-content">
                    <Col md={4} className="song-image">
                        {album && album.images ? (
                            <Image src={album.images} onError={(e)=>{e.target.onerror = null; e.target.src=cd}} className="song-img" rounded />
                        ) : (
                            <div className="placeholder">
                                <Image src={cd} onError={(e)=>{e.target.onerror = null; e.target.src=cd}} className="song-img" rounded />
                            </div>
                        )}
                    </Col>
                    <Col md={4} className="song-info">
                        <div className="song-name">{album ? album.name : ''}</div>
                        <div className="artist-name">{album && album.release_date ? album.release_date : 'None'}</div>                    
                    </Col>
                </Row>
            </div>
        ))}
        </Container>
        </UsersTemplate>
    );
}

export default UserAlbums;
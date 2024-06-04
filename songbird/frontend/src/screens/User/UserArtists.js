import React, { useState } from 'react';
import UsersTemplate from '../../components/UsersTemplate';
import '../../styles/Colors.css';
import '../../styles/UserStyles.css';
import avatar from '../../media/avatar.png';
import { useFetchArtists } from '../../components/useFetchData'; 
import { HeartFill, Heart } from 'react-bootstrap-icons';
import { Container, Row, Col, Image } from 'react-bootstrap';

function UserArtists() {
    const [searchTerm, setSearchTerm] = useState('');
    const artists = useFetchArtists(searchTerm);
    const [favorite, setFavorite] = useState({});

    console.log(artists);

    const handleFavoriteClick = (index) => {
        setFavorite(prevState => ({...prevState, [index]: !prevState[index]}));
    };

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
                placeholder="Search for artists..." 
            />
        </div>
        <Container className="info">
        {artists.map((artist, index) => (
            <div key={index}  className="info-card">
                <Row className="card-content">
                    <Col md={4} className="song-image">
                        {artist && artist.images ? (
                            <Image src={artist.images} onError={(e)=>{e.target.onerror = null; e.target.src=avatar}} className="song-img" rounded />
                        ) : (
                            <div className="placeholder">
                                <Image src={avatar} onError={(e)=>{e.target.onerror = null; e.target.src=avatar}} className="song-img" rounded />
                            </div>
                        )}
                    </Col>
                    <Col md={4} className="song-info">
                        <div className="song-name">{artist ? artist.name : ''}</div>
                        <div className="artist-name">{artist && artist.followers ? JSON.stringify(artist.followers) : ''}</div>                    
                    </Col>
                    <Col md={4} className="song-info">
                    <div onClick={() => handleFavoriteClick(index)} className="heart-icon">
                        {favorite[index] ? <HeartFill color="red" size={20} /> : <Heart color="black" size={20} />}
                    </div>
                    </Col>
                </Row>
            </div>
        ))}
        </Container>
        </UsersTemplate>
    );
}

export default UserArtists;
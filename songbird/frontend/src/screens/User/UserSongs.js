import React, { useState } from 'react';
import UsersTemplate from '../../components/UsersTemplate';
import '../../styles/Colors.css';
import '../../styles/UserStyles.css';
import cd from '../../media/cd.png';
import { useFetchSongs } from '../../components/useFetchData'; 
import { HeartFill, Heart } from 'react-bootstrap-icons';
import { Container, Row, Col, Image } from 'react-bootstrap';
import { Link } from 'react-router-dom';

function UserSongs() {
    const [searchTerm, setSearchTerm] = useState('');
    const songs = useFetchSongs(searchTerm);
    const [favorite, setFavorite] = useState({});

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
                placeholder="Search for songs..." 
            />
        </div>
        <Container className="info">
        {songs.map((song, index) => (
            <Link to={`/song/${song.id}`} key={index} className="info-card">
                <Row className="card-content">
                    <Col md={4} className="song-image">
                        {song && song.images ? (
                            <Image src={song.images} onError={(e)=>{e.target.onerror = null; e.target.src=cd}} className="song-img" rounded />
                        ) : song && song.album && song.album.images ? (
                            <Image src={song.album.images} onError={(e)=>{e.target.onerror = null; e.target.src=cd}} className="song-img" rounded />
                        ) : song && song.album_images ? (
                            <Image src={song.album_images} onError={(e)=>{e.target.onerror = null; e.target.src=cd}} className="song-img" rounded />
                        ) : (
                            <div className="placeholder">
                                <Image src={cd} onError={(e)=>{e.target.onerror = null; e.target.src=cd}} className="song-img" rounded />
                            </div>
                        )}
                    </Col>
                    <Col md={4} className="song-info">
                        <div className="song-name">{song ? song.name : ''}</div>
                        <div className="artist-name">{song && song.main_artist ? song.main_artist.name ? song.main_artist.name : song.main_artist : ''}</div>
                        {/* <div className="album-name">{song && song.album ? song.album.name ? song.album.name : song.album : ''}</div> */}
                    </Col>
                    <Col md={4} className="song-info">
                    <div onClick={() => handleFavoriteClick(index)} className="heart-icon">
                        {favorite[index] ? <HeartFill color="red" size={20} /> : <Heart color="black" size={20} />}
                    </div>
                    </Col>
                </Row>
            </Link>
        ))}
        </Container>
        </UsersTemplate>
    );
}

export default UserSongs;
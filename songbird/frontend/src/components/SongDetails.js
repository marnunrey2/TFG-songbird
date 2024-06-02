import React, { useEffect, useState } from 'react';
import axios from 'axios';
import UsersTemplate from './UsersTemplate';
import cd from '../media/cd.png';
import { HeartFill, Heart } from 'react-bootstrap-icons';
import { useParams } from 'react-router-dom';
import { Container, Row, Col, Image } from 'react-bootstrap';
import { FaSpotify, FaYoutube, FaApple, FaDeezer } from 'react-icons/fa';

function SongDetails() {
    const [song, setSong] = useState(null);
    const [favorite, setFavorite] = useState({});

    const { id } = useParams(); 

    useEffect(() => {
        axios.get(`http://localhost:8000/api/songs/${id}`)
            .then(response => {
                console.log(response.data);
                setSong(response.data);
            });
    }, [id]);

    const handleFavoriteClick = () => {
        setFavorite(prevState => ({...prevState, [id]: !prevState[id]}));
    };

    const formatDuration = (duration) => {
        const minutes = Math.floor(duration / 60);
        const seconds = duration % 60;
        return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    };

    const renderAvailabilityIcons = () => {
        const icons = {
            'Spotify': <FaSpotify size={40} color="#1DB954" />,
            'YouTube': <FaYoutube size={40} color="#FF0000" />,
            'Apple Music': <FaApple size={40} color="#000000" />,
            'Deezer': <FaDeezer size={40} color="#00A4DC" />,
            // Add more services here if needed
        };

        return song.available_at.map(service => (
            <span key={service} className="mr-2">
                {icons[service]}
            </span>
        ));
    };

    if (!song) {
        return <div>Loading...</div>;
    }

    return (
        <UsersTemplate>
        <Container className="info">
            <div className="details-card">
                <Row className="details-card-content">
                    <Col md={4} className="details-song-image">
                        {song && song.images ? (
                            <Image src={song.images} alt={song.name} className="song-img-details" rounded />
                        ) : song && song.album && song.album.images ? (
                            <Image src={song.album.images} alt={song.name} className="song-img-details" rounded />
                        ) : song && song.album_images ? (
                            <Image src={song.album_images} alt={song.name} className="song-img-details" rounded />
                        ) : (
                            <div className="placeholder">
                                <Image src={cd} alt={song.name} className="song-img-details" rounded />
                            </div>
                        )}
                    </Col>
                    <Col md={4} className="song-details">
                        <h2>{song ? song.name : ''}</h2>
                        <h6><strong>Artist: </strong>{song && song.main_artist ? song.main_artist.name ? song.main_artist.name : song.main_artist : ''}</h6>
                        {song.collaborators.length > 0 && (
                            <h6><strong>Collaborators: </strong>{song.collaborators.map(collab => collab.name).join(', ')}</h6>
                        )}
                        <h6><strong>Album: </strong>{song && song.album ? song.album.name ? song.album.name : song.album : ''}</h6>
                    </Col>
                    <Col md={4} className="song-details" style={{marginTop: '70px', marginLeft: '70px'}}>
                        {song.release_date && <h6><strong>Release Date: </strong>{new Date(song.release_date).toLocaleDateString()}</h6>}
                        <h6><strong>Duration: </strong>{formatDuration(song.duration)}</h6>
                        <h6><strong>Genre: </strong>{song.album?.genre.join(', ')}</h6>
                        <h6><strong>Explicit: </strong>{song.explicit ? 'Yes' : 'No'}</h6>
                    </Col>
                    <Col md={4} className="song-details">
                        <div onClick={handleFavoriteClick} className="heart-icon">
                            {favorite[id] ? <HeartFill color="red" size={30} /> : <Heart color="black" size={30} />}
                        </div>
                    </Col>
                </Row>
                <Row className="details-card-content" style={{ marginTop: '40px' }}>
                    <Col className='song-details'>
                        <h3>Lyrics</h3>
                        <p>{song.lyrics? song.lyrics : 'No lyrics'}</p>
                    </Col>
                    <Col className='song-details'>
                        <h6><strong>Available at: </strong></h6>
                        <h6>{renderAvailabilityIcons()}</h6>
                    </Col>
                </Row>
            </div>
        </Container>
        </UsersTemplate>
    );
}

export default SongDetails;
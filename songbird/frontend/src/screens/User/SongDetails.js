import React, { useState } from 'react';
import UsersTemplate from '../../components/UsersTemplate';
import cd from '../../media/cd.png';
import { HeartFill, Heart } from 'react-bootstrap-icons';
import { useParams } from 'react-router-dom';
import { Container, Row, Col, Image } from 'react-bootstrap';
import { FaSpotify, FaYoutube, FaApple, FaDeezer } from 'react-icons/fa';
import { togglePostLikes, useFetchSongData } from '../../components/useFetchData';

function SongDetails() {
    const { id } = useParams(); 
    const song = useFetchSongData(id);
    const [user, setUser] = useState(JSON.parse(localStorage.getItem('user')));

    const handleFavoriteClick = async () => {
        await togglePostLikes(user, setUser, song, Number(id));
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
        };

        return song.available_at.map(service => (
            <span key={service} style={{marginRight: '10px'}}>
                {icons[service]}
            </span>
        ));
    };
    
    const renderLyrics = () => {
        const lyricsArray = song.lyrics.split('\n');
        const formattedLyrics = lyricsArray.reduce((acc, line) => {
            const parts = line.split('[');
            parts.forEach((part, index) => {
                if (index !== 0 && part.includes(']')) {
                    acc.push(<br />); 
                    acc.push(<strong>{'[' + part.split(']')[0] + ']'}</strong>);
                    acc.push(part.split(']')[1]);
                } else {
                    acc.push(part);
                }
            });
            return acc;
        }, []);
        return formattedLyrics.map((line, i) => <div key={i}>{line}</div>);
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
                            <Image src={song.images} onError={(e)=>{e.target.onerror = null; e.target.src=cd}} className="song-img-details" rounded />
                        ) : song && song.album && song.album.images ? (
                            <Image src={song.album.images} onError={(e)=>{e.target.onerror = null; e.target.src=cd}} className="song-img-details" rounded />
                        ) : song && song.album_images ? (
                            <Image src={song.album_images} onError={(e)=>{e.target.onerror = null; e.target.src=cd}} className="song-img-details" rounded />
                        ) : (
                            <div className="placeholder">
                                <Image src={cd} onError={(e)=>{e.target.onerror = null; e.target.src=cd}} className="song-img-details" rounded />
                            </div>
                        )}
                    </Col>
                    <Col md={4} className="song-details">
                        {song.name && <h2>{song.name}</h2>}
                        <h6><strong>Artist: </strong>{song && song.main_artist ? song.main_artist.name ? song.main_artist.name : song.main_artist : ''}</h6>
                        {song.collaborators.length > 0 && (
                            <h6><strong>Collaborators: </strong>{song.collaborators.map(collab => collab.name).join(', ')}</h6>
                        )}
                        {song.album && <h6><strong>Album: </strong>{song.album.name}</h6>}
                    </Col>
                    <Col xs={12} md={4} className="song-details mt-3 mt-md-5 ml-md-5 order-1 order-md-0">                        {song.release_date && <h6><strong>Release Date: </strong>{new Date(song.release_date).toLocaleDateString()}</h6>}
                        {song.duration && <h6><strong>Duration: </strong>{formatDuration(song.duration)} min</h6>}
                        <h6><strong>Genre: </strong>{song.main_artist.genres.length > 0 ? song.main_artist.genres.map(genre => genre.name).join(', ') : 'No genre'}</h6>
                        <h6><strong>Explicit lyrics: </strong>{song.explicit ? 'Yes' : 'No'}</h6>
                    </Col>
                    {!user.is_superuser && 
                    <Col md={4} className="song-details">
                        <div onClick={handleFavoriteClick} className="heart-icon">
                            {user.liked_songs.map(song => song.id).includes(Number(id)) ? <HeartFill color="red" size={30} /> : <Heart color="black" size={30} />}
                        </div>
                    </Col>
                    }
                </Row>
                <Row className="details-card-content align-items-start" style={{ marginTop: '40px' }}>
                    <Col className='song-details order-1 order-md-0'>
                        <h3>Lyrics</h3>
                        {song.lyrics ? renderLyrics() : 'No lyrics'}                  
                    </Col>
                    {song.available_at.length > 0 &&
                    <Col xs={12} md={6} className='song-details order-0 order-md-1' style={{ marginBottom: '40px' }}>
                        <h6><strong>Available at: </strong></h6>
                        <h6>{renderAvailabilityIcons()}</h6>
                    </Col>
                    }
                </Row>
            </div>
        </Container>
        </UsersTemplate>
    );
}

export default SongDetails;

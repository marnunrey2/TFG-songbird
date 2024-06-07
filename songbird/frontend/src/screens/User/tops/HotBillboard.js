import React, { useState } from 'react';
import UsersTemplate from '../../../components/UsersTemplate';
import '../../../styles/Colors.css';
import '../../../styles/UserStyles.css';
import cd from '../../../media/cd.png';
import { useFetchTopPlaylists } from '../../../components/useFetchData'; 
import { Container, Row, Col, Image } from 'react-bootstrap';
import { Link } from 'react-router-dom';

function HotBillboard() {
    const playlistName = 'Hot 100 Billboard';
    const websiteName = 'Billboard';
    const [loading, setLoading] = useState(true);
    const songs = useFetchTopPlaylists(playlistName, websiteName, setLoading);

    return (
        <UsersTemplate>
        <h1>{playlistName}</h1>
        <Container className="info">
        {loading ? 'Loading...' : songs.map((song, index) => (
            <Link to={`/song/${song.song.id}`} key={index} className="info-card-album">
                <Row className="card-content">
                    <Col md={1} className="song-info">
                        <div className="song-position">{song.position ? song.position.position : ''}</div>
                    </Col>
                    <Col md={4} className="song-image">
                        {song.song && song.song.images ? (
                            <Image src={song.song.images} onError={(e)=>{e.target.onerror = null; e.target.src=cd}} className="song-img" rounded />
                        ) : song.song && song.song.album && song.song.album.images ? (
                            <Image src={song.song.album.images} onError={(e)=>{e.target.onerror = null; e.target.src=cd}} className="song-img" rounded />
                        ) : song.song && song.song.album_images ? (
                            <Image src={song.song.album_images} onError={(e)=>{e.target.onerror = null; e.target.src=cd}} className="song-img" rounded />
                        ) : (
                            <div className="placeholder">
                                <Image src={cd} onError={(e)=>{e.target.onerror = null; e.target.src=cd}} className="song-img" rounded />
                            </div>
                        )}
                    </Col>
                    <Col md={4} className="song-info text-center-md-down">
                        <div className="song-name">{song.song ? song.song.name : ''}</div>
                        <div className="artist-name">{song.song && song.song.main_artist ? song.song.main_artist.name ? song.song.main_artist.name : song.song.main_artist : ''}</div>
                    </Col>
                </Row>
            </Link>
        ))}
        </Container>
        </UsersTemplate>
    );
}

export default HotBillboard;
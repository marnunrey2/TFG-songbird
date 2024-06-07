import React, { useState } from 'react';
import { useFetchRecommendations, togglePostLikes } from '../../components/useFetchData';
import UsersTemplate from '../../components/UsersTemplate';
import cd from '../../media/cd.png';
import { Container, Row, Col, Image } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { HeartFill, Heart } from 'react-bootstrap-icons';

const Recommendations = () => {

    const [loading, setLoading] = useState(true);
    const [user, setUser] = useState(JSON.parse(localStorage.getItem('user')));
    const songs = useFetchRecommendations(user.id, setLoading);

    const handleFavoriteClick = async (event, index) => {
        event.preventDefault(); 
        event.stopPropagation();

        const song = songs[index].song;
        await togglePostLikes(user, setUser, song, song.id);

    };

    return (
        <UsersTemplate>
        <h1>Recommended Songs Just For You</h1>
        <Container className="info">
        {loading ? 'Loading...' : songs.map(({song, score}, index) => (
            <Link to={`/song/${song.id}`} key={index} className="info-card-album">
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
                    <Col md={4} className="song-info text-center-md-down">
                        <div className="song-name">{song ? song.name : ''}</div>
                        <div className="artist-name">{song && song.main_artist ? song.main_artist.name ? song.main_artist.name : song.main_artist : ''}</div>
                        {/* <div className="album-name">{song && song.album ? song.album.name ? song.album.name : song.album : ''}</div> */}
                    </Col>
                    <Col md={4} className="song-info">
                    <div onClick={(event) => handleFavoriteClick(event, index)} className="heart-icon">
                        {user.liked_songs.map(song => song.id).includes(song.id) ? <HeartFill color="red" size={20} /> : <Heart color="black" size={20} />}
                    </div>
                    </Col>
                </Row>
            </Link>
        ))}
        </Container>
        </UsersTemplate>
    );
};

export default Recommendations;

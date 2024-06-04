import React, { useState } from 'react';
import axios from 'axios';
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
    const [user, setUser] = useState(JSON.parse(localStorage.getItem('user')));

    const handleFavoriteClick = (event, index) => {
        event.preventDefault(); 
        event.stopPropagation();

        const songId = songs[index].id;
        const userId = user.id;

        let updatedUser = { ...user };
        let isSongLiked = updatedUser.liked_songs.map(song => song.id).includes(songId);
    
        let requestUrl = isSongLiked ? 'http://localhost:8000/api/user/unlike_song/' : 'http://localhost:8000/api/user/like_song/';
        axios.post(requestUrl, { user_id: userId, song_id: songId }, {
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then(response => {
                console.log(response);

            // Update the liked_songs in the user object
            if (isSongLiked) {
                updatedUser.liked_songs = updatedUser.liked_songs.filter(song => song.id !== songId);
            } else {
                updatedUser.liked_songs.push(songs[index]);
            }
            // Update the user object in the localStorage
            setUser(updatedUser);
            localStorage.setItem('user', JSON.stringify(updatedUser));
            })
            .catch(error => {
                console.log(error);
            });
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
}

export default UserSongs;
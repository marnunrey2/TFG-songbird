import React, { useState } from 'react';
import UsersTemplate from '../../components/UsersTemplate';
import '../../styles/Colors.css';
import '../../styles/UserStyles.css';
import cd from '../../media/cd.png';
import { useFetchSongs } from '../../components/useFetchData'; 
import { HeartFill, Heart } from 'react-bootstrap-icons';

function UserSongs() {
    const [searchTerm, setSearchTerm] = useState('');
    const songs = useFetchSongs(searchTerm);
    const [favorite, setFavorite] = useState({});

    console.log(songs);

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
        <div className="info">
        {songs.map((song, index) => (
            <div key={index}  className="info-card">
                <div className="card-content">
                    <div className="song-image">
                        {song && song.images ? (
                            <img src={song.images} alt={song.name} className="song-img" />
                        ) : song && song.album && song.album.images ? (
                            <img src={song.album.images} alt={song.name} className="song-img" />
                        ) : song && song.album_images ? (
                            <img src={song.album_images} alt={song.name} className="song-img" />
                        ) : (
                            <div className="placeholder">
                                <img src={cd} alt={song ? song.name : ''} className="song-img" />
                            </div>
                        )}
                    </div>
                    <div className="song-info">
                        <div className="song-name">{song ? song.name : ''}</div>
                        <div className="artist-name">{song && song.main_artist ? song.main_artist.name ? song.main_artist.name : song.main_artist : ''}</div>
                        <div className="album-name">{song && song.album ? song.album.name ? song.album.name : song.album : ''}</div>
                    </div>
                    <div onClick={() => handleFavoriteClick(index)} className="heart-icon">
                        {favorite[index] ? <HeartFill color="red" size={20} /> : <Heart color="black" size={20} />}
                    </div>
                </div>
            </div>
        ))}
        </div>
        </UsersTemplate>
    );
}

export default UserSongs;
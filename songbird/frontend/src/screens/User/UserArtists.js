import React, { useState } from 'react';
import UsersTemplate from '../../components/UsersTemplate';
import '../../styles/Colors.css';
import '../../styles/UserStyles.css';
import avatar from '../../media/avatar.png';
import { useFetchArtists } from '../../components/useFetchData'; 
import { HeartFill, Heart } from 'react-bootstrap-icons';


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
        <div className="info">
        {artists.map((artist, index) => (
            <div key={index}  className="info-card">
                <div className="card-content">
                    <div className="song-image">
                        {artist && artist.images ? (
                            <img src={artist.images} alt={artist.name} className="song-img" />
                        ) : (
                            <div className="placeholder">
                                <img src={avatar} alt={artist ? artist.name : ''} className="song-img" />
                            </div>
                        )}
                    </div>
                    <div className="song-info">
                        <div className="song-name">{artist ? artist.name : ''}</div>
                        <div className="artist-name">{artist && artist.followers ? JSON.stringify(artist.followers) : ''}</div>                    
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

export default UserArtists;
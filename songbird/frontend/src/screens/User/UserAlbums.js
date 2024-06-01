import React, { useState } from 'react';
import UsersTemplate from '../../components/UsersTemplate';
import '../../styles/Colors.css';
import '../../styles/UserStyles.css';
import cd from '../../media/cd.png';
import { useFetchAlbums } from '../../components/useFetchData'; 
import { HeartFill, Heart } from 'react-bootstrap-icons';


function UserAlbums() {
    const [searchTerm, setSearchTerm] = useState('');
    const albums = useFetchAlbums(searchTerm);
    const [favorite, setFavorite] = useState({});

    console.log(albums);

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
                placeholder="Search for albums..." 
            />
        </div>
        <div className="info">
        {albums.map((album, index) => (
            <div key={index}  className="info-card">
                <div className="card-content">
                    <div className="song-image">
                        {album && album.images ? (
                            <img src={album.images} alt={album.name} className="song-img" />
                        ) : (
                            <div className="placeholder">
                                <img src={cd} alt={album ? album.name : ''} className="song-img" />
                            </div>
                        )}
                    </div>
                    <div className="song-info">
                        <div className="song-name">{album ? album.name : ''}</div>
                        <div className="artist-name">{album && album.release_date ? album.release_date : 'None'}</div>                    
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

export default UserAlbums;
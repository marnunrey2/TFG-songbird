import React, { useState, useEffect } from 'react';
import UsersTemplate from '../../components/UsersTemplate';
import '../../styles/Colors.css';
import '../../styles/UserStyles.css';
import cd from '../../media/cd.png';
import { useFetchAlbums } from '../../components/useFetchData'; 
import { Container, Row, Col, Image } from 'react-bootstrap';
import { Link } from 'react-router-dom';


function useDebounce(value, delay) {
    const [debouncedValue, setDebouncedValue] = useState(value);
  
    useEffect(() => {
      const handler = setTimeout(() => {
        setDebouncedValue(value);
      }, delay);
  
      return () => {
        clearTimeout(handler);
      };
    }, [value, delay]);
  
    return debouncedValue;
}

function UserAlbums() {
    const [searchTerm, setSearchTerm] = useState('');
    const debouncedSearchTerm = useDebounce(searchTerm, 1000);
    const albums = useFetchAlbums(debouncedSearchTerm);

    console.log(albums);

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
        <Container className="info">
        {albums.map((album, index) => (
            <Link to={`/album/${album.id}`} key={index} className="info-card-album">
                <Row className="card-content">
                    <Col md={4} className="song-image">
                        {album && album.images ? (
                            <Image src={album.images} onError={(e)=>{e.target.onerror = null; e.target.src=cd}} className="song-img" rounded />
                        ) : (
                            <div className="placeholder">
                                <Image src={cd} onError={(e)=>{e.target.onerror = null; e.target.src=cd}} className="song-img" rounded />
                            </div>
                        )}
                    </Col>
                    <Col md={4} className="song-info text-center-md-down">
                        <div className="song-name">{album ? album.name : ''}</div>
                        <div className="artist-name">{album && album.release_date ? album.release_date : 'None'}</div>                    
                    </Col>
                </Row>
            </Link>
        ))}
        </Container>
        </UsersTemplate>
    );
}

export default UserAlbums;
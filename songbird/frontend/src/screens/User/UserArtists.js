import React, { useState, useEffect } from 'react';
import UsersTemplate from '../../components/UsersTemplate';
import '../../styles/Colors.css';
import '../../styles/UserStyles.css';
import avatar from '../../media/avatar.png';
import { useFetchArtists } from '../../components/useFetchData'; 
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
  

function UserArtists() {
    const [searchTerm, setSearchTerm] = useState('');
    const debouncedSearchTerm = useDebounce(searchTerm, 1000);
    const artists = useFetchArtists(debouncedSearchTerm);

    console.log(artists);

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
        <Container className="info">
        {artists.map((artist, index) => (
            <Link to={`/artist/${artist.name}`} key={index} className="info-card">
                <Row className="card-content">
                    <Col xs={12} md={4} className="song-image text-center-md-down">
                        {artist && artist.images ? (
                            <Image src={artist.images} onError={(e)=>{e.target.onerror = null; e.target.src=avatar}} className="song-img" rounded />
                        ) : (
                            <div className="placeholder">
                                <Image src={avatar} onError={(e)=>{e.target.onerror = null; e.target.src=avatar}} className="song-img" rounded />
                            </div>
                        )}
                    </Col>
                    <Col xs={12} md={4} className="song-info text-center-md-down">
                        <div className="song-name">{artist ? artist.name : ''}</div>
                    </Col>
                </Row>
            </Link>
        ))}
        </Container>
        </UsersTemplate>
    );
}

export default UserArtists;
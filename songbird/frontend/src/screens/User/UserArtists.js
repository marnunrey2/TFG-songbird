import React, { useState, useEffect } from 'react';
import UsersTemplate from '../../components/UsersTemplate';
import '../../styles/Colors.css';
import '../../styles/UserStyles.css';
import avatar from '../../media/avatar.png';
import { useFetchArtists, useFetchGenres } from '../../components/useFetchData'; 
import { Container, Row, Col, Image, Dropdown } from 'react-bootstrap';
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
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState('All');
    const [genre, setGenre] = useState('No genre');

    const debouncedSearchTerm = useDebounce(searchTerm, 1000);
    const genres = useFetchGenres();
    const user = JSON.parse(localStorage.getItem('user'));

    const artists = useFetchArtists(debouncedSearchTerm, genre, setLoading);

    const handleSearchChange = (event) => {
        setLoading(true);
        setFilter('All');
        setGenre('No genre');
        setSearchTerm(event.target.value);
    };

    const handleSelectFilter = (selectedFilter) => {
        setFilter(selectedFilter);
    };

    const handleSelectGenre = (selectedGenre) => {
        setLoading(true);
        setGenre(selectedGenre);
    };

    let filteredArtists;

    if (filter === 'Liked' && genre === 'No genre') {
        filteredArtists = user.liked_songs.flatMap(song => [song.main_artist, ...song.collaborators]);
    } else if (filter === 'Liked' && genre !== 'No genre') {
        const likedArtists = user.liked_songs.flatMap(song => [song.main_artist, ...song.collaborators]);
        filteredArtists = likedArtists.filter(artist => artist.genres.some(g => g.name === genre));
    } else {
        filteredArtists = artists;
    }


    return (
        <UsersTemplate>
        <Row >
            <Col xs lg="12" className="search-container">
                <input 
                    type="text" 
                    value={searchTerm} 
                    onChange={handleSearchChange} 
                    className="search-input" 
                    placeholder="Search for artists..." 
                />
            </Col>
        </Row>
        <Row className="search-container" style={{marginTop: 0, width: '95%'}}>
            <Col xs lg="1" className='filter-title'>Filter by:</Col>
            <Col xs lg="2">
                <Dropdown onSelect={handleSelectFilter}>
                    <Dropdown.Toggle variant="success" id="dropdown-basic"  className='website-dropdown filter'>
                        {filter}
                    </Dropdown.Toggle>

                    <Dropdown.Menu>
                        <Dropdown.Item eventKey='All'>All artists</Dropdown.Item>
                        <Dropdown.Item eventKey='Liked'>Liked artists</Dropdown.Item>
                    </Dropdown.Menu>
                </Dropdown>
            </Col>
            <Col xs lg="2">
                <Dropdown onSelect={handleSelectGenre}>
                    <Dropdown.Toggle variant="success" id="dropdown-basic"  className='website-dropdown filter'>
                        {genre}
                    </Dropdown.Toggle>
                    <Dropdown.Menu>
                        <Dropdown.Item eventKey={'No genre'}>No genre</Dropdown.Item>
                        {genres.map((genre, index) => (
                            <Dropdown.Item key={index} eventKey={genre}>{genre}</Dropdown.Item>
                        ))}
                    </Dropdown.Menu>
                </Dropdown>
            </Col>
        </Row>
        <Container className="info">
        {loading ? 'Loading...' : filteredArtists.length > 0 ? filteredArtists.map((artist, index) => (
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
        )) : <h2 style={{color: 'white'}}>No artists found</h2>}
        </Container>
        </UsersTemplate>
    );
}

export default UserArtists;
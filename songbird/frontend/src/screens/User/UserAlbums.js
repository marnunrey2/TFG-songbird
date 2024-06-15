import React, { useState, useEffect } from 'react';
import UsersTemplate from '../../components/UsersTemplate';
import '../../styles/Colors.css';
import '../../styles/UserStyles.css';
import cd from '../../media/cd.png';
import { useFetchAlbums, useFetchGenres } from '../../components/useFetchData'; 
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

function UserAlbums() {
    const [searchTerm, setSearchTerm] = useState('');
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState('All');
    const [genre, setGenre] = useState('No genre');

    const debouncedSearchTerm = useDebounce(searchTerm, 1000);
    const genres = useFetchGenres();
    const user = JSON.parse(localStorage.getItem('user'));

    const albums = useFetchAlbums(debouncedSearchTerm, genre, setLoading);

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

    let filteredAlbums;

    if (filter === 'Liked' && genre === 'No genre') {
        filteredAlbums = user.liked_songs.map(song => song.album);
    } else if (filter === 'Liked' && genre !== 'No genre') {
        filteredAlbums = user.liked_songs.map(song => song.album).filter(album => album.artist.genres.some(g => g.name === genre));
    } else {
        filteredAlbums = albums;
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
                    placeholder="Search for albums..." 
                />
            </Col>
        </Row>
        {!user.is_superuser && 
        <Row className="search-container" style={{marginTop: 0, width: '95%'}}>
            <Col xs lg="1" className='filter-title'>Filter by:</Col>
            <Col xs lg="2">
                <Dropdown onSelect={handleSelectFilter}>
                    <Dropdown.Toggle variant="success" id="dropdown-basic"  className='website-dropdown filter'>
                        {filter}
                    </Dropdown.Toggle>

                    <Dropdown.Menu>
                        <Dropdown.Item eventKey='All'>All albums</Dropdown.Item>
                        <Dropdown.Item eventKey='Liked'>Liked albums</Dropdown.Item>
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
        }
        <Container className="info">
        {loading ? 'Loading...' : filteredAlbums.length > 0 ? filteredAlbums.map((album, index) => (
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
        )) : <h2 style={{color: 'white'}}>No songs found</h2>}
        </Container>
        </UsersTemplate>
    );
}

export default UserAlbums;
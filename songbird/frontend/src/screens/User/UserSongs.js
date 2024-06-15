import React, { useState, useEffect } from 'react';
import UsersTemplate from '../../components/UsersTemplate';
import '../../styles/Colors.css';
import '../../styles/UserStyles.css';
import cd from '../../media/cd.png';
import { useFetchSongs, togglePostLikes, useFetchGenres } from '../../components/useFetchData'; 
import { HeartFill, Heart } from 'react-bootstrap-icons';
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

function UserSongs() {
    const [searchTerm, setSearchTerm] = useState('');
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState('All');
    const [genre, setGenre] = useState('No genre');

    const debouncedSearchTerm = useDebounce(searchTerm, 1000);
    const genres = useFetchGenres();
    const [user, setUser] = useState(JSON.parse(localStorage.getItem('user')));

    const songs = useFetchSongs(debouncedSearchTerm, genre, setLoading);

    const handleFavoriteClick = async (event, songId) => {
        event.preventDefault(); 
        event.stopPropagation();

        const song = songs.find(song => song.id === songId);
        await togglePostLikes(user, setUser, song, song.id);
        setUser(JSON.parse(localStorage.getItem('user')));
    };

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

    let filteredSongs;

    if (filter === 'Liked' && genre === 'No genre') {
        filteredSongs = user.liked_songs;
    } else if (filter === 'Liked' && genre !== 'No genre') {
        filteredSongs = user.liked_songs.filter(song => song.main_artist.genres.some(g => g.name === genre));
    } else {
        filteredSongs = songs;
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
                    placeholder="Search for songs..." 
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
                        <Dropdown.Item eventKey='All'>All songs</Dropdown.Item>
                        <Dropdown.Item eventKey='Liked'>Liked songs</Dropdown.Item>
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
        {loading ? 'Loading...' : filteredSongs.length > 0 ? filteredSongs.map((song, index) => (
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
                    {!user.is_superuser && 
                        <Col md={4} className="song-info">
                        <div onClick={(event) => handleFavoriteClick(event, song.id)} className="heart-icon">
                            {user.liked_songs.map(song => song.id).includes(song.id) ? <HeartFill color="red" size={20} /> : <Heart color="black" size={20} />}
                        </div>
                        </Col>
                    }
                </Row>
            </Link>
        )) : <h2 style={{color: 'white'}}>No songs found</h2>}
        </Container>
        </UsersTemplate>
    );
}

export default UserSongs;

import React, { useState } from 'react';
import '../styles/Colors.css';
import '../styles/App.css';
import cd from '../media/cd.png';
import { useFetchTopPlaylists } from './useFetchData'; 
import { Container, Row, Col, Image } from 'react-bootstrap';
import CustomNavbar from './Navbar';

function TopHomepage({ websiteName }) {
    const [loading, setLoading] = useState(true);
    const songs = useFetchTopPlaylists('Top Global', websiteName, setLoading);

    return (
        <div className='App'>
            <CustomNavbar />
            <h1>Top Global {websiteName}</h1>
            <p className='white-text text-center ml-sm-2 mr-sm-2' style={{alignSelf: 'center', justifySelf: 'center', marginTop: '20px', marginLeft: '50px', marginRight:'50px'}}>If you want to see Top USA, Top Spain, Top Billboard and many more, go ahead and <a href='/signup' className='white-text'>sign up!</a></p>
            
            <Container className="top-info">
            {loading ? 'Loading...' : songs.map((song, index) => (
                <Row className="top-content">
                    <Col md={1} className="top-position">
                        <div>{song.position ? song.position.position : ''}</div>
                    </Col>
                    <Col md={4} className="top-image">
                        {song.song && song.song.images ? (
                            <Image src={song.song.images} onError={(e)=>{e.target.onerror = null; e.target.src=cd}} className='top-img' rounded />
                        ) : song.song && song.song.album && song.song.album.images ? (
                            <Image src={song.song.album.images} onError={(e)=>{e.target.onerror = null; e.target.src=cd}} className='top-img' rounded />
                        ) : song.song && song.song.album_images ? (
                            <Image src={song.song.album_images} onError={(e)=>{e.target.onerror = null; e.target.src=cd}} className='top-img' rounded />
                        ) : (
                            <div className="placeholder">
                                <Image src={cd} onError={(e)=>{e.target.onerror = null; e.target.src=cd}} className='top-img' rounded />
                            </div>
                        )}
                    </Col>
                    <Col md={4} className="text-center-md-down">
                        <div><strong>{song.song ? song.song.name : ''}</strong></div>
                        <div className="top-artist-name">{song.song && song.song.main_artist ? song.song.main_artist.name ? song.song.main_artist.name : song.song.main_artist : ''}</div>
                    </Col>
                </Row>
            ))}
            </Container>
        </div>
    );
}

export default TopHomepage;
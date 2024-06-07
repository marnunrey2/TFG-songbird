import React, { useState, useEffect } from 'react';
import UsersTemplate from '../../components/UsersTemplate';
import { useFetchGeneralData } from '../../components/useFetchData';
import '../../styles/Colors.css';
import '../../styles/UserStyles.css';
import cd from '../../media/cd.png';
import { Container, Row, Col, Image } from 'react-bootstrap';
import { Link, useParams } from 'react-router-dom';


function GeneralSearch() {
    const { searchTerm } = useParams(); 
    const [loading, setLoading] = useState(true);
    const results = useFetchGeneralData(searchTerm, setLoading);

    
    // Add this useEffect hook
    useEffect(() => {
        setLoading(true);
    }, [searchTerm]);

    return (
        <UsersTemplate>
            <h1>Search results for... {searchTerm}</h1>
            <Container className="info">
                {loading ? 'Loading...' : results.map(({type, data}, index) => {
                    const urlMap = {
                        song: '/song',
                        artist: '/artist',
                        album: '/album',
                        lyrics: '/song'
                    };
                    const url = `${urlMap[type]}/${data.id}`;
    
                    return (
                        <Link to={url} key={index} className="info-card-album">
                            <Row className="card-content">
                                <Col md={4} className="song-image">
                                    {data && data.images ? (
                                        <Image src={data.images} onError={(e) => { e.target.onerror = null; e.target.src = cd }} className="song-img" rounded />
                                    ) : data && data.album && data.album.images ? (
                                        <Image src={data.album.images} onError={(e) => { e.target.onerror = null; e.target.src = cd }} className="song-img" rounded />
                                    ) : data && data.album_images ? (
                                        <Image src={data.album_images} onError={(e) => { e.target.onerror = null; e.target.src = cd }} className="song-img" rounded />
                                    ) : (
                                        <div className="placeholder">
                                            <Image src={cd} onError={(e) => { e.target.onerror = null; e.target.src = cd }} className="song-img" rounded />
                                        </div>
                                    )}
                                </Col>
                                <Col md={4} className="song-info text-center-md-down">
                                    <div className="song-name">{data ? data.name : ''}</div>
                                    <div className="artist-name">Match with {type}</div>
                                </Col>
                            </Row>
                        </Link>
                    );
                })}
            </Container>
        </UsersTemplate>
    );
}

export default GeneralSearch;

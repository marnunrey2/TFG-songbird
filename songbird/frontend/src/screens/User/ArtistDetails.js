import React from 'react';
import UsersTemplate from '../../components/UsersTemplate';
import avatar from '../../media/avatar.png';
import { useParams } from 'react-router-dom';
import { Container, Row, Col, Image } from 'react-bootstrap';
import { useFetchArtistData } from '../../components/useFetchData';

function ArtistDetails() {
    const { name } = useParams(); 
    const { artist, albums, songs } = useFetchArtistData(name);

    if (!artist) {
        return <div>Loading...</div>;
    }

    return (
        <UsersTemplate>
        <Container className="info">
            <div className="details-card">
                <Row className="details-card-content">
                    <Col md={4} className="details-artist-image">
                        {artist && artist.images ? (
                            <Image src={artist.images} onError={(e)=>{e.target.onerror = null; e.target.src=avatar}} className="artist-img-details" rounded />
                        ) : (
                            <div className="placeholder">
                                <Image src={avatar} onError={(e)=>{e.target.onerror = null; e.target.src=avatar}} className="artist-img-details" rounded />
                            </div>
                        )}
                    </Col>
                    <Col md={4} className="artist-details">
                        <h2>{artist ? artist.name : ''}</h2>
                        <h6><strong>Genres: </strong>{artist && artist.genres ? artist.genres.join(', ') : ''}</h6>
                        <h6><strong>Followers: </strong>{artist && artist.followers ? JSON.stringify(artist.followers) : ''}</h6>
                    </Col>
                </Row>
                <Row className="details-card-content align-items-start" style={{ marginTop: '40px' }}>
                    <Col className='artist-details'>
                        <h3>Albums</h3>
                        {albums.map((album, i) => (
                            <div key={i}>{album.name}</div>
                        ))}
                    </Col>
                    <Col className='artist-details'>
                        <h3>Latest Songs</h3>
                        {songs.map((song, i) => (
                            <div key={i}>{song.name}</div>
                        ))}
                    </Col>
                </Row>
            </div>
        </Container>
        </UsersTemplate>
    );
}

export default ArtistDetails;
import React from 'react';
import UsersTemplate from '../../components/UsersTemplate';
import { useParams } from 'react-router-dom';
import { Container, Row, Col, Image } from 'react-bootstrap';
import { useFetchAlbumData } from '../../components/useFetchData';
import avatar from '../../media/avatar.png';

function AlbumDetails() {
    const { id } = useParams(); 
    const album = useFetchAlbumData(id);

    if (!album) {
        return <div>Loading...</div>;
    }

    return (
        <UsersTemplate>
        <Container className="info">
            <div className="details-card">
                <Row className="details-card-content">
                    <Col md={4} className="details-song-image">
                        {album && album.images ? (
                            <Image src={album.images} onError={(e)=>{e.target.onerror = null; e.target.src=avatar}} className="song-img-details" rounded />
                        ) : (
                            <div className="placeholder">
                                <Image src={avatar} onError={(e)=>{e.target.onerror = null; e.target.src=avatar}} className="song-img-details" rounded />
                            </div>
                        )}
                    </Col>
                    <Col md={4} className="song-details">
                        <h2>{album ? album.name : ''}</h2>
                        {album && album.genres.length > 0 ? <h6><strong>Genres: </strong>{album.genres.map( genre => genre.name).join(', ')}</h6> : <h6> </h6>}
                        <h6><strong>Release Date: </strong>{album ? album.release_date : ''}</h6>
                        <h6><strong>Total Tracks: </strong>{album ? album.total_tracks : ''}</h6>
                    </Col>
                </Row>
                <Row className="details-card-content align-items-start" style={{ marginTop: '40px' }}>
                    <Col className='song-details'>
                        <h3>Songs</h3>
                        <ul>
                            {album.songs.map((song, i) => (
                                <li key={i}>{song.name}</li>
                            ))}
                        </ul>
                    </Col>
                </Row>
            </div>
        </Container>
        </UsersTemplate>
    );
}

export default AlbumDetails;
import React from 'react';
import UsersTemplate from '../../components/UsersTemplate';
import avatar from '../../media/avatar.png';
import { useParams } from 'react-router-dom';
import { Container, Row, Col, Image } from 'react-bootstrap';
import { useFetchArtistData } from '../../components/useFetchData';
import { FaSpotify, FaYoutube, FaApple, FaDeezer } from 'react-icons/fa';

function ArtistDetails() {
    const { name } = useParams(); 
    const { artist, albums, songs } = useFetchArtistData(name);

    const renderAvailabilityIcons = () => {
        const icons = {
            'Spotify': <FaSpotify size={40} color="#1DB954" />,
            'YouTube': <FaYoutube size={40} color="#FF0000" />,
            'Apple Music': <FaApple size={40} color="#000000" />,
            'Deezer': <FaDeezer size={40} color="#00A4DC" />,
        };

        return Object.entries(artist.followers).map(([platform, count], i) => (
            <span key={i} style={{marginLeft: '50px', marginRight: '10px'}}>
                {icons[platform]} {count}
            </span>

        ));
    };

    if (!artist) {
        return <div>Loading...</div>;
    }

    return (
        <UsersTemplate>
        <Container className="info">
            <div className="details-card">
                <Row className="details-card-content">
                    <Col md={4} className="details-song-image">
                        {artist && artist.images ? (
                            <Image src={artist.images} onError={(e)=>{e.target.onerror = null; e.target.src=avatar}} className="song-img-details" rounded />
                        ) : (
                            <div className="placeholder">
                                <Image src={avatar} onError={(e)=>{e.target.onerror = null; e.target.src=avatar}} className="song-img-details" rounded />
                            </div>
                        )}
                    </Col>
                    <Col md={4} className="song-details">
                        <h2>{artist ? artist.name : ''}</h2>
                        <h6><strong>Genres: </strong>{artist && artist.genres ? artist.genres.map(genre => genre.name).join(', ') : ''}</h6>
                        
                        <h6><strong>Followers: </strong></h6>
                        <h6>{renderAvailabilityIcons()}</h6>
                    </Col>
                </Row>
                <Row className="details-card-content align-items-start" style={{ marginTop: '40px' }}>
                    <Col className='song-details'>
                        <h3>Albums</h3>
                        <ul>
                            {albums.map((album, i) => (
                                <li key={i}>{album.name}</li>
                            ))}
                        </ul>
                    </Col>
                    <Col className='song-details'>
                        <h3>Latest Songs</h3>
                        <ul>
                            {songs.slice(0, 5).map((song, i) => (
                                <li key={i}><strong>({song.release_date})</strong> {song.name}</li>
                            ))}
                        </ul>
                    </Col>
                </Row>
            </div>
        </Container>
        </UsersTemplate>
    );
}

export default ArtistDetails;
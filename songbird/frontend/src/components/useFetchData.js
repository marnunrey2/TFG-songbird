import { useState, useEffect } from 'react';
import axios from 'axios';


export function useFetchGeneralData(searchTerm, setLoading) {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get(`http://localhost:8000/api/search/?q=${encodeURIComponent(searchTerm)}`)
      .then(response => {
        setData(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching search:', error);
      });
  }, [searchTerm, setLoading]);

  return data;
};


export function useFetchSongs(searchTerm, genre, setLoading) {
    const [data, setData] = useState([]);
  
    useEffect(() => {
      let url;
      if (searchTerm) {
        url = `http://localhost:8000/api/songs-search/?q=${encodeURIComponent(searchTerm)}`;
        // Whoosh
        // url = `http://localhost:8000/api/song/search?search=${encodeURIComponent(searchTerm)}`;
      } else if (genre && genre !== 'No genre') {
        url = `http://localhost:8000/api/songs?genre=${genre}&limit=150`;
      } else {
        url = `http://localhost:8000/api/songs?limit=100`;
      }

      axios.get(url)
        .then(response => {
            setData(response.data);
            setLoading(false);
        })
        .catch(error => {
          console.error('Error fetching songs:',error);
        });
    }, [searchTerm, genre, setLoading]);
  
    return data;
}


export function useFetchSongData(songId) {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios.get(`http://localhost:8000/api/songs/${songId}`)
      .then(response => {
        setData(response.data);
      })
      .catch(error => {
        console.error('Error fetching song details:', error);
      });
  }, [songId]);

  return data;
};

export function useFetchArtists(searchTerm, genre, setLoading) {
    const [data, setData] = useState([]);
  
    useEffect(() => {
      let url;
      if (searchTerm) {
        url = `http://localhost:8000/api/artists-search/?q=${encodeURIComponent(searchTerm)}`;
      } else if (genre && genre !== 'No genre') {
        url = `http://localhost:8000/api/artists?genre=${genre}&limit=150`;
      } else {
        url = `http://localhost:8000/api/artists?limit=100`;
      }

      axios.get(url)
        .then(response => {
          setData(response.data);
          setLoading(false);
        })
        .catch(error => {
          console.error('Error fetching artists:',error);
        });
    }, [searchTerm, genre, setLoading]);
  
    return data;
}


export function useFetchArtistData(name) {
  const [artist, setArtist] = useState(null);
  const [albums, setAlbums] = useState([]);
  const [songs, setSongs] = useState([]);

  useEffect(() => {
      axios.get(`http://localhost:8000/api/artists/${name}`)
          .then(response => {
              setArtist(response.data);
          })
          .catch(error => {
            console.error('Error fetching artist details:',error);
          });

      axios.get(`http://localhost:8000/api/artists/${name}/albums`)
          .then(response => {
              setAlbums(response.data);
          })
          .catch(error => {
            console.error('Error fetching artist albums:',error);
          });

      axios.get(`http://localhost:8000/api/artists/${name}/songs`)
          .then(response => {
              setSongs(response.data);
          })
          .catch(error => {
            console.error('Error fetching artist songs:',error);
          });
  }, [name]);

  return { artist, albums, songs };
}

export function useFetchAlbums(searchTerm, genre, setLoading) {
    const [data, setData] = useState([]);
  
    useEffect(() => {
        let url;
        if (searchTerm) {
          url = `http://localhost:8000/api/albums-search/?q=${encodeURIComponent(searchTerm)}`;
        } else if (genre && genre !== 'No genre') {
          url = `http://localhost:8000/api/albums?genre=${genre}&limit=150`;
        } else {
          url = `http://localhost:8000/api/albums?limit=100`;
        }
  
        axios.get(url)
          .then(response => {
            setData(response.data);
            setLoading(false);
          })
          .catch(error => {
            console.error('Error fetching albums:',error);
          });
      }, [searchTerm, genre, setLoading]);
  
    return data;
}


export function useFetchAlbumData(albumId) {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios.get(`http://localhost:8000/api/albums/${albumId}`)
      .then(response => {
        setData(response.data);
      })
      .catch(error => {
        console.error('Error fetching album details:', error);
      });
  }, [albumId]);

  return data;
};

export function useFetchWebsiteNames(playlistName) {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get(`http://localhost:8000/api/website_names/${playlistName}/`)
      .then(response => {
        setData(response.data);
      })
      .catch(error => {
        console.error('Error fetching website names:', error);
      });
  }, [playlistName]);

  return data;
}

export function useFetchGenres() {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get(`http://localhost:8000/api/genres/`)
      .then(response => {
        setData(response.data);
      })
      .catch(error => {
        console.error('Error fetching genres:', error);
      });
  }, []);

  return data;
}

export function useFetchTopPlaylists(playlistName, websiteName, setLoading) {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get(`http://localhost:8000/api/playlist_songs/${playlistName}/${websiteName}/`)
      .then(response => {
        setData(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching playlist data:', error);
      });
  }, [playlistName, websiteName, setLoading]);

  return data;
}

export const togglePostLikes = async  (user, setUser, song, songId) => {
  const isSongLiked = user.liked_songs.map(s => s.id).includes(songId);

  let requestUrl = isSongLiked ? 'http://localhost:8000/api/user/unlike_song/' : 'http://localhost:8000/api/user/like_song/';
  
  try {
    await axios.post(requestUrl, { user_id: user.id, song_id: songId }, {
      headers: {
        'Content-Type': 'application/json',
      }
    });
    
    const updatedUser = { ...user };

    if (isSongLiked) {
      updatedUser.liked_songs = updatedUser.liked_songs.filter(s => s.id !== songId);
    } else {
      updatedUser.liked_songs.push(song);
    }

    setUser(updatedUser);
    localStorage.setItem('user', JSON.stringify(updatedUser));

  } catch (error) {
    console.error('Error toggling favorite song:', error);
  }
};

export function useFetchRecommendations(user_id, setLoading) {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get(`http://localhost:8000/api/recommendations/${user_id}/`)
        .then(response => {
            setData(response.data);
            setLoading(false);
        })
        .catch(error => {
            console.error("There was an error fetching the recommendations!", error);
        });
}, [user_id, setLoading]);

  return data;
};


export function useFetchAdminDashboard() {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get(`http://localhost:8000/api/admin/dashboard/`)
      .then(response => {
        setData(response.data);
      })
      .catch(error => {
        console.error('Error fetching admin dashboard:', error);
      });
  }, []);

  return data;
};

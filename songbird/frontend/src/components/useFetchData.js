import { useState, useEffect } from 'react';
import axios from 'axios';

export function useFetchSongs(searchTerm) {
    const [data, setData] = useState([]);
  
    useEffect(() => {
      // let url = `http://localhost:8000/api/songs?limit=50&ordering=-date_added`;
        let url = `http://localhost:8000/api/songs?limit=50`;
      if (searchTerm) {
        url = `http://localhost:8000/api/songs-search/?q=${encodeURIComponent(searchTerm)}`;
        // Whoosh
        // url = `http://localhost:8000/api/song/search?search=${encodeURIComponent(searchTerm)}`;
      }

      axios.get(url)
        .then(response => {
            if (searchTerm) {
              setData(response.data);
            } else {
              setData(response.data.results);
            }
        })
        .catch(error => {
          console.error(error);
        });
    }, [searchTerm]);
  
    return data;
}

export function useFetchArtists(searchTerm) {
    const [data, setData] = useState([]);
  
    useEffect(() => {
      let url = `http://localhost:8000/api/artists?limit=50&ordering=-followers`;
      if (searchTerm) {
        url = `http://localhost:8000/api/artists-search/?q=${encodeURIComponent(searchTerm)}`;
      }

      axios.get(url)
        .then(response => {
            if (searchTerm) {
                setData(response.data);
            } else {
                setData(response.data.results);
            }
        })
        .catch(error => {
          console.error(error);
        });
    }, [searchTerm]);
  
    return data;
}

export function useFetchAlbums(searchTerm) {
    const [data, setData] = useState([]);
  
    useEffect(() => {
        let url = `http://localhost:8000/api/albums?limit=50&ordering=-release_date`;
        if (searchTerm) {
          url = `http://localhost:8000/api/albums-search/?q=${encodeURIComponent(searchTerm)}`;
        }
  
        axios.get(url)
          .then(response => {
              if (searchTerm) {
                  setData(response.data);
              } else {
                  setData(response.data.results);
              }
          })
          .catch(error => {
            console.error(error);
          });
      }, [searchTerm]);
  
    return data;
}
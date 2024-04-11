import requests
from .models import (
    Song,
    Album,
    Artist,
    Genre,
)
from itertools import islice

song_ids = set()
album_ids = set()
artist_ids = set()


def chunks(data, SIZE=50):
    it = iter(data)
    for i in range(0, len(data), SIZE):
        if SIZE + i < len(data):
            yield set(islice(it, SIZE))
        else:
            yield set(islice(it, len(data) - i))


def spotify_api():
    client_id = "25c561e06c384a0c8a24901dc80f8114"
    client_secret = "f7e84ccb68384876a6b3264eb3d74d77"
    auth_url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }

    auth_response = requests.post(auth_url, data=data)
    access_token = auth_response.json().get("access_token")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Weekly Top Global
    playlist_id = "37i9dQZEVXbNG2KDcFcKOF"
    get_playlist_spotify(playlist_id, headers)

    # Weekly Top Spain
    playlist_id = "37i9dQZEVXbJwoKy8qKpHG"
    get_playlist_spotify(playlist_id, headers)


def get_playlist_spotify(playlist_id, headers):
    global song_ids, album_ids, artist_ids

    # Endpoint to make the request
    endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

    # Make the GET request to Spotify API
    response = requests.get(endpoint, headers=headers)

    # added_at, added_by, is_local, primary_color, track, video_thumbnail
    items = response.json()["items"]

    for item in items:
        song_info = item["track"]

        # Add the song, album, and artist IDs to the sets
        song_ids.add(song_info["id"])
        album_ids.add(song_info["album"]["id"])
        artist_ids.update(art["id"] for art in song_info["artists"])

    # Fetch the songs, albums, and artists
    while song_ids or album_ids or artist_ids:
        if artist_ids:
            get_multiple_artists_spotify(artist_ids.copy(), headers)
            artist_ids.clear()
        if album_ids:
            get_multiple_albums_spotify(album_ids.copy(), headers)
            album_ids.clear()
        if song_ids:
            get_multiple_songs_spotify(song_ids.copy(), headers)
            song_ids.clear()


def get_multiple_artists_spotify(artist_ids, headers):

    for chunk in chunks(artist_ids):
        # Make the GET request to Spotify API
        endpoint = f"https://api.spotify.com/v1/artists/?ids={','.join(chunk)}"
        response = requests.get(endpoint, headers=headers)
        artists_info = response.json()["artists"]
        for artist_info in artists_info:

            # Extract the artist information
            artist_name = artist_info["name"]
            artist_genres = artist_info["genres"]
            artist_followers = artist_info["followers"]["total"]
            artist_images = (
                artist_info["images"][0]["url"] if artist_info["images"] else None
            )
            artist_popularity = artist_info["popularity"]
            artist_href = artist_info["href"]

            # Get or create the artist
            artist, created = Artist.objects.get_or_create(
                id=artist_info["id"],
                defaults={
                    "name": artist_name,
                    "followers": artist_followers,
                    "images": artist_images,
                    "popularity": artist_popularity,
                    "href": artist_href,
                },
            )

            # Get or create the genres and add them to the artist
            for genre_name in artist_genres:
                genre, created = Genre.objects.get_or_create(name=genre_name)
                artist.genres.add(genre)


def get_multiple_albums_spotify(album_ids, headers):
    global artist_ids, song_ids

    for chunk in chunks(album_ids, 20):
        # Make the GET request to Spotify API
        endpoint = f"https://api.spotify.com/v1/albums/?ids={','.join(chunk)}"
        response = requests.get(endpoint, headers=headers)
        albums_info = response.json()["albums"]
        for album_info in albums_info:

            # Extract the album information
            album_name = album_info["name"]
            album_genre = album_info["genres"]
            album_images = album_info["images"][0]["url"]
            album_popularity = album_info["popularity"]
            album_release_date = album_info["release_date"]
            album_total_tracks = album_info["total_tracks"]
            album_href = album_info["href"]

            # Get or create the album
            album, created = Album.objects.get_or_create(
                id=album_info["id"],
                defaults={
                    "name": album_name,
                    "images": album_images,
                    "popularity": album_popularity,
                    "release_date": album_release_date,
                    "total_tracks": album_total_tracks,
                    "href": album_href,
                },
            )

            # Get or create the genres and add them to the album
            for genre_name in album_genre:
                genre, created = Genre.objects.get_or_create(name=genre_name)
                album.genre.add(genre)

            # Get the songs and artists for the album
            new_song_ids = {
                song["id"]
                for song in album_info["tracks"]["items"]
                if not Song.objects.filter(id=song["id"]).exists()
            }
            new_artist_ids = {
                art["id"]
                for art in album_info["artists"]
                if not Artist.objects.filter(id=art["id"]).exists()
            }

            song_ids.update(new_song_ids)
            artist_ids.update(new_artist_ids)

            # Add the songs and artists to the album
            artists = Artist.objects.filter(id__in=artist_ids)
            album.artists.set(artists)
            album.save()


def get_multiple_songs_spotify(song_ids, headers):
    global album_ids, artist_ids

    for chunk in chunks(song_ids):
        # Make the GET request to Spotify API
        endpoint = f"https://api.spotify.com/v1/tracks/?ids={','.join(chunk)}"
        response = requests.get(endpoint, headers=headers)
        songs_info = response.json()["tracks"]
        for song_info in songs_info:

            # Extract the song information
            song_name = song_info["name"]
            song_duration = song_info["duration_ms"]
            song_explicit = song_info["explicit"]
            song_popularity = song_info["popularity"]
            song_href = song_info["href"]

            # Get or create the song
            song, created = Song.objects.get_or_create(
                id=song_info["id"],
                defaults={
                    "name": song_name,
                    "duration": song_duration,
                    "explicit": song_explicit,
                    "popularity": song_popularity,
                    "href": song_href,
                },
            )

            # Get the album and artists for the song
            new_album_id = (
                song_info["album"]["id"]
                if not Album.objects.filter(id=song_info["album"]["id"]).exists()
                else None
            )
            new_artist_ids = {
                art["id"]
                for art in song_info["artists"]
                if not Artist.objects.filter(id=art["id"]).exists()
            }

            if new_album_id:
                album_ids.add(new_album_id)
            artist_ids.update(new_artist_ids)

            # Get the album and artists for the song
            album = Album.objects.get(id=song_info["album"]["id"])
            artists_ids = [art["id"] for art in song_info["artists"]]
            artists = Artist.objects.filter(id__in=artists_ids)

            # Add the album and artists to the song
            song.album = album
            song.artists.set(artists)
            song.save()

import requests
from .models import (
    Song,
    Album,
    Artist,
    Genre,
)


def get_playlist_spotify(playlist_id, headers):
    # Endpoint to make the request
    endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

    # Make the GET request to Spotify API
    response = requests.get(endpoint, headers=headers)

    # added_at, added_by, is_local, primary_color, track, video_thumbnail
    items = response.json()["items"]

    for item in items:
        song_info = item["track"]

        # Save the song, album, and artists to the database
        song = get_songs_spotify(song_info["href"], headers)
        album = get_albums_spotify(song_info["album"]["href"], headers)
        artists = [
            get_artists_spotify(art["href"], headers) for art in song_info["artists"]
        ]

        # Add the artists to the song and album
        song.artists.set(artists)
        album.artists.set(artists)

    return None  # No need to return anything as we're saving to the database


def get_songs_spotify(song_href, headers):
    # Make the GET request to Spotify API
    response = requests.get(song_href, headers=headers)

    # Check if the response is empty
    if not response.text:
        print(f"No response for song: {song_href}")
        return None

    song_info = response.json()

    # Extract the song information
    song_name = song_info["name"]
    song_duration = song_info["duration_ms"]
    song_explicit = song_info["explicit"]
    song_popularity = song_info["popularity"]

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
    album = get_albums_spotify(song_info["album"]["href"], headers)
    artists = [
        get_artists_spotify(art["href"], headers) for art in song_info["artists"]
    ]

    # Add the album and artists to the song
    song.album = album
    song.artists.set(artists)
    song.save()

    return song


def get_albums_spotify(album_href, headers):
    # Make the GET request to Spotify API
    response = requests.get(album_href, headers=headers)

    # Check if the response is empty
    if not response.text:
        print(f"No response for song: {album_href}")
        return None

    album_info = response.json()

    # Extract the album information
    album_name = album_info["name"]
    album_genre = album_info["genres"]
    album_images = album_info["images"][0]["url"]
    album_popularity = album_info["popularity"]
    album_release_date = album_info["release_date"]
    album_total_tracks = album_info["total_tracks"]

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
    for song in album_info["tracks"]["items"]:
        # Check if the song already exists in the database
        if not Song.objects.filter(id=song["id"]).exists():
            get_songs_spotify(song["href"], headers)
    artists = [
        get_artists_spotify(art["href"], headers) for art in album_info["artists"]
    ]

    # Add the songs and artists to the album
    album.artists.set(artists)
    album.save()

    return album


def get_artists_spotify(artist_href, headers):
    # Make the GET request to Spotify API
    response = requests.get(artist_href, headers=headers)

    # Check if the response is empty
    if not response.text:
        print(f"No response for artist: {artist_href}")
        return None

    artist_info = response.json()

    # Extract the artist information
    artist_name = artist_info["name"]
    artist_genres = artist_info["genres"]
    artist_followers = artist_info["followers"]["total"]
    artist_images = artist_info["images"][0]["url"]
    artist_popularity = artist_info["popularity"]

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

    return artist


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

    """
    # Weekly Top Spain
    playlist_id = "37i9dQZEVXbJwoKy8qKpHG"
    get_playlist_spotify(playlist_id, headers)
    """


""" MAKING LESS REQUESTS (NOT SURE IF WORKS)

def get_playlist_spotify(playlist_id, headers):
    # Endpoint to make the request
    endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

    # Make the GET request to Spotify API
    response = requests.get(endpoint, headers=headers)

    # added_at, added_by, is_local, primary_color, track, video_thumbnail
    items = response.json()["items"]

    # Get all song ids, album ids and artist ids
    song_ids = [item["track"]["id"] for item in items]
    album_ids = [item["track"]["album"]["id"] for item in items]
    artist_ids = [artist["id"] for item in items for artist in item["track"]["artists"]]

    # Get all songs, albums and artists in a single request
    songs = get_songs_spotify(song_ids, headers)
    albums = get_albums_spotify(album_ids, headers)
    artists = get_artists_spotify(artist_ids, headers)

    for i, item in enumerate(items):
        song_info = item["track"]

        # Get the song, album and artists from the lists
        song = songs[i]
        album = albums[i]
        song_artists = [artist for artist in artists if artist["id"] in [a["id"] for a in song_info["artists"]]]

        # Add the artists to the song and album
        song.artists.set(song_artists)
        album.artists.set(song_artists)

    return None  # No need to return anything as we're saving to the database
    
def get_songs_spotify(song_ids, headers):
    # Make the GET request to Spotify API
    endpoint = f"https://api.spotify.com/v1/tracks?ids={','.join(song_ids)}"
    response = requests.get(endpoint, headers=headers)

    songs_info = response.json()["tracks"]

    songs = []
    for song_info in songs_info:
        # Extract the song information
        song_name = song_info["name"]
        song_duration = song_info["duration_ms"]
        song_explicit = song_info["explicit"]
        song_popularity = song_info["popularity"]

        # Get or create the song
        song, created = Song.objects.get_or_create(
            id=song_info["id"],
            defaults={
                "name": song_name,
                "duration": song_duration,
                "explicit": song_explicit,
                "popularity": song_popularity,
            },
        )

        songs.append(song)

    return songs

def get_albums_spotify(album_ids, headers):
    # Make the GET request to Spotify API
    endpoint = f"https://api.spotify.com/v1/albums?ids={','.join(album_ids)}"
    response = requests.get(endpoint, headers=headers)

    albums_info = response.json()["albums"]

    albums = []
    for album_info in albums_info:
        # Extract the album information
        album_name = album_info["name"]
        album_genre = album_info["genres"]
        album_images = album_info["images"][0]["url"]
        album_popularity = album_info["popularity"]
        album_release_date = album_info["release_date"]
        album_total_tracks = album_info["total_tracks"]

        # Get or create the album
        album, created = Album.objects.get_or_create(
            id=album_info["id"],
            defaults={
                "name": album_name,
                "images": album_images,
                "popularity": album_popularity,
                "release_date": album_release_date,
                "total_tracks": album_total_tracks,
            },
        )

        # Get or create the genres and add them to the album
        for genre_name in album_genre:
            genre, created = Genre.objects.get_or_create(name=genre_name)
            album.genre.add(genre)

        albums.append(album)

    return albums

def get_artists_spotify(artist_ids, headers):
    # Make the GET request to Spotify API
    endpoint = f"https://api.spotify.com/v1/artists?ids={','.join(artist_ids)}"
    response = requests.get(endpoint, headers=headers)

    artists_info = response.json()["artists"]

    artists = []
    for artist_info in artists_info:
        # Extract the artist information
        artist_name = artist_info["name"]
        artist_genres = artist_info["genres"]
        artist_followers = artist_info["followers"]["total"]
        artist_images = artist_info["images"][0]["url"]
        artist_popularity = artist_info["popularity"]

        # Get or create the artist
        artist, created = Artist.objects.get_or_create(
            id=artist_info["id"],
            defaults={
                "name": artist_name,
                "followers": artist_followers,
                "images": artist_images,
                "popularity": artist_popularity,
                "href": artist_info["href"],
            },
        )

        # Get or create the genres and add them to the artist
        for genre_name in artist_genres:
            genre, created = Genre.objects.get_or_create(name=genre_name)
            artist.genres.add(genre)

        artists.append(artist)

    return artists
"""

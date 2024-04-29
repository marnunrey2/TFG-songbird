import requests
from .models import (
    Song,
    Album,
    Artist,
    Genre,
    Website,
    Playlist,
    PlaylistSong,
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

    # Define the playlists
    playlists = {
        "Weekly Top Global": "37i9dQZEVXbNG2KDcFcKOF",
        "Weekly Top Spain": "37i9dQZEVXbJwoKy8qKpHG",
        "Weekly Top USA": "37i9dQZEVXbLp5XoPON0wI",
        "Weekly Top France": "37i9dQZEVXbKQ1ogMOyW9N",
        "Weekly Top Colombia": "37i9dQZEVXbL1Fl8vdBUba",
        "Weekly Top Argentina": "37i9dQZEVXbKPTKrnFPD0G",
        "Weekly Top Germany": "37i9dQZEVXbK8BKKMArIyl",
        "Weekly Top India": "37i9dQZEVXbMWDif5SCBJq",
        "Weekly Top Italy": "37i9dQZEVXbJUPkgaWZcWG",
        "Weekly Top Japan": "37i9dQZEVXbKqiTGXuCOsB",
        "Weekly Top South Korea": "37i9dQZEVXbJZGli0rRP3r",
        "Weekly Top UK": "37i9dQZEVXbMwmF30ppw50",
    }

    # Fetch the songs, albums, and artists from all the playlists
    for playlist_name, playlist_id in playlists.items():
        get_playlist_spotify(playlist_name, playlist_id, headers)


def get_playlist_spotify(playlist_name, playlist_id, headers):
    global song_ids, album_ids, artist_ids

    # Endpoint to make the request
    endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

    # Make the GET request to Spotify API
    response = requests.get(endpoint, headers=headers)

    # added_at, added_by, is_local, primary_color, track, video_thumbnail
    items = response.json()["items"]

    # Create a Website and Playlist instance
    website, _ = Website.objects.get_or_create(name="Spotify")
    playlist, _ = Playlist.objects.get_or_create(name=playlist_name, website=website)

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

    for index, item in enumerate(items):
        song_info = item["track"]

        # Get the song, album, and artist
        main_artist = Artist.objects.get(name=song_info["artists"][0]["name"])
        song = Song.objects.get(name=song_info["name"], main_artist=main_artist)

        print(playlist, index + 1, song, main_artist)
        # Create or update a PlaylistSong instance
        playlist_song, created = PlaylistSong.objects.update_or_create(
            song=song, playlist=playlist, defaults={"position": index + 1}
        )


def get_multiple_artists_spotify(artist_ids, headers):

    for chunk in chunks(artist_ids):
        # Make the GET request to Spotify API
        endpoint = f"https://api.spotify.com/v1/artists/?ids={','.join(chunk)}"
        response = requests.get(endpoint, headers=headers)
        artists_info = response.json()["artists"]
        for artist_info in artists_info:

            # Extract the artist information
            artist_name = artist_info["name"]
            artist_followers = artist_info["followers"]["total"]
            artist_images = (
                artist_info["images"][0]["url"] if artist_info["images"] else None
            )
            artist_popularity = artist_info["popularity"]
            artist_href = artist_info["href"]

            # Get or create the artist
            artist, created = Artist.objects.get_or_create(
                name=artist_name,
                defaults={
                    "followers": artist_followers,
                    "images": artist_images,
                    "popularity": artist_popularity,
                    "href": artist_href,
                },
            )

            # Get or create the genres and add them to the artist
            for genre_name in artist_info["genres"]:
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
            album_images = album_info["images"][0]["url"]
            album_popularity = album_info["popularity"]
            album_release_date = album_info["release_date"]
            album_total_tracks = album_info["total_tracks"]
            album_href = album_info["href"]

            artist_name = album_info["artists"][0]["name"]
            artist, created = Artist.objects.get_or_create(name=artist_name)

            # If the artist was created, add its id to artists_id
            if created:
                artist_ids.add(album_info["artists"][0]["id"])

            # Get or create the album
            album, created = Album.objects.get_or_create(
                name=album_name,
                artist=artist,
                defaults={
                    "images": album_images,
                    "popularity": album_popularity,
                    "release_date": album_release_date,
                    "total_tracks": album_total_tracks,
                    "href": album_href,
                },
            )

            # Get or create the genres and add them to the album
            for genre_name in album_info["genres"]:
                genre, created = Genre.objects.get_or_create(name=genre_name)
                album.genre.add(genre)

            # Get the songs and artists for the album
            new_song_ids = {
                song["id"]
                for song in album_info["tracks"]["items"]
                if not Song.objects.filter(name=song["name"]).exists()
            }

            song_ids.update(new_song_ids)

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

            # Get/create the artist
            main_artist, created = Artist.objects.get_or_create(
                name=song_info["artists"][0]["name"]
            )

            # Get or create the song
            song, created = Song.objects.get_or_create(
                name=song_name,
                main_artist=main_artist,
                defaults={
                    "duration": song_duration,
                    "explicit": song_explicit,
                    "popularity": song_popularity,
                    "href": song_href,
                },
            )

            # Add the album and collaborators to the song
            if len(song_info["artists"]) > 1:
                for artist_info in song_info["artists"][1:]:
                    artist, created = Artist.objects.get_or_create(
                        name=artist_info["name"]
                    )
                    song.collaborators.add(artist)

            # Get/create the album
            album_name = song_info["album"]["name"]
            album_artist = song_info["album"]["artists"][0]["name"]
            album, created = Album.objects.get_or_create(
                name=album_name, artist__name=album_artist
            )

            if created:
                album_ids.append(song_info["album"]["id"])

            song.album = album
            song.save()

            new_artist_ids = {
                art["id"]
                for art in song_info["artists"]
                if not Artist.objects.filter(name=art["name"]).exists()
            }

            artist_ids.update(new_artist_ids)

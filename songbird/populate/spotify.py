from dotenv import load_dotenv
import os
import requests
from .models import (
    Song,
    Album,
    Artist,
    Genre,
    Website,
    Playlist,
    PlaylistSong,
    Position,
)
from itertools import islice
from datetime import datetime

song_ids = set()
album_ids = set()
artist_ids = set()
playlist_ids = {}

top_playlists = {
    "Top Global": "37i9dQZEVXbNG2KDcFcKOF",
    "Top Spain": "37i9dQZEVXbJwoKy8qKpHG",
    "Top USA": "37i9dQZEVXbLp5XoPON0wI",
    "Top UK": "37i9dQZEVXbMwmF30ppw50",
    "Top Canada": "37i9dQZEVXbMda2apknTqH",
    "Top South Korea": "37i9dQZEVXbJZGli0rRP3r",
    "Top France": "37i9dQZEVXbKQ1ogMOyW9N",
    "Top Germany": "37i9dQZEVXbK8BKKMArIyl",
    "Top Australia": "37i9dQZEVXbK4fwx2r07XW",
    "Top Colombia": "37i9dQZEVXbL1Fl8vdBUba",
    "Top Argentina": "37i9dQZEVXbKPTKrnFPD0G",
    "Top Italy": "37i9dQZEVXbJUPkgaWZcWG",
    "Top Japan": "37i9dQZEVXbKqiTGXuCOsB",
}

genre_playlists = {
    "Latina": ["37i9dQZF1DX10zKzsJ2jva"],
    "Reggaeton": ["37i9dQZF1DWY7IeIP1cdjF"],
    "Pop": [
        "37i9dQZF1DWUa8ZRTfalHk",
        "37i9dQZF1DXcBWIGoYBM5M",
        "37i9dQZF1DX3sCT1ItXgNd",
        "37i9dQZF1DWSpF87bP6JSF",
    ],
    "Rock": ["37i9dQZF1DWZryfp6NSvtz", "37i9dQZF1DX1MT1Ubz4wvO"],
    "Metal": ["37i9dQZF1DX5J7FIl4q56G"],
    "Hip hop": ["37i9dQZF1DX2sQHbtx0sdt"],
    "Flamenco": ["37i9dQZF1DWYJd705x6Zbc"],
    "Dance": ["37i9dQZF1DX0BcQWzuB7ZO"],
    "Indie": ["37i9dQZF1DXdbXrPNafg9d"],
    "R&B": ["37i9dQZF1DWUzFXarNiofw"],
    "K-pop": ["37i9dQZF1DXe5W6diBL5N4"],
    "Jazz": ["37i9dQZF1DX7YCknf2jT6s"],
    "Clasica": ["37i9dQZF1DWV0gynK7G6pD"],
    "Folk": ["37i9dQZF1DWYV7OOaGhoH0"],
    "Soul": ["37i9dQZF1DWSXWSaQmvWOB"],
    "Reggae": ["37i9dQZF1DXbSbnqxMTGx9"],
    "Instrumental": ["37i9dQZF1DXaImRpG7HXqp"],
    "Punk": ["37i9dQZF1DX0KpeLFwA3tO"],
    "Blues": ["37i9dQZF1DX0QNpebF7rcL"],
    "Alternativa": ["37i9dQZF1DX9GRpeH4CL0S"],
    "Afro": ["37i9dQZF1DWT6SJaitNDax"],
    "Funk": ["37i9dQZF1DX70TzPK5buVf"],
    "Cumbia": ["37i9dQZF1DWT1viuVscXm2"],
    "Salsa": ["37i9dQZF1DX1UHxedJfnRM"],
    "Country": ["37i9dQZF1DX7hnECllVaUq"],
}


def chunks(data, SIZE=50):
    it = iter(data)
    for i in range(0, len(data), SIZE):
        if SIZE + i < len(data):
            yield set(islice(it, SIZE))
        else:
            yield set(islice(it, len(data) - i))


def get_token():
    # Load the .env file
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

    # Get the access token
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
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
    return headers


def spotify_api():
    global song_ids, album_ids, artist_ids, playlist_ids, top_playlists, genre_playlists

    print("Spotify API: getting IDs...")

    headers = get_token()

    # Fetch the songs, albums, and artists from all the playlists
    for playlist_name, playlist_id in top_playlists.items():
        get_playlist_spotify(
            playlist_name, playlist_id, top_playlist=True, headers=headers
        )

    # Fetch the songs, albums, and artists from all the playlists
    for playlist_name, playlists_ids in genre_playlists.items():
        for playlist_id in playlists_ids:
            get_playlist_spotify(
                playlist_name, playlist_id, top_playlist=False, headers=headers
            )

    print("Spotify API: IDs done, getting data ...")

    headers = get_token()

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

    print("Spotify API: data done, creating playlists ...")

    # Create a Website and Playlist instance
    website, _ = Website.objects.get_or_create(name="Spotify")
    for playlist_name, items in playlist_ids.items():
        playlist, _ = Playlist.objects.get_or_create(
            name=playlist_name, website=website
        )

        for index, item in enumerate(items):
            song_name, artist_name = item
            main_artist = Artist.objects.get(name=artist_name)
            song = Song.objects.get(name=song_name, main_artist=main_artist)
            position, _ = Position.objects.get_or_create(position=index + 1)

            # Create or update a PlaylistSong instance
            PlaylistSong.objects.update_or_create(
                song=song, playlist=playlist, position=position
            )


def get_playlist_spotify(playlist_name, playlist_id, top_playlist, headers):
    global song_ids, album_ids, artist_ids, playlist_ids

    # Endpoint to make the request
    endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

    # Make the GET request to Spotify API
    response = requests.get(endpoint, headers=headers)

    # added_at, added_by, is_local, primary_color, track, video_thumbnail
    try:
        items = response.json()["items"]
    except:
        print(playlist_name, playlist_id)
        print(response.json())
        return

    for item in items:
        song_info = item["track"]

        # Add the song, album, and artist IDs to the sets
        if song_info is not None:
            song_ids.add(song_info["id"])
            album_ids.add(song_info["album"]["id"])
            artist_ids.update(art["id"] for art in song_info["artists"])
            if top_playlist:
                if playlist_ids.get(playlist_name) is None:
                    playlist_ids[playlist_name] = [
                        (song_info["name"], song_info["artists"][0]["name"])
                    ]
                else:
                    playlist_ids[playlist_name].append(
                        (song_info["name"], song_info["artists"][0]["name"])
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
            # artist_popularity = artist_info["popularity"]
            # artist_href = artist_info["href"]

            # Update or create the artist
            artist, created = Artist.objects.update_or_create(
                name=artist_name,
                defaults={
                    "images": artist_images,
                },
            )
            artist.followers["Spotify"] = artist_followers

            # Get or create the genres and add them to the artist
            for genre_name in artist_info["genres"]:
                for g in Genre.BASE_GENRES:
                    if g in genre_name.upper():
                        genre, created = Genre.objects.get_or_create(name=g)
                        artist.genres.add(genre)
                        artist.save()

            artist.save()


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
            # album_popularity = album_info["popularity"]
            album_release_date_str = album_info["release_date"]
            if len(album_release_date_str) == 4:  # 'YYYY' format
                album_release_date = datetime.strptime(
                    album_release_date_str, "%Y"
                ).date()
            elif len(album_release_date_str) == 7:  # 'YYYY-MM' format
                album_release_date = datetime.strptime(
                    album_release_date_str, "%Y-%m"
                ).date()
            else:  # 'YYYY-MM-DD' format
                album_release_date = datetime.strptime(
                    album_release_date_str, "%Y-%m-%d"
                ).date()

            album_total_tracks = album_info["total_tracks"]
            # album_href = album_info["href"]

            artist_name = album_info["artists"][0]["name"]
            artist, created = Artist.objects.get_or_create(name=artist_name)

            # If the artist was created, add its id to artists_id
            if created:
                artist_ids.add(album_info["artists"][0]["id"])

            # Update or create the album
            album, created = Album.objects.update_or_create(
                name=album_name,
                artist=artist,
                defaults={
                    "images": album_images,
                    "release_date": album_release_date,
                    "total_tracks": album_total_tracks,
                },
            )

            # Get or create the genres and add them to the album
            for genre_name in album_info["genres"]:
                for g in Genre.BASE_GENRES:
                    if g in genre_name.upper():
                        genre, created = Genre.objects.get_or_create(name=g)
                        album.genres.add(genre)

            album.save()

            # Get the songs and artists for the album
            new_song_ids = {
                song["id"]
                for song in album_info["tracks"]["items"]
                if not Song.objects.filter(name=song["name"]).exists()
            }
            song_ids.update(new_song_ids)


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
            song_duration = song_info["duration_ms"] // 1000  # Convert to seconds
            song_explicit = song_info["explicit"]
            song_release_date_str = song_info["album"]["release_date"]
            if len(song_release_date_str) == 4:  # 'YYYY' format
                song_release_date = datetime.strptime(
                    song_release_date_str, "%Y"
                ).date()
            elif len(song_release_date_str) == 7:  # 'YYYY-MM' format
                song_release_date = datetime.strptime(
                    song_release_date_str, "%Y-%m"
                ).date()
            else:  # 'YYYY-MM-DD' format
                song_release_date = datetime.strptime(
                    song_release_date_str, "%Y-%m-%d"
                ).date()

            # song_popularity = song_info["popularity"]
            # song_href = song_info["href"]

            # Get/create the artist
            main_artist, created = Artist.objects.get_or_create(
                name=song_info["artists"][0]["name"]
            )

            # Update or create the song
            song, created = Song.objects.update_or_create(
                name=song_name,
                main_artist=main_artist,
                defaults={
                    "duration": song_duration,
                    "explicit": song_explicit,
                    "release_date": song_release_date,
                },
            )
            song.available_at.append("Spotify")

            # Add the album and collaborators to the song
            if len(song_info["artists"]) > 1:
                for artist_info in song_info["artists"][1:]:
                    artist, created = Artist.objects.get_or_create(
                        name=artist_info["name"]
                    )
                    song.collaborators.add(artist)
                    song.save()

            # Get/create the album
            album_name = song_info["album"]["name"]
            album_artist = song_info["album"]["artists"][0]["name"]
            album, created = Album.objects.get_or_create(
                name=album_name, artist__name=album_artist
            )
            song.album = album
            song.save()

            # if created:
            #     album_ids.add(song_info["album"]["id"])

            new_artist_ids = {
                art["id"]
                for art in song_info["artists"]
                if not Artist.objects.filter(name=art["name"]).exists()
            }

            artist_ids.update(new_artist_ids)

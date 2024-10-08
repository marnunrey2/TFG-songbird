import requests
from populate.models import (
    Playlist,
    Song,
    Artist,
    Album,
    Website,
    Position,
    PlaylistSong,
)
import time
from datetime import datetime
from itertools import islice


songs_ids = set()
albums_ids = set()
artists_ids = set()


def chunks(data, SIZE=25):
    it = iter(data)
    for i in range(0, len(data), SIZE):
        if SIZE + i < len(data):
            yield set(islice(it, SIZE))
        else:
            yield set(islice(it, len(data) - i))


def amazon_music_api():

    Website.objects.get_or_create(name="Amazon Music")

    # Access token (expires in 1 hour)
    access_token = input("Please enter a new access token: ")

    # Security Id
    profile_id = "Amazon profile id"

    # Top 50 Most played: International -> B07QHGBGC9
    playlist_id = "B0794G8R8W"
    get_playlist_songs(playlist_id, access_token, profile_id)

    # Today Hits: Spain -> B073PW84YH
    playlist_id = "B073PW84YH"
    get_playlist_songs(playlist_id, access_token, profile_id)


def get_playlist_songs(playlist_id, access_token, profile_id):
    global songs_ids, albums_ids, artists_ids

    url = f"https://api.music.amazon.dev/v1/playlists/{playlist_id}/tracks"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "x-api-key": profile_id,
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)

    # Check the response status code
    if response.status_code == 429:  # "Too Many Requests"
        access_token = input("Please enter a new access token: ")

        # Retry the request with the next token
        headers["Authorization"] = f"Bearer {access_token}"
        response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(response.json())
        return

    playlist_name = response.json()["data"]["playlist"]["title"]
    tracks = response.json()["data"]["playlist"]["tracks"]["edges"]

    for track in tracks:

        # POSITION
        position = int(track["cursor"].split(":")[0]) + 1

        track_info = track["node"]

        # Add the song, album, and artist IDs to the sets
        songs_ids.add((playlist_name, position, track_info["id"]))
        albums_ids.add(track_info["album"]["id"])
        artists_ids.update(art["id"] for art in track_info["artists"])

    # Fetch the songs, albums, and artists
    while songs_ids or albums_ids or artists_ids:
        if artists_ids:
            get_multiple_artists_amazon(artists_ids.copy())
            artists_ids.clear()
        if albums_ids:
            get_multiple_albums_amazon(albums_ids.copy())
            albums_ids.clear()
        if songs_ids:
            get_multiple_songs_amazon(songs_ids.copy())
            songs_ids.clear()


def get_multiple_artists_amazon(artist_ids, access_token, profile_id):

    for chunk in chunks(artist_ids):

        url = f"https://api.music.amazon.dev/v1/artists/?ids={','.join(chunk)}"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "x-api-key": profile_id,
            "Content-Type": "application/json",
        }

        response = requests.get(url, headers=headers)

        # Check the response status code
        if response.status_code == 429:  # "Too Many Requests"
            access_token = input("Please enter a new access token: ")

            # Retry the request with the next token
            headers["Authorization"] = f"Bearer {access_token}"
            response = requests.get(url, headers=headers)

        # if response.status_code != 200:
        #     print(response.json())
        #     return

        artists_info = response.json()["data"]["artist"]

        for artist_info in artists_info:

            # Extract the artist information
            name = artist_info["name"]
            image_url = artist_info["images"][0]["url"]

            # Get/create the artist
            artist, created = Artist.objects.get_or_create(name=name)

            # If the artist was created or if it exists and images is None, update the images field
            if created or (artist.images is None and image_url is not None):
                artist.images = image_url
                artist.save()

        time.sleep(1.5)  # pauses for 1 second


def get_multiple_albums_amazon(album_ids, access_token, profile_id):
    global artists_ids, songs_ids

    for chunk in chunks(album_ids):

        url = f"https://api.music.amazon.dev/v1/albums/?ids={','.join(chunk)}"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "x-api-key": profile_id,
            "Content-Type": "application/json",
        }

        response = requests.get(url, headers=headers)

        # Check the response status code
        if response.status_code == 429:  # "Too Many Requests"
            access_token = input("Please enter a new access token: ")

            # Retry the request with the next token
            headers["Authorization"] = f"Bearer {access_token}"
            response = requests.get(url, headers=headers)

        # if response.status_code != 200:
        #     print(response.json())
        #     return

        albums_info = response.json()["data"]["album"]

        for album_info in albums_info:

            # Extract the album information
            name = album_info["title"]
            release_date = album_info["releaseDate"]
            release_date = datetime.strptime(
                release_date, "%Y-%m-%dT%H:%M:%S.%fZ"
            ).strftime("%Y-%m-%d")
            image_url = album_info["images"][0]["url"]

            # Get/create the artist
            artist_name = album_info["artists"][0]["name"]
            artist, created = Artist.objects.get_or_create(name=artist_name)

            # If the artist was created, add its id to artists_id
            if created:
                artists_ids.add(album_info["artists"][0]["id"])

            # Get/create the album
            album, created = Album.objects.get_or_create(name=name, artist=artist)

            # If the album was created or if it exists and a field is None, update the field
            if created or (album.images is None and image_url is not None):
                album.images = image_url
            if created or (album.release_date is None and release_date is not None):
                album.release_date = release_date

            album.save()

            # Get the songs and artists for the album
            new_song_ids = {
                song["id"]
                for song in album_info["tracks"]
                if not Song.objects.filter(name=song["title"]).exists()
            }

            songs_ids.update((None, None, new_song_ids))

        time.sleep(1.5)  # pauses for 1 second


def get_multiple_songs_amazon(song_ids, access_token, profile_id):
    global albums_ids, artists_ids

    for chunk in chunks(song_ids):

        playlists_in_chunk = [song_id[0] for song_id in chunk]
        positions_in_chunk = [song_id[1] for song_id in chunk]
        song_ids_in_chunk = [song_id[2] for song_id in chunk]
        url = (
            f"https://api.music.amazon.dev/v1/tracks/?ids={','.join(song_ids_in_chunk)}"
        )

        headers = {
            "Authorization": f"Bearer {access_token}",
            "x-api-key": profile_id,
            "Content-Type": "application/json",
        }

        response = requests.get(url, headers=headers)

        # Check the response status code
        if response.status_code == 429:  # "Too Many Requests"
            access_token = input("Please enter a new access token: ")

            # Retry the request with the next token
            headers["Authorization"] = f"Bearer {access_token}"
            response = requests.get(url, headers=headers)

        # if response.status_code != 200:
        #     print(response.json())
        #     return

        tracks_info = response.json()["data"]["track"]

        for index, track_info in enumerate(tracks_info):

            # Extract the song information
            name = track_info["shortTitle"]
            duration = track_info["duration"]
            release_date = track_info["releaseDate"]
            release_date = datetime.strptime(
                release_date, "%Y-%m-%dT%H:%M:%S.%fZ"
            ).strftime("%Y-%m-%d")
            explicit = track_info["parentalSettings"]["hasExplicitLanguage"]
            image_url = track_info["images"][0]["url"]

            # Get main artist
            main_artist_name = track_info["artists"][0]["name"]
            main_artist = Artist.objects.filter(
                name__icontains=main_artist_name
            ).first()

            if main_artist is None:
                main_artist = Artist.objects.create(name=main_artist_name)
                artists_ids.add(track_info["artists"][0]["id"])

            # Create or update the album
            album_name = track_info["album"]["title"]
            album = Album.objects.filter(
                name__icontains=album_name, artist=main_artist
            ).first()

            if album is None:
                album = Album.objects.create(name=album_name, artist=main_artist)
                albums_ids.append(track_info["album"]["id"])

            # Create or update the song
            song = Song.objects.filter(
                name__icontains=name, main_artist=main_artist
            ).first()

            if song is None:
                song = Song.objects.create(name=name, main_artist=main_artist)
                created = True
            else:
                created = False

            # If the song was created or if it exists and a field is None, update the field
            if created or (song.images is None and image_url is not None):
                song.images = image_url
            if created or (song.release_date is None and release_date is not None):
                song.release_date = release_date
            if created or (song.duration is None and duration is not None):
                song.duration = duration
            if created or (song.explicit is None and explicit is not None):
                song.explicit = explicit
            if created or (song.album is None and album is not None):
                song.album = album

            # Create or update the collaborator
            for art_info in track_info["artists"][1:]:
                colab_name = art_info["name"]
                colab = Artist.objects.filter(name__icontains=colab_name).first()

                if colab is None:
                    colab = Artist.objects.create(name=colab_name)
                    artists_ids.add(art_info["id"])

                # Add the collaborator to the song's collaborators
                song.collaborators.add(colab)

            song.available_at.append("Amazon Music")
            song.save()

            # Update "Top Country" playlist
            playlist_name = playlists_in_chunk[index]
            pos = positions_in_chunk[index]
            position, _ = Position.objects.get_or_create(position=pos)
            playlist, _ = Playlist.objects.get_or_create(
                name=playlist_name, website=Website.objects.get(name="Amazon Music")
            )
            PlaylistSong.objects.update_or_create(
                song=song, playlist=playlist, position=position
            )

        time.sleep(1.5)  # pauses for 1 second

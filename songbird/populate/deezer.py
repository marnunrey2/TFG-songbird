from bs4 import BeautifulSoup
import urllib.request
import json
from datetime import timedelta

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

song_ids = set()
album_ids = set()
artist_ids = set()


def deezer():

    # Define the playlists
    top_playlists = {
        "Top Global": "3155776842",
        "Top Spain": "1116190041",
        "Top USA": "1313621735",
        "Top France": "1109890291",
        "Top Colombia": "1116188451",
        "Top Argentina": "1279119721",
        "Top Germany": "1111143121",
        "Top Italy": "1116187241",
        "Top Japan": "1362508955",
        "Top South Korea": "1362510315",
        "Top UK": "1111142221",
    }

    website, _ = Website.objects.get_or_create(name="Deezer")

    # Fetch the songs, albums, and artists from all the playlists
    for playlist_name, playlist_id in top_playlists.items():
        get_playlist_deezer(playlist_name, playlist_id)


def get_playlist_deezer(playlist_name, playlist_id):

    # BeautifulSoup
    url = "https://www.deezer.com/es/playlist/"
    f = urllib.request.urlopen(url + playlist_id)
    s = BeautifulSoup(f, "lxml")

    song_links = s.find("body").find("div", id="dzr-app").find("script").string

    playlist = json.loads(song_links.split(" = ")[1])

    # SNG_ID, PRODUCT_TRACK_ID, UPLOAD_ID, SNG_TITLE, ART_ID, PROVIDER_ID, ART_NAME, ARTIST_IS_DUMMY, ARTISTS, ALB_ID, ALB_TITLE, VIDEO, DURATION, ALB_PICTURE, ART_PICTURE, RANK_SNG, FILESIZE, GAIN, MEDIA_VERSION, DISK_NUMBER, TRACK_NUMBER, TRACK_TOKEN, TRACK_TOKEN_EXPIRE, VERSION, MEDIA, EXPLICIT_LYRICS, RIGHTS, ISRC, DATE_ADD, HIERARCHICAL_TITLE, SNG_CONTRIBUTORS, LYRICS_ID, EXPLICIT_TRACK_CONTENT, VARIATION,__TYPE__
    songs_list = playlist["SONGS"]["data"]

    for song_info in songs_list:

        # NAME -> SNG_TITLE
        name = song_info["SNG_TITLE"]

        # Create or update the artist
        for art_info in song_info["ARTISTS"]:
            artist_name = art_info["ART_NAME"]
            artist, created = Artist.objects.get_or_create(name=artist_name)

        # Create or update the album
        album_name = song_info["ALB_TITLE"]
        album_picture = song_info["ALB_PICTURE"]
        album, created = Album.objects.get_or_create(name=album_name, artist=artist)

        # If the album was created or if it exists and images is None, update the images field
        if created or (album.images is None and album_picture is not None):
            album.images = album_picture
            album.save()

        # DURATION -> DURATION
        duration = song_info["DURATION"]

        # EXPLICIT_LYRICS -> EXPLICIT_LYRICS
        explicit = True if song_info["EXPLICIT_LYRICS"] == "1" else False

        # Create or update the song
        song, created = Song.objects.update_or_create(
            name=name,
            main_artist=Artist.objects.get(name=song_info["ART_NAME"]),
            defaults={
                "duration": duration,
                "explicit": explicit,
                "album": album,
            },
        )

        # Create or update the collaborator
        if len(song_info["ARTISTS"]) > 1:
            for a in song_info["ARTISTS"][1:]:
                colab_name = a["ART_NAME"]
                colab_picture = a["ART_PICTURE"]
                colab, created = Artist.objects.get_or_create(name=colab_name)

                # If the artist was created or if it exists and images is None, update the images field
                if created or (colab.images is None and colab_picture is not None):
                    colab.images = colab_picture
                    colab.save()

                # Add the collaborator to the song's collaborators
                song.collaborators.add(colab)

        # Create or update a PlaylistSong instance
        ranking = song_info["RANK_SNG"]
        position, _ = Position.objects.get_or_create(position=ranking)
        playlist, _ = Playlist.objects.get_or_create(
            name="All Time Top", website=Website.objects.get(name="Deezer")
        )
        PlaylistSong.objects.update_or_create(
            song=song, playlist=playlist, position=position
        )

        song.save()

    # Create a Playlist instance
    playlist, _ = Playlist.objects.get_or_create(
        name=playlist_name, website=Website.objects.get(name="Deezer")
    )

    for index, song_info in enumerate(songs_list):

        position, _ = Position.objects.get_or_create(position=index + 1)

        # Get the song, album, and artist
        main_artist = Artist.objects.get(name=song_info["ART_NAME"])
        song = Song.objects.get(name=song_info["SNG_TITLE"], main_artist=main_artist)

        # Create or update a PlaylistSong instance
        PlaylistSong.objects.update_or_create(
            song=song, playlist=playlist, position=position
        )

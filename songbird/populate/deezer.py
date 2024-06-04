import json
import requests
import urllib.request
from bs4 import BeautifulSoup
from .models import (
    Song,
    Album,
    Artist,
    Website,
    Playlist,
    PlaylistSong,
    Position,
    Genre,
)

song_ids = set()
album_ids = set()
artist_ids = set()


def deezer():

    # Define the playlists
    top_playlists = {
        "Top Global": "3155776842",
        "Top Spain": "1116190041",
        "Top USA": "1313621735",
        "Top UK": "1111142221",
        "Top Canada": "1652248171",
        "Top South Korea": "1362510315",
        "Top France": "1109890291",
        "Top Germany": "1111143121",
        "Top Australia": "1313616925",
        "Top Colombia": "1116188451",
        "Top Argentina": "1279119721",
        "Top Italy": "1116187241",
        "Top Japan": "1362508955",
    }

    Website.objects.get_or_create(name="Deezer")

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

    for index, song_info in enumerate(songs_list):

        # NAME -> SNG_TITLE
        name = song_info["SNG_TITLE"]

        # DURATION -> DURATION
        duration = song_info["DURATION"]

        # EXPLICIT_LYRICS -> EXPLICIT_LYRICS
        explicit = True if song_info["EXPLICIT_LYRICS"] == "1" else False

        # Get main artist
        main_artist_name = song_info["ARTISTS"][0]["ART_NAME"]
        main_artist_picture = song_info["ARTISTS"][0]["ART_PICTURE"]
        main_artist = Artist.objects.filter(name__icontains=main_artist_name).first()

        if main_artist is None:
            main_artist = Artist.objects.create(name=main_artist_name)
            created = True
        else:
            created = False

        # If the artist was created or if it exists and images is None, update the images field
        if created or (main_artist.images is None and main_artist_picture is not None):
            main_artist.images = main_artist_picture
            main_artist.save()

        # Create or update the album
        album_name = song_info["ALB_TITLE"]
        album = Album.objects.filter(
            name__icontains=album_name, artist=main_artist
        ).first()

        if album is None:
            album = Album.objects.create(name=album_name, artist=main_artist)
            created = True
        else:
            created = False

        # Get the album genres
        album_id = song_info["ALB_ID"]
        response = requests.get(f"https://api.deezer.com/album/{album_id}")
        album_info = response.json()
        genres = album_info["genres"]["data"]
        for genre in genres:
            genre_name = genre["name"]
            for g in Genre.BASE_GENRES:
                if g in genre_name.upper():
                    genre_obj, _ = Genre.objects.get_or_create(name=g)
                    album.genres.add(genre_obj)

        # If the album was created or if it exists and images is None, update the images field
        album_picture = album_info["cover_medium"]
        if (
            created
            or (album.images is None and album_picture is not None)
            or not (
                album.images.startswith("http://")
                or album.images.startswith("https://")
            )
        ):
            album.images = album_picture

        album.save()

        # Create or update the song
        song = Song.objects.filter(
            name__icontains=name, main_artist=main_artist
        ).first()

        if song is None:
            song = Song.objects.create(name=name, main_artist=main_artist)
            created = True
        else:
            created = False

        song.duration = duration
        song.explicit = explicit
        song.album = album

        # Create or update the collaborator
        for art_info in song_info["ARTISTS"][1:]:
            colab_name = art_info["ART_NAME"]
            colab_picture = art_info["ART_PICTURE"]
            colab = Artist.objects.filter(name__icontains=colab_name).first()

            if colab is None:
                colab = Artist.objects.create(name=colab_name)
                created = True
            else:
                created = False

            # If the artist was created or if it exists and images is None, update the images field
            if created or (colab.images is None and colab_picture is not None):
                colab.images = colab_picture
                colab.save()

            # Add the collaborator to the song's collaborators
            song.collaborators.add(colab)

        song.available_at.append("Deezer")
        song.save()

        # Update "All Time Top" playlist
        ranking = song_info["RANK_SNG"]
        position, _ = Position.objects.get_or_create(position=ranking)
        playlist, _ = Playlist.objects.get_or_create(
            name="All Time Top", website=Website.objects.get(name="Deezer")
        )
        PlaylistSong.objects.update_or_create(
            song=song, playlist=playlist, position=position
        )

        # Update "Top Country" playlist
        position, _ = Position.objects.get_or_create(position=index + 1)
        playlist, _ = Playlist.objects.get_or_create(
            name=playlist_name, website=Website.objects.get(name="Deezer")
        )
        PlaylistSong.objects.update_or_create(
            song=song, playlist=playlist, position=position
        )

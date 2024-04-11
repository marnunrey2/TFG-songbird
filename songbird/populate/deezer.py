from populate.models import Genre, Artist, Album, Song

from bs4 import BeautifulSoup
import urllib.request
import json
from datetime import timedelta


def deezer():

    # BeautifulSoup
    url = "https://www.deezer.com/es/playlist"
    codigo = "/1116190041"
    f = urllib.request.urlopen(url + codigo)
    s = BeautifulSoup(f, "lxml")

    song_links = s.find("body").find("div", id="dzr-app").find("script").string

    playlist = json.loads(song_links.split(" = ")[1])

    # PLAYLIST_ID, TITLE, TITLE_SEO, TYPE, STATUS, PARENT_PLAYLIST_ID, PARENT_USER_ID, PARENT_USERNAME, PARENT_USER_PICTURE, DESCRIPTION, PLAYLIST_PICTURE, PICTURE_TYPE, DURATION, NB_SONG, FANS, RANK, CHECKSUM, NB_FAN, DATE_ADD, DATE_MOD, HAS_ARTIST_LINKED, IS_SPONSORED, __TYPE__, IS_FAVORITE
    playlist_info = playlist["DATA"]

    # SNG_ID, PRODUCT_TRACK_ID, UPLOAD_ID, SNG_TITLE, ART_ID, PROVIDER_ID, ART_NAME, ARTIST_IS_DUMMY, ARTISTS, ALB_ID, ALB_TITLE, VIDEO, DURATION, ALB_PICTURE, ART_PICTURE, RANK_SNG, FILESIZE, GAIN, MEDIA_VERSION, DISK_NUMBER, TRACK_NUMBER, TRACK_TOKEN, TRACK_TOKEN_EXPIRE, VERSION, MEDIA, EXPLICIT_LYRICS, RIGHTS, ISRC, DATE_ADD, HIERARCHICAL_TITLE, SNG_CONTRIBUTORS, LYRICS_ID, EXPLICIT_TRACK_CONTENT, VARIATION,__TYPE__
    songs_list = playlist["SONGS"]["data"]

    for song_info in songs_list:

        # NAME -> SNG_TITLE
        name = song_info["SNG_TITLE"]

        # Create or update the artist
        artist_name = song_info["ART_NAME"]
        artist_picture = song_info["ART_PICTURE"]
        artist, created = Artist.objects.get_or_create(name=artist_name)

        # If the artist was created or if it exists and images is None, update the images field
        if created or (artist.images is None and artist_picture is not None):
            artist.images = artist_picture
            artist.save()

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

        # LYRICS -> LYRICS_ID
        # MEDIA -> HREF (url a un trozo de la cancion)

        # Create or update the song
        song, created = Song.objects.update_or_create(
            name=name,
            main_artist=artist,
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

        song.save()

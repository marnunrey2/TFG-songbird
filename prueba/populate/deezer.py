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

    artists = []
    albums = []
    songs = []

    for song in songs_list:

        # NAME -> SNG_TITLE
        name = song["SNG_TITLE"]

        # ARTIST & COLABORATORS INFO -> ART_NAME, ARTISTS, ART_PICTURE
        artist_name = song["ART_NAME"]
        artist_picture = song["ART_PICTURE"]
        artists.append({"name": artist_name, "images": artist_picture})
        # artist, created = Artist.objects.get_or_create(
        #     name=artist_name, images=artist_picture
        # )

        for a in song["ARTISTS"]:
            colab_name = a["ART_NAME"]
            colaborator_picture = a["ART_PICTURE"]
            if colab_name != artist_name:
                artists.append({"name": colab_name, "images": colaborator_picture})
                # colab, created = Artist.objects.get_or_create(
                #     name=colab_name, images=colaborator_picture
                # )

        # ALBUM -> ALB_TITLE, ALB_PICTURE
        album_name = song["ALB_TITLE"]
        album_picture = song["ALB_PICTURE"]
        albums.append({"name": album_name, "images": album_picture})
        # album, created = Album.objects.get_or_create(
        #     name=album_name, images=album_picture
        # )

        # DURATION -> DURATION
        duration = song["DURATION"]

        # EXPLICIT_LYRICS -> EXPLICIT_LYRICS
        explicit = True if song["EXPLICIT_LYRICS"] == "1" else False

        # LYRICS -> LYRICS_ID
        # MEDIA -> HREF (url a un trozo de la cancion)

        # Update or create the song
        songs.append(
            {
                "name": name,
                "duration": duration,
                "explicit": explicit,
            }
        )
        # song, created = Song.objects.update_or_create(
        #     name=name,
        #     duration=duration,
        #     explicit=explicit,
        # )

        # artist.save()
        # album.save()
        # song.save()

    return (
        {tuple(d.items()) for d in songs},
        {tuple(d.items()) for d in artists},
        {tuple(d.items()) for d in albums},
    )

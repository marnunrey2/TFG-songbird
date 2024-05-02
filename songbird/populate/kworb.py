from bs4 import BeautifulSoup
import urllib.request
from .models import (
    Song,
    Artist,
    Website,
    Playlist,
    PlaylistSong,
    Position,
)


def kworb_all_time():
    kworb_spotify_all_time()
    kworb_apple_music_all_time()


def kworb_spotify_all_time():

    # BeautifulSoup
    url = f"https://kworb.net/spotify/songs.html"
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f, "lxml")

    song_links = s.find("table", class_="sortable").find("tbody").find_all("tr")

    playlist, _ = Playlist.objects.get_or_create(
        name="All Time Top", website=Website.objects.get(name="Spotify")
    )

    pos = 1
    for song in song_links:
        song_info = song.find_all("td")
        s = song_info[0].text.split(" - ")
        artist_name = s[0].strip()
        song_name = s[1].strip()
        streams = int(song_info[1].text.strip().replace(",", ""))

        main_artist, _ = Artist.objects.get_or_create(name=artist_name)
        song, _ = Song.objects.update_or_create(
            name=song_name,
            main_artist=main_artist,
            defaults={"spotify_streams": streams},
        )

        position, _ = Position.objects.get_or_create(position=pos)

        # Create or update a PlaylistSong instance
        PlaylistSong.objects.update_or_create(
            song=song, playlist=playlist, position=position
        )

        if pos == 100:
            break

        pos += 1


def kworb_apple_music_all_time():

    # BeautifulSoup
    url = f"https://kworb.net/apple_songs/totals.html"
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f, "lxml")

    song_links = s.find("table", class_="sortable").find("tbody").find_all("tr")

    playlist, _ = Playlist.objects.get_or_create(
        name="All Time Top", website=Website.objects.get(name="Apple Music")
    )

    pos = 1
    for song in song_links:
        song_info = song.find_all("td")
        s = song_info[0].text.split(" - ")
        artist_name = s[0].strip()
        song_name = s[1].strip()
        streams = int(song_info[4].text.strip().replace(",", ""))

        main_artist, _ = Artist.objects.get_or_create(name=artist_name)
        song, _ = Song.objects.update_or_create(
            name=song_name,
            main_artist=main_artist,
            defaults={"spotify_streams": streams},
        )

        position, _ = Position.objects.get_or_create(position=pos)

        # Create or update a PlaylistSong instance
        PlaylistSong.objects.update_or_create(
            song=song, playlist=playlist, position=position
        )

        if pos == 100:
            break

        pos += 1

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

BASE_URL = "https://kworb.net"

countries = [
    "Worldwide",
    "spain",
    "United States",
    "France",
    "Colombia",
    "Argentina",
    "Germany",
    "India",
    "Italy",
    "Japan",
    "South Korea",
    "United Kingdom",
]


def apple_music():

    Website.objects.get_or_create(name="Apple Music")
    Website.objects.get_or_create(name="Shazam")

    # BeautifulSoup
    url = f"{BASE_URL}/charts/"
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f, "lxml")

    song_links = s.find("table", class_="sortable").find("tbody").find_all("tr")

    for song in song_links:
        tds = song.find_all("td")

        country = tds[0].text.strip()

        if country in countries:

            if country == "United States":
                country = "USA"
            elif country == "United Kingdom":
                country = "UK"
            elif country == "Wordwide":
                country = "Global"

            # Apple Music
            playlist, _ = Playlist.objects.get_or_create(
                name=f"Top {country}", website=Website.objects.get(name="Apple Music")
            )
            get_songs(tds[3].find("a")["href"], playlist)

            # Shazam
            playlist, _ = Playlist.objects.get_or_create(
                name=f"Top {country}", website=Website.objects.get(name="Shazam")
            )
            get_songs(tds[5].find("a")["href"], playlist)

            # youtube_songs = get_songs(tds[4].find("a")["href"]) if tds[4].find("a") else []


def get_songs(href, playlist):

    # BeautifulSoup
    url = f"{BASE_URL}{href}"
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f, "lxml")

    try:
        content = s.find("table", class_="sortable").find("tbody").find_all("tr")
    except:
        return

    for cont in content:
        tds = cont.find_all("td")

        pos = int(tds[0].text.strip())

        if len(tds) < 3:
            song_info = tds[-1].text.strip()
        else:
            song_info = tds[2].text

        song = song_info.split(" - ")
        artist_name = song[0].strip()
        song_name = song[1].strip()

        main_artist, _ = Artist.objects.get_or_create(name=artist_name)
        song, _ = Song.objects.get_or_create(
            name=song_name,
            main_artist=main_artist,
        )
        song.available_at.append("Apple Music")
        song.save()

        position, _ = Position.objects.get_or_create(position=pos)

        # Create or update a PlaylistSong instance
        PlaylistSong.objects.update_or_create(
            song=song, playlist=playlist, position=position
        )

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
    "Spain",
    "United States",
    "United Kingdom",
    "Canada",
    "South Korea",
    "France",
    "Germany",
    "Australia",
    "Colombia",
    "Argentina",
    "Italy",
    "Japan",
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
            elif country == "Worldwide":
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

        # Get Info
        song = song_info.split(" - ")
        song_name = song[1].strip()

        artists = song[0].replace(" & ", ",").split(",")
        artist_name = artists[0].strip()

        collaborators = artists[1:]
        more_colabs = (
            song[1].split("feat. ")[1].replace(")", "").replace(" & ", ",").split(",")
            if "feat. " in song[1]
            else []
        )
        collaborators += [colab.strip() for colab in more_colabs]

        # Get main artist
        main_artist = Artist.objects.filter(name__icontains=artist_name).first()

        if main_artist is None:
            main_artist = Artist.objects.create(name=artist_name)

        # Create or update the song
        song = Song.objects.filter(
            name__icontains=song_name, main_artist=main_artist
        ).first()

        if song is None:
            song = Song.objects.create(name=song_name, main_artist=main_artist)

        # Create or update the collaborator
        for colab_name in collaborators:
            colab = Artist.objects.filter(name__icontains=colab_name).first()

            if colab is None:
                colab = Artist.objects.create(name=colab_name)

            # Add the collaborator to the song's collaborators
            song.collaborators.add(colab)

        song.available_at.append("Apple Music")
        song.save()

        # Only get the top 100 songs
        if pos <= 100:

            # Update "Top Country" playlist
            position, _ = Position.objects.get_or_create(position=pos)
            PlaylistSong.objects.update_or_create(
                song=song, playlist=playlist, position=position
            )

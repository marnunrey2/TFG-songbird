from bs4 import BeautifulSoup
import urllib.request

from .models import (
    Song,
    Album,
    Artist,
    Website,
    Playlist,
    PlaylistSong,
    Position,
)


def billboard():

    Website.objects.get_or_create(name="Billboard")

    # BeautifulSoup
    url = f"https://www.billboard.com/charts/hot-100/"
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f, "lxml")

    song_links = s.find("div", class_="chart-results-list").find_all(
        "div", class_="o-chart-results-list-row-container"
    )

    for song_info in song_links:
        info = song_info.find("ul").find_all("li")
        song_list = [
            child.text.strip().replace("\n", "").replace("\t", "")
            for li in info
            for child in li.children
            if child.name
        ]
        song_list = [li for li in song_list if li]

        pos = song_list[0]
        song_name = song_list[-9]
        artists = (
            song_list[-8]
            .replace("Featuring", ",")
            .replace(" & ", ",")
            .replace(" x ", ",")
            .replace(" X ", ",")
            .replace(" + ", ",")
            .replace(": Ye", "")
            .split(",")
        )
        # last_week = song_list[-3]
        # peak = song_list[-2]
        # weeks = song_list[-1]

        # Get main artist
        main_artist = Artist.objects.filter(name__icontains=artists[0]).first()

        if main_artist is None:
            main_artist = Artist.objects.create(name=artists[0])

        # Create or update the song
        song_picture = info[1].find("img")["data-lazy-src"]
        song = Song.objects.filter(
            name__icontains=song_name, main_artist=main_artist
        ).first()

        if song is None:
            song = Song.objects.create(name=song_name, main_artist=main_artist)
            created = True
        else:
            created = False

        # If the song was created or if it exists and images is None, update the images field
        if created or (song.images is None and song_picture is not None):
            song.images = song_picture
            song.save()

        # Create or update the collaborator
        for art in artists[1:]:
            colab = Artist.objects.filter(name__icontains=art).first()

            if colab is None:
                colab = Artist.objects.create(name=art)

            # Add the collaborator to the song's collaborators
            song.collaborators.add(colab)

        # Update "Billboard" playlist
        position, _ = Position.objects.get_or_create(position=pos)
        playlist, _ = Playlist.objects.get_or_create(
            name="Hot 100 Billboard", website=Website.objects.get(name="Billboard")
        )
        PlaylistSong.objects.update_or_create(
            song=song, playlist=playlist, position=position
        )

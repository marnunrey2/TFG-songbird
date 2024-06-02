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
    Website.objects.get_or_create(name="Spotify")
    Website.objects.get_or_create(name="Apple Music")

    kworb_all_time_website("Spotify", "https://kworb.net/spotify/songs.html", 1)
    kworb_all_time_website(
        "Apple Music", "https://kworb.net/apple_songs/totals.html", 4
    )


def kworb_all_time_website(website_name, url, streams_index):
    # BeautifulSoup
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f, "lxml")

    song_links = s.find("table", class_="sortable").find("tbody").find_all("tr")

    playlist, _ = Playlist.objects.get_or_create(
        name="All Time Top", website=Website.objects.get(name=website_name)
    )

    pos = 1
    for song in song_links:
        song_info = song.find_all("td")
        s = song_info[0].text.split(" - ")
        artists = s[0].replace(" & ", ", ").replace(" x ", ", ").split(", ")
        if "chase" in artists and "status" in artists:
            index = artists.index("chase")
            artists.remove("chase")
            artists.remove("status")
            artists.insert(index, "chase & status")

        artist_name = artists[0].strip()
        collaborators = artists[1:]
        song_name = s[1].strip()
        streams = int(song_info[streams_index].text.strip().replace(",", ""))

        # Get or create the main artist
        main_artist = Artist.objects.filter(name__icontains=artist_name).first()

        if main_artist is None:
            main_artist = Artist.objects.create(name=artist_name)

        # Get or create the song
        song = Song.objects.filter(
            name__icontains=song_name, main_artist=main_artist
        ).first()

        if song is None:
            song = Song.objects.create(name=song_name, main_artist=main_artist)

        if collaborators:
            for collaborator in collaborators:
                collaborator = collaborator.strip()
                artist = Artist.objects.filter(name__icontains=collaborator).first()

                if artist is None:
                    artist = Artist.objects.create(name=collaborator)

                song.collaborators.add(artist)

        song.available_at.append(website_name)
        song.reproductions[website_name] = streams
        song.save()

        # Update "All Time Top" playlist
        position, _ = Position.objects.get_or_create(position=pos)
        PlaylistSong.objects.update_or_create(
            song=song, playlist=playlist, position=position
        )

        if pos == 100:
            break

        pos += 1

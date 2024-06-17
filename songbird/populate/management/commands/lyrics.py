import lyricsgenius
from dotenv import load_dotenv
from django.core.management.base import BaseCommand
import os
import re
import requests
from ...models import Song
from fuzzywuzzy import fuzz


def genius_lyrics():
    # Load the .env file
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    token = os.getenv("GENIUS_ACCESS_TOKEN")

    genius = lyricsgenius.Genius(token)

    # Get all songs from the database
    songs = Song.objects.filter(lyrics__isnull=True)

    print(f"Finding lyrics for: {songs.count()} songs")
    errors = 0
    timeouts = 0

    for song in songs:
        if (
            song is None
            or song.name == ""
            or song.name == "Unknown"
            or song.main_artist is None
        ):
            print(f"Song '{song.name}'is None or empty. Skipping to next song.")
            continue

        song_name = song.name
        artist_name = song.main_artist.name
        try:
            genius_song = genius.search_song(song_name, artist_name)

            # Check if genius_song is None
            if genius_song is None:
                continue

            # Check if the song name and the genius title are similar
            similarity = fuzz.ratio(
                song_name.lower() + " " + artist_name.lower(),
                genius_song.title.lower() + " " + genius_song.artist.lower(),
            )
            if similarity < 60:
                print(
                    f"SIMILARITY SMALL: Song name '{song_name}' and genius title '{genius_song.title}' are not similar. Skipping to next song."
                )
                continue

            # Refactor lyrics
            lyrics = genius_song.lyrics.split("Lyrics")[1:]
            lyrics = "".join(lyrics)
            lyrics = re.sub(r"\d*Embed$", "", lyrics)
            lyrics = re.sub(r'\[Letra de ".*?"\]', "", lyrics)

            song.lyrics = lyrics
            song.save()

        except requests.exceptions.Timeout:
            print(f"TIMEOUT: song {song_name} by {artist_name}. Skipping to next song.")
            timeouts += 1
            continue
        except Exception as e:
            print(f"ERROR: {e}")
            errors += 1
            continue

    # Songs without lyrics
    songs = Song.objects.filter(lyrics__isnull=True)
    songs_names = [song.name for song in songs]
    print(f"Songs without lyrics: {songs.count()}")
    print(songs_names)
    print(f"Total Errors: {errors}")
    print(f"Total Timeouts: {timeouts}")


class Command(BaseCommand):
    help = "Index data for Whoosh search"

    def handle(self, *args, **kwargs):
        genius_lyrics()
        self.stdout.write(self.style.SUCCESS("Successfully extracted lyrics"))


def genius_lyrics_of_a_song(song_name):
    # Load the .env file
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    token = os.getenv("GENIUS_ACCESS_TOKEN")

    genius = lyricsgenius.Genius(token)

    # Get all songs from the database
    song = Song.objects.filter(name=song_name).first()

    if (
        song is None
        or song.name == ""
        or song.name == "Unknown"
        or song.main_artist is None
    ):
        print(f"Song '{song.name}'is None or empty. Skipping to next song.")
        return

    song_name = song.name
    artist_name = song.main_artist.name

    print(song_name, artist_name)
    try:
        genius_song = genius.search_song(song_name, artist_name)
        print(genius_song)
        print(genius_song.title)
        print(genius_song.artist)

        # Check if genius_song is None
        if genius_song is None:
            return

        # Check if the song name and the genius title are similar
        similarity = fuzz.ratio(
            song_name.lower() + " " + artist_name.lower(),
            genius_song.title.lower() + " " + genius_song.artist.lower(),
        )
        print(similarity)
        if similarity < 60:
            print(
                f"SIMILARITY SMALL: Song name '{song_name}' and genius title '{genius_song.title}' are not similar. Skipping to next song."
            )
            return

        # Refactor lyrics
        lyrics = genius_song.lyrics.split("Lyrics")[1:]
        lyrics = "".join(lyrics)
        lyrics = re.sub(r"\d*Embed$", "", lyrics)
        lyrics = re.sub(r'\[Letra de ".*?"\]', "", lyrics)

        song.lyrics = lyrics
        song.save()

    except requests.exceptions.Timeout:
        print(f"TIMEOUT: Song {song_name} by {artist_name}. Skipping to next song.")
        return
    except Exception as e:
        print(f"ERROR: {e}")
        return


"""
import requests
from dotenv import load_dotenv
import os


def search_genius(query):
    # Load the .env file
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    token = os.getenv("GENIUS_ACCESS_TOKEN")

    url = "https://api.genius.com/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        results = response.json()["response"]["hits"]
        songs = [result["result"]["full_title"] for result in results]
        return songs
    else:
        return None


# Usage
query = "fornight taylor swift"
result = search_genius(query)

print(result)
"""

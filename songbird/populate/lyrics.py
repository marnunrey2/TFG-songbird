import lyricsgenius
from dotenv import load_dotenv
import os
import re
import requests
from .models import Song


def genius_lyrics():
    # Load the .env file
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    token = os.getenv("GENIUS_ACCESS_TOKEN")

    genius = lyricsgenius.Genius(token)

    # Get all songs from the database
    songs = Song.objects.filter(lyrics__isnull=True)

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
        except requests.exceptions.Timeout:
            print(
                f"Request timed out for song {song_name} by {artist_name}. Skipping to next song."
            )
            continue

        # Check if genius_song is None
        if genius_song is None:
            print(
                f"No Genius song found for song {song_name} by {artist_name}. Skipping to next song."
            )
            continue

        # Refactor lyrics
        lyrics = genius_song.lyrics.split("Lyrics")[1:]
        lyrics = "".join(lyrics)
        lyrics = re.sub(r"\d*Embed$", "", lyrics)
        song.lyrics = lyrics
        song.save()

    # Songs without lyrics
    songs = Song.objects.filter(lyrics__isnull=True)
    songs_names = [song.name for song in songs]
    print(f"Songs without lyrics: {songs.count()}")
    print(songs_names)


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

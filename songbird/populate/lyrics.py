import lyricsgenius

genius = lyricsgenius.Genius()
song_name = "To You"
artist_name = "Andy Shauf"
song = genius.search_song(song_name, artist_name)
print(song.lyrics)


# Try search_songs with a chunk of 5 songs

# Try to get artist info (instagram, twitter, facebook, etc.) by
# artist = genius.search_artist("Andy Shauf")
# artist.save_lyrics() (json file)


import requests
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.


def search_genius(query):
    url = "https://api.genius.com/search"
    token = os.getenv("GENIUS_ACCESS_TOKEN")  # get the token from environment variables
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None


# Usage
query = "Kendrick Lamar"
result = search_genius(query)

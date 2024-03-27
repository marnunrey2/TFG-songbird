import requests
from populate.models import Playlist, Song
import time


albums_ids = set()
artists_ids = set()


def get_playlist_songs(playlist_id):
    global albums_ids, artists_ids

    # Access token (expires in 1 hour)
    access_token = "Atza|IwEBIOcVMLRn7fXbSP1QzZeF_IE64_y-taO3UN3juWpWuNfHI7I8iunnf3ZYZ6XcUHgd3oNtmd6kGcPCIpPZcgcR_UTCvRgL9MTk7E60Xr0MFVHqzeYl9HG6QYmuj1oOVrekdL6wNcS6EvC2HfGtyCxFommgDkKUKwayDQyBIKWj65qfqL2nVmy7rJ59joQfE9kqwW4IgUduLpgP-aE88jmUqcwPWCdcfPsOvU6Hy7LYCEZ9lLDJXV6wLdPq1o1XLoyO-p98rU2u35srY6zrGeYAB4eF2ydFoRyZkRTa29tjBZQGB6WL2rKcIACL557BwU206elTM7RN_1X5XMVg0xSrmjTSUZ_MzhCKlxVgmP4l6SLpVQYT0zoaS_lHUleCtdODODYeKWWQE_se-qPn3kx3LN4uU6BXEbzmzXbFaAiKfFtGCg"

    # Security Id
    profile_id = "amzn1.application.72b588cbc0d549449095eb4147c3b7a4"

    url = f"https://api.music.amazon.dev/v1/playlists/{playlist_id}/tracks"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "x-api-key": profile_id,
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(response.json())
        return

    playlist_name = response.json()["data"]["playlist"]["title"]
    tracks = response.json()["data"]["playlist"]["tracks"]["edges"]

    songs_ids = []

    for track in tracks:

        # POSITION
        position = int(track["cursor"].split(":")[0]) + 1

        track_info = track["node"]

        # SONG ID
        song_id = track_info["id"]
        songs_ids.append(song_id)

        # ALBUM ID
        album_id = track_info["album"]["id"]
        albums_ids.add(album_id)

        artists = track_info["artists"]

        for art in artists:
            # ARTIST ID
            artist_id = art["id"]
            artists_ids.add(artist_id)

    Playlist.objects.create(name=playlist_name)

    get_songs(songs_ids)


def get_songs(songs_ids):

    # Access token (expires in 1 hour)
    access_token = "Atza|IwEBIOcVMLRn7fXbSP1QzZeF_IE64_y-taO3UN3juWpWuNfHI7I8iunnf3ZYZ6XcUHgd3oNtmd6kGcPCIpPZcgcR_UTCvRgL9MTk7E60Xr0MFVHqzeYl9HG6QYmuj1oOVrekdL6wNcS6EvC2HfGtyCxFommgDkKUKwayDQyBIKWj65qfqL2nVmy7rJ59joQfE9kqwW4IgUduLpgP-aE88jmUqcwPWCdcfPsOvU6Hy7LYCEZ9lLDJXV6wLdPq1o1XLoyO-p98rU2u35srY6zrGeYAB4eF2ydFoRyZkRTa29tjBZQGB6WL2rKcIACL557BwU206elTM7RN_1X5XMVg0xSrmjTSUZ_MzhCKlxVgmP4l6SLpVQYT0zoaS_lHUleCtdODODYeKWWQE_se-qPn3kx3LN4uU6BXEbzmzXbFaAiKfFtGCg"

    # Security Id
    profile_id = "amzn1.application.72b588cbc0d549449095eb4147c3b7a4"

    for song_id in songs_ids:

        url = f"https://api.music.amazon.dev/v1/tracks/{song_id}"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "x-api-key": profile_id,
            "Content-Type": "application/json",
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(response.json())
            return

        track_info = response.json()["data"]["track"]

        # SONG NAME
        name = track_info["shortTitle"]

        # DURATION
        duration = track_info["duration"]

        # RELEASE DATE
        release_date = track_info["releaseDate"]

        # EXPLICIT LANGUAGE
        explicit = track_info["parentalSettings"]["hasExplicitLanguage"]

        # IMAGE URL
        image_url = track_info["images"][0]["url"]

        Song.objects.create(
            name=name,
            release_date=release_date,
            duration=duration,
            explicit=explicit,
            image=image_url,
        )

        time.sleep(1)  # pauses for 1 second


def amazon_music_api():
    Playlist.objects.all().delete()
    Song.objects.all().delete()

    # Top 50 Most played: International -> B07QHGBGC9
    playlist_id = "B07QHGBGC9"
    get_playlist_songs(playlist_id)

    # Today Hits: Spain -> B073PW84YH
    playlist_id = "B073PW84YH"
    get_playlist_songs(playlist_id)

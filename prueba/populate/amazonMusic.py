import requests
from populate.models import Playlist, Song
import time


songs_ids = set()
albums_ids = set()
artists_ids = set()

songs = []
artists = []
albums = []


def amazon_music_api():

    # Top 50 Most played: International -> B07QHGBGC9
    playlist_id = "B07QHGBGC9"
    get_playlist_songs(playlist_id)

    # Today Hits: Spain -> B073PW84YH
    playlist_id = "B073PW84YH"
    get_playlist_songs(playlist_id)

    return songs, artists, albums


def get_playlist_songs(playlist_id):
    global songs_ids, albums_ids, artists_ids

    # Access token (expires in 1 hour)
    access_token = "Atza|IwEBIF64wtKhDtU7PYhN4AgPglx8h8pLB317kriQA9cldmw_APWYnl5S-WFbJwmVM1rI7e8dQ_Rz-zZ6QyjobfGO6nat1XOj6RJexGGt8R42P0nkz9X9iFlWk3BamD9g_NDQ9My-bTAU5S_vn_TYHB7jSu9gGT4k9KIWY-H-8KSUwDlzuFmNsYf3toSpwwvofd9trtQFjW2R05gQNzimNTeuFBpt_lPQANnQUdoUtwTlSmzgsTdJBDBx2FWWoHJVmpSZ7SZVM4-C99TnbYdXBTvfTgyWP5fi36yFn_4fwf6VFtMEfjfZJDHXqcxCDUgMP8x8N_BWIE0fiS1uJxwB2KvKD34YhKz35tSI-oJ52x1RjzImKZYD_R3vjrFuc90mnGedRojkXW28Dkh-YlXTK1cgUAA78ITR1AUVwiQesEFkW5AIVA"

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

    for track in tracks:

        # POSITION
        position = int(track["cursor"].split(":")[0]) + 1

        track_info = track["node"]

        # SONG ID
        song_id = track_info["id"]
        songs_ids.add(song_id)

        # ALBUM ID
        album_id = track_info["album"]["id"]
        albums_ids.add(album_id)

        artists = track_info["artists"]

        for art in artists:
            # ARTIST ID
            artist_id = art["id"]
            artists_ids.add(artist_id)

    get_artists(artists_ids)
    get_albums(albums_ids)
    get_songs(songs_ids)


def get_artists(artist_ids):
    global artists

    # Access token (expires in 1 hour)
    access_token = "Atza|IwEBIF64wtKhDtU7PYhN4AgPglx8h8pLB317kriQA9cldmw_APWYnl5S-WFbJwmVM1rI7e8dQ_Rz-zZ6QyjobfGO6nat1XOj6RJexGGt8R42P0nkz9X9iFlWk3BamD9g_NDQ9My-bTAU5S_vn_TYHB7jSu9gGT4k9KIWY-H-8KSUwDlzuFmNsYf3toSpwwvofd9trtQFjW2R05gQNzimNTeuFBpt_lPQANnQUdoUtwTlSmzgsTdJBDBx2FWWoHJVmpSZ7SZVM4-C99TnbYdXBTvfTgyWP5fi36yFn_4fwf6VFtMEfjfZJDHXqcxCDUgMP8x8N_BWIE0fiS1uJxwB2KvKD34YhKz35tSI-oJ52x1RjzImKZYD_R3vjrFuc90mnGedRojkXW28Dkh-YlXTK1cgUAA78ITR1AUVwiQesEFkW5AIVA"

    # Security Id
    profile_id = "amzn1.application.72b588cbc0d549449095eb4147c3b7a4"

    for artist_id in artist_ids:

        url = f"https://api.music.amazon.dev/v1/artists/{artist_id}"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "x-api-key": profile_id,
            "Content-Type": "application/json",
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(response.json())
            return

        track_info = response.json()["data"]["artist"]

        # SONG NAME
        name = track_info["name"]

        # IMAGE URL
        image_url = track_info["images"][0]["url"]

        artists.append(
            {
                "name": name,
                "image_url": image_url,
            }
        )

        time.sleep(1)  # pauses for 1 second


def get_albums(album_ids):
    global albums

    # Access token (expires in 1 hour)
    access_token = "Atza|IwEBIF64wtKhDtU7PYhN4AgPglx8h8pLB317kriQA9cldmw_APWYnl5S-WFbJwmVM1rI7e8dQ_Rz-zZ6QyjobfGO6nat1XOj6RJexGGt8R42P0nkz9X9iFlWk3BamD9g_NDQ9My-bTAU5S_vn_TYHB7jSu9gGT4k9KIWY-H-8KSUwDlzuFmNsYf3toSpwwvofd9trtQFjW2R05gQNzimNTeuFBpt_lPQANnQUdoUtwTlSmzgsTdJBDBx2FWWoHJVmpSZ7SZVM4-C99TnbYdXBTvfTgyWP5fi36yFn_4fwf6VFtMEfjfZJDHXqcxCDUgMP8x8N_BWIE0fiS1uJxwB2KvKD34YhKz35tSI-oJ52x1RjzImKZYD_R3vjrFuc90mnGedRojkXW28Dkh-YlXTK1cgUAA78ITR1AUVwiQesEFkW5AIVA"

    # Security Id
    profile_id = "amzn1.application.72b588cbc0d549449095eb4147c3b7a4"

    for album_id in album_ids:

        url = f"https://api.music.amazon.dev/v1/albums/{album_id}"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "x-api-key": profile_id,
            "Content-Type": "application/json",
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(response.json())
            return

        track_info = response.json()["data"]["album"]

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

        albums.append(
            {
                "name": name,
                "duration": duration,
                "release_date": release_date,
                "explicit": explicit,
                "image_url": image_url,
            }
        )

        # ARTISTS
        # for artist in track_info["artists"]:
        #     artists_ids.add(artist["id"])
        # for track in track_info["tracks"]:
        #     songs_ids.add(track["id"])

        time.sleep(1)  # pauses for 1 second


def get_songs(songs_ids):
    global songs

    # Access token (expires in 1 hour)
    access_token = "Atza|IwEBIF64wtKhDtU7PYhN4AgPglx8h8pLB317kriQA9cldmw_APWYnl5S-WFbJwmVM1rI7e8dQ_Rz-zZ6QyjobfGO6nat1XOj6RJexGGt8R42P0nkz9X9iFlWk3BamD9g_NDQ9My-bTAU5S_vn_TYHB7jSu9gGT4k9KIWY-H-8KSUwDlzuFmNsYf3toSpwwvofd9trtQFjW2R05gQNzimNTeuFBpt_lPQANnQUdoUtwTlSmzgsTdJBDBx2FWWoHJVmpSZ7SZVM4-C99TnbYdXBTvfTgyWP5fi36yFn_4fwf6VFtMEfjfZJDHXqcxCDUgMP8x8N_BWIE0fiS1uJxwB2KvKD34YhKz35tSI-oJ52x1RjzImKZYD_R3vjrFuc90mnGedRojkXW28Dkh-YlXTK1cgUAA78ITR1AUVwiQesEFkW5AIVA"

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

        songs.append(
            {
                "name": name,
                "duration": duration,
                "release_date": release_date,
                "explicit": explicit,
                "image_url": image_url,
            }
        )

        # albums_ids.add(track_info["album"]["id"])
        # for artist in track_info["artists"]:
        #     artists_ids.add(artist["id"])

        time.sleep(1)  # pauses for 1 second

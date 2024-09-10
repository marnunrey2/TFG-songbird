from ..models import Artist, Playlist, PlaylistSong, Position, Song, Website, Album
from googleapiclient.discovery import build
from ytmusicapi import YTMusic
import re
import datetime


top_playlists = {
    "All Time Top": "PL8A83124F1D79BD4F",
    "Weekly Top Global": "ZZ",
    "Weekly Top Spain": "ES",
    "Weekly Top USA": "US",
    "Weekly Top France": "FR",
    "Weekly Top Colombia": "CO",
    "Weekly Top Argentina": "AR",
    "Weekly Top Germany": "DE",
    "Weekly Top India": "IN",
    "Weekly Top Italy": "IT",
    "Weekly Top Japan": "JP",
    "Weekly Top South Korea": "KR",
    "Weekly Top UK": "GB",
}

song_ids = set()
album_ids = set()
artist_ids = set()


def youtube_api():
    Website.objects.get_or_create(name="YouTube")

    for playlist_name, playlist_id in top_playlists.items():
        print(playlist_name)
        if playlist_name == "All Time Top":
            all_time_top_playlist(playlist_id)
        else:
            get_ytmusic_charts(playlist_name, playlist_id)


def youtube_token():
    client_id = (
        "Youtube client id"
    )
    client_secret = "Youtube client secret"
    api_key = "Youtube API key"

    youtube = build("youtube", "v3", developerKey=api_key)
    return youtube


def all_time_top_playlist(playlist_id):

    youtube = youtube_token()

    # All time top playlist
    request = youtube.playlistItems().list(
        part="snippet, contentDetails",
        playlistId=playlist_id,
        maxResults=50,
    )

    response = request.execute()

    get_songs(response)


def get_songs(response):

    playlist, _ = Playlist.objects.get_or_create(
        name="All Time Top", website=Website.objects.get(name="YouTube")
    )

    for song in response["items"]:
        # items: kind, etag, id, snippet, contentDetails

        content_details = song["contentDetails"]
        video_id = content_details["videoId"]
        release_date = content_details["videoPublishedAt"]
        release_date = datetime.datetime.strptime(release_date, "%Y-%m-%dT%H:%M:%SZ")

        # items/snippet: publishedAt, channelId, title, description, thumbnails, channelTitle, playlistId, position, resourceId, videoOwnerChannelTitle, videoOwnerChannelId
        snippet = song["snippet"]
        song_name = snippet["title"]
        pos = snippet["position"] + 1
        image = snippet["thumbnails"]["default"]["url"]

        # Get duration and views
        youtube = youtube_token()

        # contentDetails, liveStreamingDetails, localizations, statistics",
        # CANNOT ACCES: ageGating, fileDetails
        request = youtube.videos().list(
            part="contentDetails, statistics",
            id=video_id,
        )

        response = request.execute()

        duration = response["items"][0]["contentDetails"]["duration"]
        match = re.match("PT(\d+)M(\d+)?S?", duration)
        if match:
            minutes = int(match.group(1))
            seconds = int(match.group(2)) if match.group(2) else 0
            duration = minutes * 60 + seconds

        views = response["items"][0]["statistics"]["viewCount"]

        # Clean song name
        song_name = remove_emojis(song_name)

        song_name = (
            song_name.replace("Official Video", "")
            .replace("Official Music Video", "")
            .replace("Original Video", "")
            .replace("Video Oficial", "")
            .replace("OFFICIAL VIDEO", "")
            .replace("Ultra Records", "")
            .replace("Furious 7 Soundtrack", "")
            .replace("The Official 2010 FIFA World Cup™ Song", "")
            .replace("This Time for Africa", "")
            .replace("PURPOSE : The Movement", "")
            .replace("श्री हनुमान चालीसा |", "")
            .replace("Full HD", "")
            .replace("M/V", "")
            .replace("()", "")
            .replace("[]", "")
        )

        division = split_song_name(song_name)

        if "Shree Hanuman" in division[0]:
            artists = [division[3].strip()]
            name = division[0].strip()
            artists.append(division[2].strip())
        elif "Gummy Bear" in division[0]:
            artists = []
            name = division[0].strip()
        else:
            artists = get_artists(division[0])
            name, artists = get_name_and_collaborators(division[1], artists)

        for art in artists:
            Artist.objects.get_or_create(name=art)

        if len(artists) == 0:
            song, _ = Song.objects.update_or_create(
                name=song_name,
                release_date=release_date,
                duration=duration,
                images=image,
            )
        else:
            song, _ = Song.objects.update_or_create(
                name=song_name,
                main_artist=Artist.objects.get(name=artists[0]),
                defaults={
                    "release_date": release_date,
                    "duration": duration,
                    "images": image,
                },
            )
        song.available_at.append("YouTube")
        song.reproductions["YouTube"] = views
        song.save()

        position, _ = Position.objects.get_or_create(position=pos)

        # Create or update a PlaylistSong instance
        PlaylistSong.objects.update_or_create(
            song=song, playlist=playlist, position=position
        )


def remove_emojis(data):
    emoj = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002500-\U00002BEF"  # chinese char
        "\U00002702-\U000027B0"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001f926-\U0001f937"
        "\U00010000-\U0010ffff"
        "\u2640-\u2642"
        "\u2600-\u2B55"
        "\u200d"
        "\u23cf"
        "\u23e9"
        "\u231a"
        "\ufe0f"  # dingbats
        "\u3030"
        "]+",
        re.UNICODE,
    )
    return re.sub(emoj, "", data)


def split_song_name(song_name):
    delimiters = ["|", " - ", ":"]
    for delimiter in delimiters:
        if delimiter in song_name:
            return song_name.split(delimiter)
    return [song_name]


def get_artists(division):
    delimiters = ["&", ",", "  "]
    for delimiter in delimiters:
        if delimiter in division:
            artists = division.split(delimiter)
            return [
                artist.replace("(", "").replace(")", "").strip() for artist in artists
            ]
    return [division.replace("(", "").replace(")", "").strip()]


def get_name_and_collaborators(division, artists):
    features = ["feat.", "ft."]
    for feature in features:
        if feature in division:
            parts = division.split(feature)
            name = parts[0].replace("(", "").replace(")", "").strip()
            if "Remix" in name:
                name = name.replace("Remix", "(Remix)")
            new_artists = get_artists(parts[1])
            artists.extend([artist for artist in new_artists if artist not in artists])
            return name, artists
    name = division.replace("(", "").replace(")", "").strip()
    if "Remix" in name:
        name = name.replace("Remix", "(Remix)")
    return name, artists


def get_ytmusic_charts(playlist_name, country_code):
    global song_ids, album_ids, artist_ids

    ytmusic = YTMusic()
    charts = ytmusic.get_charts(country=country_code)

    playlist, _ = Playlist.objects.get_or_create(
        name=playlist_name, website=Website.objects.get(name="YouTube")
    )

    for pos, video in enumerate(charts["videos"]["items"], start=1):

        position, _ = Position.objects.get_or_create(position=pos)

        video_id = video["videoId"]
        if type(video_id) == str:
            artists = tuple(art["name"] for art in video["artists"])
            song_ids.add((video_id, playlist, position, artists, None))
            artist_ids.update(art["id"] for art in video["artists"])
        else:
            song_name = video["title"]
            artist = video["views"]

            parts = video["artists"][0]["name"].split()  # '4 min 43 sec'
            minutes = int(parts[0])
            seconds = int(parts[2])
            duration = minutes * 60 + seconds

            # Get or create an Artist instance
            main_artist, created = Artist.objects.get_or_create(name=artist)

            # Create or update a Song instance
            song, created = Song.objects.update_or_create(
                name=song_name,
                main_artist=main_artist,
                defaults={
                    "duration": duration,
                },
            )

            # Create or update a PlaylistSong instance
            PlaylistSong.objects.update_or_create(
                song=song, playlist=playlist, position=position
            )

    for artist_id in artist_ids:
        get_charts_artists(artist_id)

    for album_id in album_ids:
        get_charts_albums(album_id)

    for song_id, playlist, position, artists, album_name in song_ids:
        get_charts_songs(song_id, playlist, position, artists, album_name)


def get_charts_artists(artist_id):
    global album_ids
    ytmusic = YTMusic()

    try:
        art_info = ytmusic.get_artist(artist_id)

        art_name = art_info["name"]
        art_followers = art_info["subscribers"]

        # Update or create the artist
        artist, created = Artist.objects.get_or_create(name=art_name)
        artist.followers["YouTube"] = art_followers
        artist.save()

        # Add albums
        art_albums = art_info["albums"]["results"]
        album_ids.update(alb["browseId"] for alb in art_albums)

    except Exception as e:
        print("Artist error: ", e)
        return


def get_charts_albums(album_id):
    global song_ids
    ytmusic = YTMusic()

    try:
        album_info = ytmusic.get_album(album_id)
        album_name = album_info["title"]
        album_release_date = datetime.date(int(album_info["year"]), 1, 1)
        album_total_tracks = album_info["trackCount"]

        # Get the artist
        album_artist = album_info["artists"][0]["name"]
        artist, created = Artist.objects.get_or_create(name=album_artist)

        # Update or create the album
        album, created = Album.objects.update_or_create(
            name=album_name,
            artist=artist,
            defaults={
                "release_date": album_release_date,
                "total_tracks": album_total_tracks,
            },
        )

        # Get the video IDs from album_info["tracks"]
        video_ids = {track["videoId"] for track in album_info["tracks"]}

        # Update tuples
        updated_tuples = set()
        for video_id, playlist, position, artists, _ in song_ids:
            if video_id in video_ids:
                updated_tuples.add((video_id, playlist, position, artists, album_name))
            else:
                updated_tuples.add((video_id, playlist, position, artists, None))

        # Add new tuples for tracks that are not in song_ids
        for video_id in video_ids:
            if video_id not in [song_id for song_id, _, _, _, _ in song_ids]:
                updated_tuples.add((video_id, None, None, (album_artist,), album_name))

        song_ids = updated_tuples

    except Exception as e:
        print("Album error: ", e)
        return


def get_charts_songs(song_id, playlist, position, artists, album_name):
    ytmusic = YTMusic()

    try:
        videos = ytmusic.get_song(videoId=song_id)

        song_name = videos["videoDetails"]["title"]
        song_duration = int(videos["videoDetails"]["lengthSeconds"])
        song_views = videos["videoDetails"]["viewCount"]
        song_release_date_str = videos["microformat"]["microformatDataRenderer"][
            "publishDate"
        ]
        song_release_date = datetime.datetime.strptime(
            song_release_date_str, "%Y-%m-%dT%H:%M:%S%z"
        ).date()

        # Get/create the artist
        main_artist, created = Artist.objects.get_or_create(name=artists[0])

        # Update or create the song
        song, created = Song.objects.update_or_create(
            name=song_name,
            main_artist=main_artist,
            defaults={
                "duration": song_duration,
                "release_date": song_release_date,
            },
        )
        song.available_at.append("YouTube")
        song.reproductions["YouTube"] = song_views

        # Add collaborators
        for artist in artists[1:]:
            collab, created = Artist.objects.get_or_create(name=artist)
            song.collaborators.add(collab)

        if album_name is not None:
            album, created = Album.objects.get_or_create(
                name=album_name, artist__name=main_artist
            )
            song.album = album
        song.save()

        # Create or update a PlaylistSong instance
        if playlist is not None and position is not None:
            PlaylistSong.objects.update_or_create(
                song=song, playlist=playlist, position=position
            )

    except Exception as e:
        print("Song error: ", e)
        return

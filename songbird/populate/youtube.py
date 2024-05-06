from .models import Artist, Playlist, PlaylistSong, Position, Song, Website
from googleapiclient.discovery import build
from ytmusicapi import YTMusic
import re
from datetime import datetime


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


def youtube_api():
    Website.objects.get_or_create(name="YouTube")

    for playlist_name, playlist_id in top_playlists.items():
        # if playlist_name == "All Time Top":
        #     all_time_top_playlist(playlist_id)
        # else:
        get_ytmusic_charts(playlist_id)


def youtube_token():
    client_id = (
        "68827693716-mpcjd7d4onls3ofikmj07prg194rk4f7.apps.googleusercontent.com"
    )
    client_secret = "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"
    api_key = "AIzaSyCd2I915u6iEy2MmpytUXH4En6pMFo9Sk0"

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

    songs = []
    songs = get_songs(songs, response)


def get_songs(songs, response):

    playlist, _ = Playlist.objects.get_or_create(
        name="All Time Top", website=Website.objects.get(name="YouTube")
    )

    for song in response["items"]:
        # items: kind, etag, id, snippet, contentDetails

        content_details = song["contentDetails"]
        video_id = content_details["videoId"]
        release_date = content_details["videoPublishedAt"]
        release_date = datetime.strptime(release_date, "%Y-%m-%dT%H:%M:%SZ")

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

    return songs


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


def get_ytmusic_charts(country_code):
    ytmusic = YTMusic()
    charts = ytmusic.get_charts(country=country_code)
    print(charts)

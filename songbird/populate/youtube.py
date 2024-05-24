from dotenv import load_dotenv
import re
import datetime
import os
from googleapiclient.discovery import build
from .models import Artist, Playlist, PlaylistSong, Position, Song, Website, Album

top_playlists = {
    # "All Time Top": "PL8A83124F1D79BD4F",
    # "Weekly Top Global": "PL4fGSI1pDJn5kI81J1fYWK5eZRl1zJ5kM",
    # "Weekly Top Spain": "PL4fGSI1pDJn4jhQB4kb9M36dvVmJQPt4T",
    # "Weekly Top USA": "PL4fGSI1pDJn69On1f-8NAvX_CYlx7QyZc",
    # "Weekly Top UK": "PL4fGSI1pDJn688ebB8czINn0_nov50e3A",
    # "Weekly Top Canada": "PL4fGSI1pDJn4IeWA7bBJYh__qgOCRMkIh",
    # "Weekly Top France": "PL4fGSI1pDJn50iCQRUVmgUjOrCggCQ9nR",
    # "Weekly Top Germany": "PL4fGSI1pDJn4X-OicSCOy-dChXWdTgziQ",
    # "Weekly Top Australia": "PL4fGSI1pDJn44PMHPLYatj8rta8WYtZ8_",
    "Weekly Top Colombia": "PL4fGSI1pDJn4ObZYxzctc1AM45GSWm2DC",
    "Weekly Top Argentina": "PL4fGSI1pDJn403fWAsjzCMsLEgBTOa25K",
    "Weekly Top Italy": "PL4fGSI1pDJn5BPviUFX4a3IMnAgyknC68",
}

SONG_INFO = {
    "Shree Hanuman Chalisa": ("Shree Hanuman Chalisa", "Hariharan", []),
    "The Gummy Bear Song": ("The Gummy Bear Song", "Gummibär", []),
    "GulabiSadi": ("GulabiSadi", "Sanju Rathod", ["G-SPXRK"]),
    "Maroon Color": ("Maroon Color", "Neelkamal Singh", ["Kalpana", "Om Jha"]),
    "Kurchi Madathapetti": ("Kurchi Madathapetti", "Thaman S", []),
    "Jale 2": ("Jale 2", "Shiva Choudhary", ["Sapna Choudhary"]),
    "Bhojpuri Song 2024": (
        "Bhojpuri Song 2024",
        "Khesari Lal Yadav",
        ["Khushi Kakkar", "Dimpal Singh"],
    ),
    "Bhojpuri Song": (
        "Bhojpuri Song",
        "Khesari Lal Yadav",
        ["Karishma Kakkar", "Dimpal Singh"],
    ),
    "Teri Baaton Mein Aisa Uljha Jiya (Title Track)": (
        "Teri Baaton Mein Aisa Uljha Jiya",
        "Raghav",
        ["Kriti Sanon", "Asees Kaur"],
    ),
    "THE BOX MEDLEY FUNK 2": (
        "THE BOX MEDLEY FUNK 2",
        "MC BRINQUEDO",
        ["MC TUTO", "MC LARANJINHA", "MC CEBEZINHO", "DJ OREIA"],
    ),
    "Illuminati": ("Illuminati", "Vinayak Sasikumar", ["Sushin Shyam"]),
    "Achacho": (
        "Achacho",
        "Hiphop Tamizha",
        ["Kharesma Ravichandran", "Srinisha Jayaseelan"],
    ),
    "Yimmy Yimmy": (
        "Yimmy Yimmy",
        "Jacqueline Fernandez",
        ["Rajat Nagpal", "Shreya Ghoshal", "Tayc"],
    ),
    "สวยขยี้ใจ - บ่าวบุ๊ค": ("บ่าวบุ๊ค", "สวยขยี้ใจ", ["ทิดแอม", "คำมอส"]),
    "สีแชทบ่คือเก่า - เบนซ์ ปรีชา": ("สีแชทบ่คือเก่า", "เบนซ์ ปรีชา", ["พนมรุ้งเรคคอร์ด"]),
    "Bling-Bang-Bang-Born": ("Bling-Bang-Bang-Born", "Creepy Nuts", []),
    "CASCA DE BALA": ("Casca de Bala", "Thrullio Milionário", []),
    "PUSHPA PUSHPA": ("PUSHPA PUSHPA", "DSP", []),
    "Columbia - Quevedo": ("Columbia", "Quevedo", []),
    "LA CHIMICHANGA": ("LA CHIMICHANGA", "Yahir Saldivar", []),
    "CC FREESTYLE": ("CC FREESTYLE", "Central Cee", []),
    "C FREESTYLE": ("C FREESTYLE", "Unknown", []),
    "Loving You Is in My DNA": ("DNA (Loving You)", "Billy Gillies", ["Hannah Boleyn"]),
    "Goin Off": ("Goin Off", "Karan Aujla", []),
    "Naina": ("Naina", "Diljit Dosanjh", ["Badshah"]),
    "Sheesha": ("Sheesha", "Gulab Sidhu", ["Mahi Sharma"]),
    "TEMPS EN TEMPS": ("TEMPS EN TEMPS", "Koba LaD", ["Zola"]),
    "cover Amine Babylone Live 2023": (
        "Choufou l'amour mandar fia",
        "Bilel Tacchini",
        [],
    ),
    "Que Tal - Julian Daza": ("Que Tal", "Julian Daza", []),
    "GANGSTER EN LA DISCO ": ("GANGSTER EN LA DISCO ", "Pirlo", ["Ovi", "Blessd"]),
    "OJITOS ROJOS REMIX": ("OJITOS ROJOS REMIX", "BLESSD", ["RYAN CASTRO"]),
    "Ayer Y Hoy": ("Ayer y Hoy", "La Combinación Vallenata", []),
    "PALABRAS SOBRAN REMIX": (
        "PALABRAS SOBRAN REMIX",
        "BLESSD",
        ["RYAN CASTRO", "BRYANT MYERS", "HADES 66"],
    ),
    "A MIMIR EN EL CHAT": (
        "A Mimir en el Chat",
        "Dejavu FF",
        ["Angi Fire", "Las Gemelas del Free"],
    ),
    "Por Mi Mexico Remix": (
        "Por Mi Mexico Remix",
        "Lefty SM",
        ["Santa Fe Klan", "Dharius", "C-Kan", "MC Davo", "Neto Peña"],
    ),
    "EL AMOR Y LA FELICIDAD": ("EL AMOR Y LA FELICIDAD", "Chakal Del Sur", []),
    "Clavelitos": ("Clavelitos", "Romulo Caicedo", []),
    "TATTOO - ELAGGUME": ("TATTOO", "ELAGGUME", []),
    "ADDO STAJE (RIDE IT NAPOLETAN REMIX)": (
        "ADDO STAJE - Ride it RMX",
        "Le-one",
        ["VTR"],
    ),
}


def youtube_api():
    Website.objects.get_or_create(name="YouTube")

    for playlist_name, playlist_id in top_playlists.items():
        print(playlist_name)
        get_playlist(playlist_id, playlist_name)


def youtube_token():
    # Load the .env file
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

    youtube_api_key = os.getenv("YOUTUBE_API_KEY")
    youtube = build("youtube", "v3", developerKey=youtube_api_key)
    return youtube


def get_playlist(playlist_id, playlist_name):
    youtube = youtube_token()

    request = youtube.playlistItems().list(
        part="snippet, contentDetails",
        playlistId=playlist_id,
        maxResults=50,
    )

    response = request.execute()

    playlist, _ = Playlist.objects.get_or_create(
        name=playlist_name, website=Website.objects.get(name="YouTube")
    )

    get_songs(response, playlist)


def get_songs(response, playlist):
    for song_info in response["items"]:

        if song_info["snippet"]["title"] == "Private video":
            continue

        content_details = song_info["contentDetails"]
        video_id = content_details["videoId"]

        # Get release date, name, position and image
        release_date = content_details["videoPublishedAt"]
        release_date = datetime.datetime.strptime(release_date, "%Y-%m-%dT%H:%M:%SZ")

        snippet = song_info["snippet"]
        youtube_name = snippet["title"]
        pos = snippet["position"] + 1
        image = snippet["thumbnails"]["default"]["url"]

        # Get token
        youtube = youtube_token()

        # contentDetails, liveStreamingDetails, localizations, statistics",
        # CANNOT ACCES: ageGating, fileDetails
        request_video = youtube.videos().list(
            part="contentDetails, statistics",
            id=video_id,
        )

        response_video = request_video.execute()

        # Get duration and views
        duration = response_video["items"][0]["contentDetails"]["duration"]
        match = re.match("PT(\d+)M(\d+)?S?", duration)
        if match:
            minutes = int(match.group(1))
            seconds = int(match.group(2)) if match.group(2) else 0
            duration = minutes * 60 + seconds

        views = response_video["items"][0]["statistics"]["viewCount"]

        # Clean song name
        song_name = remove_emojis(youtube_name)
        song_name = remove_phrases(song_name)

        # Extracting song information handleling weird cases
        if not song_name.strip():
            name = "Unknown"
            artist = "Unknown"
            collaborators = []
        elif "Peso Pluma" in song_name:
            name = song_name.split(" - ")[0]
            artist = "Peso Pluma"
            collaborators = song_name.split(",")[1:] if "," in song_name else []
        elif "RAP LA RUE" in song_name:
            name = song_name.split(" - ")[1].replace("[RAP LA RUE] ROUND 4", "")
            artist = "RAP LA RUE"
            collaborators = song_name.split(" - ")[0].split(" x ")
        elif "Luis Alfonso" in song_name:
            name = song_name.split(" - ")[0]
            if name == "Regalada Sales Cara":
                name = "Regalada Sales Cara (Remix)"
            artists = song_name.split(" - ")[1].replace(" x ", ", ").split(", ")
            artist = artists[0]
            collaborators = [art.replace("(Remix)", "") for art in artists[1:]]
        elif "Elder Dayán" in song_name:
            name = song_name.split(" - ")[0]
            artists = song_name.split(" - ")[1].replace(" y ", ", ").split(", ")
            artist = artists[0]
            collaborators = artists[1:]
        else:
            for key, value in SONG_INFO.items():
                if key in song_name:
                    name, artist, collaborators = value
                    break
            else:
                name, artist, collaborators = extract_info(song_name)

        # print({"song_name": name, "artist": artist, "collaborators": collaborators})
        # print(name)

        name = name.strip()
        artist = artist.strip() if artist else None

        # Creating artists and songs
        if artist is None:
            artist = "Unknown"

        # Get main artist
        main_artist = Artist.objects.filter(name__icontains=artist).first()

        if main_artist is None:
            main_artist = Artist.objects.create(name=artist)

        # Create or update the song
        song = Song.objects.filter(
            name__icontains=name, main_artist=main_artist
        ).first()

        if song is None:
            song = Song.objects.create(name=name, main_artist=main_artist)
            created = True
        else:
            created = False

        # Create or update the collaborators
        for colab in collaborators:
            colab_name = colab.strip()
            if colab_name == "":
                continue

            colab = Artist.objects.filter(name__icontains=colab_name).first()

            if colab is None:
                colab = Artist.objects.create(name=colab_name)

            song.collaborators.add(colab)

        if created or not song.images:
            song.images = image

        if created or not song.duration:
            song.duration = duration

        if created or not song.release_date:
            song.release_date = release_date

        if "YouTube" not in song.reproductions:
            song.reproductions["YouTube"] = views

        song.youtube_name.append(youtube_name)
        song.available_at.append("YouTube")

        song.save()

        # Create or update a PlaylistSong instance
        position, _ = Position.objects.get_or_create(position=pos)
        PlaylistSong.objects.update_or_create(
            song=song, playlist=playlist, position=position
        )


def extract_info(song_name):
    separators = [" - ", " -", "- ", ": ", "  ", "|", " – "]
    for sep in separators:
        if sep in song_name:
            parts = song_name.split(sep)
            break
    else:
        return None

    artists, song = parts[0].strip(), parts[1].strip()

    artist_indicators = [
        ", ",
        " & ",
        "ft. ",
        " ft ",
        "Ft. ",
        "feat. ",
        " feat ",
        "Feat. ",
        "Feat ",
        " Ft ",
        " FT ",
        " with ",
        " X ",
        " x ",
        " y ",
        " e ",
        "  ",
    ]
    collaborators = []

    if (
        artists.lower() == "julión álvarez y su norteño banda"
        or artists.lower() == "felipe & rodrigo"
        or artists.lower() == "pepe y vizio"
        or artists.lower() == "chase & status"
    ):
        main_artist = artists
    elif any(indicator in artists for indicator in artist_indicators):
        for indicator in artist_indicators:
            artists = artists.replace(indicator, ",")
        artists = [
            artist.strip() for artist in artists.split(",") if artist.strip() != ""
        ]
        if "Julión Álvarez" in artists:
            index = artists.index("Julión Álvarez")
            artists.remove("Julión Álvarez")
            artists.insert(index, "Julión Álvarez y su Norteño Banda")
        elif "Felipe" in artists and "Rodrigo" in artists:
            index = artists.index("Felipe")
            artists.remove("Felipe")
            artists.remove("Rodrigo")
            artists.insert(index, "Felipe & Rodrigo")
        elif "Pepe" in artists and "Vizio" in artists:
            index = artists.index("Pepe")
            artists.remove("Pepe")
            artists.remove("Vizio")
            artists.insert(index, "Pepe y Vizio")
        elif "Chase" in artists and "Status" in artists:
            index = artists.index("Chase")
            artists.remove("Chase")
            artists.remove("Status")
            artists.insert(index, "Chase & Status")
        main_artist = artists[0]
        collaborators += artists[1:]
    else:
        main_artist = artists

    especial_indicators = ["|", " X ", " x ", ", ", " y "]
    # Create a set of artist_indicators that are not in especial_indicators
    artist_only_indicators = set(artist_indicators) - set(especial_indicators)

    if (
        song == "Madness & Badness"
        or song == "I P ME, TU P TE"
        or song == "Bloods & Crips"
        or song == "Beauty & The Beast 2"
    ):
        main_song = song
    elif any(indicator in song for indicator in especial_indicators) and not any(
        indicator in song for indicator in artist_only_indicators
    ):
        main_song = main_artist
        for indicator in especial_indicators:
            song = song.replace(indicator, ",")
        song = [s.strip() for s in song.split(",") if s.strip() != ""]
        main_artist = song[0]
        collaborators += song[1:]
    elif any(indicator in song for indicator in artist_indicators):
        for indicator in artist_indicators:
            song = song.replace(indicator, ",")
        song = [s.strip() for s in song.split(",") if s.strip() != ""]
        main_song = song[0]
        collaborators += song[1:]
    else:
        main_song = song

    # Remove starting parenthesis from main_song if it doesn't have a closing parenthesis
    if "(" in main_song and ")" not in main_song:
        main_song = main_song.replace("(", "")
    if "[" in main_song and "]" not in main_song:
        main_song = main_song.replace("[", "")

    # Remove all parentheses from main_artist and collaborators
    main_artist = (
        main_artist.replace("(", "").replace(")", "").replace("[", "").replace("]", "")
    )
    collaborators = [
        collaborator.replace("(", "").replace(")", "").replace("[", "").replace("]", "")
        for collaborator in collaborators
    ]

    return main_song, main_artist, collaborators


def remove_phrases(song_name):

    song_name = re.sub(r"\(.*prod\..*\)", "", song_name)
    song_name = re.sub(r"\(.*Prod\..*\)", "", song_name)
    song_name = re.sub(r"\[.*prod\..*\]", "", song_name)
    song_name = re.sub(r"\[.*Prod\..*\]", "", song_name)

    replacements = [
        "#30GRADOS",
        "#FLOWBR",
        "#OFB",
        "#Tiktok (Videoclip Oficial)",
        "#",
        "The Official 2010 FIFA World Cup™ Song",
        "Official Music Video 2024",
        " Exclusive music video 4K ",
        "OFFICIAL MUSIC VIDEO ||",
        "| Official Music Video |",
        "OFFICIAL MUSIC VIDEO",
        "Official Music Video",
        "official music video",
        "OFFICIAL MUSIC AUDIO",
        "Official Music Audio",
        "official music audio",
        "OFFICIAL PREMIERE VIDEO",
        "Official Premiere Video",
        "official premiere video",
        "Official Visual Art Video",
        "OFFICIAL LYRIC VIDEO",
        "Official Lyrics Video",
        "Official Lyric Video",
        "official lyric video",
        " - Official Video",
        "| (Official Video)",
        "OFFICIAL VIDEO",
        "Official Video 4K",
        "| Official Video",
        "Official Video",
        "(Official video) |",
        "Official video",
        "official video",
        "official Video",
        "ORIGINAL VIDEO",
        "Original Video",
        "original video",
        "OFFICIAL AUDIO",
        "Official Audio",
        "official audio",
        "| Lyric Video",
        "LYRIC VIDEO",
        "Lyrics Video",
        "Lyric Video",
        "lyric video",
        "MUSIC VIDEO",
        "Music Video",
        "music video",
        "VISUAL VIDEO",
        "Visual Video",
        "visual video",
        " VIDEO OFICIAL 4K ",
        "-VIDEO OFICIAL",
        "VIDEO OFICIAL",
        " l Video Oficial",
        "| Video Oficial",
        " Video Oficial ",
        "Video Official",
        "Video Oficial",
        "video oficial",
        "VIDEO UFFICIALE",
        "Video Ufficiale",
        "video ufficiale",
        "VIDEOCLIP OFICIAL",
        "Videoclip Oficial",
        "videoclip oficial",
        "AUDIO OFICIAL",
        "Audio Oficial",
        "audio oficial",
        "LETRA OFICIAL",
        "Letra Oficial",
        "letra oficial",
        "Video Letra/Lyrics",
        "VIDEO LYRIC",
        "Video Lyric",
        "video lyric",
        "VIDEO CLIPE OFICIAL",
        "Video Clipe Oficial",
        "video clipe oficial",
        "VIDÉOCLIP OFFICIEL",
        "Vidéoclip Officiel",
        "vidéoclip officiel",
        "VIDEOCLIP UFFICIALE",
        "Videoclip Ufficiale",
        "videoclip ufficiale",
        "CLIPE OFICIAL",
        "Clipe Oficial",
        "clipe oficial",
        "CLIP OFFICIEL",
        "Clip Officiel",
        "Clip officiel",
        "clip officiel",
        "OFFICIAL VISUALIZER",
        "Official Visualizer",
        "official visualizer",
        "OFFICIAL VISUALISER",
        "Official Visualiser",
        "official visualiser",
        "PERFORMANCE VIDEO",
        "Performance Video",
        "performance video",
        "LIVE PERFORMANCE",
        "Live Performance",
        "live performance",
        "New Unreleased Video",
        "( Cover Versión )",
        "( Full Video )",
        "[OFFICIAL MV]",
        "OFFICIAL MV",
        "Official MV",
        "OFFICIEL",
        "Official",
        "Oficial",
        "Lyrics",
        "Visualizer",
        "Video",
        "(Visual)",
        "(Letra)",
        "(Live)",
        "(En Vivo en Estadio Uno)",
        "(En Vivo En El Luna Park)",
        "(Estadio Geba)",
        " (En Vivo)",
        "| ENFASIS",
        "| CROSSOVER 3",
        "| Música Popular Con Letra",
        "|  Latest New Punjabi Song 2024",
        "| Latest Punjabi Songs 2024",
        "| Latest Punjabi Song 2024",
        "| LATEST PUNJABI SONGS 2023",
        "| Latest Punjabi song 2023",
        "| Latest Punjabi Song",
        "New Punjabi Songs 2024|",
        "New Punjabi Songs 2024 |",
        "New Punjabi Song 2024 |",
        "| New Punjabi Song 2024",
        "New Punjabi Songs 2024 -",
        "New Punjabi Song 2024",
        "| GHOST | Intense, Raj Ranjodh",
        "| New Punjabi Song",
        "| Punjabi Song 2023",
        "| SAKURA",
        "| Music Tym",
        "| Partyson",
        "| a new star (1 9 9 3)",
        "| From The Block Performance",
        "| ICON 5",
        "| ICON 6 | Preview",
        "| Prod . MB Music",
        "| GRM Daily",
        "| GRM daily",
        "l Sycostyle",
        "| 5911 Records",
        "| Sanremo 2024",
        " - Sanremo 2024",
        " – Sanremo 2024",
        "Sanremo 2024",
        "Ultra Records",
        "(Dallass e Rocco)",
        "(Ao Vivo Em Goiânia) QuestãoDeTempo",
        "Live Finale de l'Eurovision 2024 !",
        "Furious 7 Soundtrack",
        "Benidorm Fest 2024",
        "from Poppy Playtime: Chapter 3",
        "prod.Israel Amador",
        "PURPOSE : The Movement",
        "SHOT BY BELVEDERE",
        " Mxrci ",
        " Deol Harman ",
        "Juke Dock",
        "Tiktok",
        "CYRIL ",
        "श्री हनुमान चालीसा |",
        "อัลบั้มละไว้ในฐานที่เข้าใจ",
        ": พนมรุ้งเรคคอร์ด",
        "لبنج : هواسي",
        "/ ناصيف زيتون ورحمة رياض - ما في ليل",
        "/ الشامي - صبراً",
        "/ الشامي - يا ليل ويالعين",
        '/ OST "IL SEGRETO DI LIBERATO" DAL 9 MAGGIO AL CINEMA',
        " / SV",
        "(VIAJE 3)",
        " (2023)",
        " (2024)",
        "(67)",
        "Full HD",
        "HD",
        "M/V",
        "(  )",
        "()",
        "[]",
        "@",
    ]

    song_name = re.sub(r"\bMV\b", "", song_name)

    for replacement in replacements:
        song_name = song_name.replace(replacement, "")

    song_name = (
        song_name.replace(" ‘", " ")
        .replace("’ ", " ")
        .replace(" '", "  ")
        #     .replace("' ", "  ")
        .replace('"', " ")
        .replace("SDM92", "SDM")
        .replace(" l ", "  ")
    )

    return song_name


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
        "\U000024C2-\U0001F251"  # chinese char
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

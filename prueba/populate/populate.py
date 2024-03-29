from populate.models import Genre, Artist, Album, Song

from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
import re, json
from datetime import timedelta
import requests


# lineas para evitar error SSL
import os, ssl

if not os.environ.get("PYTHONHTTPSVERIFY", "") and getattr(
    ssl, "_create_unverified_context", None
):
    ssl._create_default_https_context = ssl._create_unverified_context


##################### DATA EXTRACTION #####################


def populate():
    # Delete all data
    Genre.objects.all().delete()
    Artist.objects.all().delete()
    Album.objects.all().delete()
    Song.objects.all().delete()

    # Populate
    # populate_kworb()
    # populate_megatop()
    # populate_youtube()
    # populate_soundcloud()
    # populate_amazon()
    # populate_deezer()
    # populate_los40()
    # populate_apple()
    # populate_shazam()
    # populate_epdm()

    return


def populate_kworb():

    #### KWORB - Spotify Global (Daily) ####

    # BeautifulSoup
    url = "https://kworb.net/spotify/country/global_daily.html"
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f, "lxml")

    song_links = s.find("table", class_="sortable").find("tbody").find_all("tr")

    songs = []

    for can in song_links:

        data = can.find_all("td")

        # POSITION
        position = data[0].text

        # VARIATION
        variation = data[1].text

        # NAME & ARTIST
        name_and_artist = data[2].find_all("a")

        if len(name_and_artist) == 0:
            name = "Unknown"
            artist = []
            collaborators = []
        else:
            name = name_and_artist[1].text.strip()
            artist = name_and_artist[0].text.strip()
            collaborators = [a.text.strip() for a in name_and_artist[2:]]

        """
        if name_and_artist.len() > 2:
            artist, created = Artist.objects.get_or_create(name=name_and_artist[0].text.strip())
            artists_collabs = [
                Artist.objects.get_or_create(name=a.text.strip()) for a in name_and_artist[2:]
            ]
            collaborators = [artist for artist, created in artists_collabs]
        else:
            artist, created = Artist.objects.get_or_create(name=name_and_artist[0].text.strip())
            collaborators = []
        """

        # DAYS
        days = data[3].text

        # STREAMS TODAY
        streams_today = data[6].text

        # STREAMS THIS WEEK
        streams_this_week = data[8].text

        # STREAMS TOTAL
        streams_total = data[-1].text

        songs.append(
            [
                name,
                artist,
                collaborators,
                position,
                variation,
                days,
                streams_today,
                streams_this_week,
                streams_total,
            ]
        )

    #### KWORB - Spotify most streamed artists (All times) ####

    # BeautifulSoup
    url = "https://kworb.net/spotify/artists.html"
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f, "lxml")

    artists_links = s.find("table", class_="sortable").find("tbody").find_all("tr")

    artists = []
    pos = 1

    for art in artists_links:
        data = art.find_all("td")

        # POSITION
        position = pos
        pos += 1

        # ARTIST
        artist = data[0].find("a").text

        # STREAMS
        streams_data = data[0].find("a")["href"]
        f2 = urllib.request.urlopen("https://kworb.net" + streams_data)
        s2 = BeautifulSoup(f2, "lxml")

        streams = s2.find("table").find("tbody").find_all("tr")

        # STREAMS TOTAL
        streams_total_data = streams[0].find_all("td")

        streams_total = streams_total_data[1].text
        streams_as_lead = streams_total_data[2].text
        streams_solo = streams_total_data[3].text
        streams_as_ft = streams_total_data[4].text

        # DAILY TOTAL
        daily_total_data = streams[1].find_all("td")

        daily_total = daily_total_data[1].text
        daily_as_lead = daily_total_data[2].text
        daily_solo = daily_total_data[3].text
        daily_as_ft = daily_total_data[4].text

        # TRACKS
        tracks_data = streams[2].find_all("td")

        tracks_total = tracks_data[1].text
        tracks_as_lead = tracks_data[2].text
        tracks_solo = tracks_data[3].text
        tracks_as_ft = tracks_data[4].text

        # UPDATE ARTIST
        artists.append(
            [
                artist,
                position,
                streams_total,
                streams_as_lead,
                streams_solo,
                streams_as_ft,
                daily_total,
                daily_as_lead,
                daily_solo,
                daily_as_ft,
                tracks_total,
                tracks_as_lead,
                tracks_solo,
                tracks_as_ft,
            ]
        )

    return songs, artists


def populate_megatop():

    #### MEGATOP ####
    music_list = "MegaTop"

    # BeautifulSoup
    url = "https://www.megatop.net/index.php"
    codigo = "?page=megatop50espana&UC_view=details&UC_id=14406"
    f = urllib.request.urlopen(url + codigo)
    s = BeautifulSoup(f, "lxml")

    song_links = s.find("table", class_="charts").find_all("tr")
    print(song_links)
    return song_links


def populate_youtube():

    #### YOUTUBE MUSIC ####
    music_list = "Youtube Music"

    # BeautifulSoup
    url = "https://music.youtube.com/playlist"
    codigo = "?list=OLAK5uy_mzYnlaHgFOvLaxqIPnnouEr-idiUn4NIM"
    f = urllib.request.urlopen(url + codigo)
    s = BeautifulSoup(f, "lxml")

    song_links = s.find("body")
    print(song_links)
    return song_links


def populate_soundcloud():

    #### SOUNDCLOUD ####
    music_list = "SoundCloud"

    # BeautifulSoup
    url = "https://soundcloud.com/iceblade_music/sets/top-50-espana"
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f, "lxml")

    song_links = s.find("div", id="app")
    print(song_links)
    return song_links


def populate_amazon():

    #### AMAZON MUSIC ####
    music_list = "Amazon Music"

    # BeautifulSoup
    url = "https://music.amazon.es/playlists"
    codigo = "/B073PW84YH"
    f = urllib.request.urlopen(url + codigo)
    s = BeautifulSoup(f, "lxml")

    song_links = s.find("div", id="container")
    print(song_links)
    return True


def populate_deezer():

    #### DEEZER ####
    music_list = "Deezer"

    # BeautifulSoup
    url = "https://www.deezer.com/es/playlist"
    codigo = "/1116190041"
    f = urllib.request.urlopen(url + codigo)
    s = BeautifulSoup(f, "lxml")

    song_links = s.find("body").find("div", id="dzr-app").find("script").string
    songs = song_links.split(" = ")[1]
    songs_list = json.loads(songs)["SONGS"]["data"]

    pos = 1

    for song in songs_list:

        # NAME -> SNG_TITLE
        name = song["SNG_TITLE"]

        # ARTIST & COLABORATORS INFO -> ART_NAME, ARTISTS, ART_PICTURE
        artist_name = song["ART_NAME"]
        artist, created = Artist.objects.get_or_create(name=artist_name)

        collaborators = []
        for a in song["ARTISTS"]:
            colab_name = a["ART_NAME"]
            if colab_name != artist_name:
                colab, created = Artist.objects.get_or_create(name=colab_name)
                collaborators.append(colab)

        # ALBUM -> ALB_TITLE, ALB_PICTURE
        album_name = song["ALB_TITLE"]
        album, created = Album.objects.get_or_create(name=album_name, artist=artist)

        # DURATION -> DURATION
        seconds = song["DURATION"]
        duration = timedelta(seconds=int(seconds))

        # LYRICS -> LYRICS_ID
        # MEDIA -> HREF (url a un trozo de la cancion)

        # Update or create the song
        song, created = Song.objects.update_or_create(
            name=name,
            duration=duration,
            artist=artist,
            album=album,
        )

        # Update the position field
        if song.position:
            song.position[music_list] = pos
        else:
            song.position = {music_list: pos}

        artist.save()
        album.save()
        song.save()

        song.collaborators.add(*collaborators)
        pos += 1

    return True


def populate_apple():

    #### APPLE MUSIC ####
    music_list = "Apple music"

    # BeautifulSoup
    url = "https://music.apple.com/es/playlist/top-100-españa"
    codigo = "/pl.0d656d7feae64198bc5fb1b02786ed75"
    url_encoded = quote(
        url + codigo, safe=":/"
    )  # To solve the ASCII problem we change it to UTF-8
    f = urllib.request.urlopen(url_encoded)
    s = BeautifulSoup(f, "lxml")

    song_links = s.find("main").find_all("div", class_="section svelte-gla0uw")
    songs = (
        song_links[1]
        .find("div", class_="placeholder-table")
        .find("div", class_="placeholder-row")
    )
    print(songs)

    return True


def populate_shazam():

    #### SHAZAM ####
    music_list = "Shazam"

    # BeautifulSoup
    url = "https://www.shazam.com/es/charts/top-200/spain"
    list_url = "/charts/top-200/spain"
    f = urllib.request.urlopen(url + list_url)
    s = BeautifulSoup(f, "lxml")

    song_links = s.find_all("main")
    print(song_links)

    return True


def populate_los40():

    #### LOS 40 PRINCIPALES ####
    music_list = "Los 40 Principales"

    # BeautifulSoup
    url = "https://los40.com/lista40/"
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f, "lxml")

    links_canciones = s.find("ul", class_="lst-can").find_all("li", id=True)

    for can in links_canciones:
        data = can.find("div", class_="c-ele")
        extra = can.find("div", class_="dat-des")

        # POSITION
        pos = can.find("div", class_="pos").find("p").string.strip()
        position = {music_list: pos}

        # ARTIST
        artist_info = data.find("div").find("span").text.strip()
        artist_replaced = (
            artist_info.replace("&", "/")
            .replace("feat.", "/")
            .replace("ft.", "/")
            .replace(",", "/")
        )

        if artist_replaced.__contains__("/"):
            artists = artist_replaced.split("/")
            artist, created = Artist.objects.get_or_create(name=artists[0].strip())
            artists_collabs = [
                Artist.objects.get_or_create(name=a.strip()) for a in artists[1:]
            ]
            collaborators = [artist for artist, created in artists_collabs]
        else:
            artist, created = Artist.objects.get_or_create(name=artist_replaced)
            collaborators = []

        # NAME
        n1 = data.find("div").find("p").text.strip()
        name = n1.replace(artist_info, "").strip()

        # IMAGE
        image = data.find("img")["src"].strip()

        # VIDEO
        try:
            video = extra.find("iframe")["src"].strip()
        except:
            video = ""

        # Update or create the song
        song, created = Song.objects.update_or_create(
            name=name,
            image=image,
            video=video,
            artist=artist,
        )

        # Update the position field
        if song.position:
            song.position[music_list] = pos
        else:
            song.position = {music_list: pos}

        artist.save()
        song.save()

        # Add the collaborators
        song.collaborators.add(*collaborators)

    return True


def populate_epdm():

    #### EL PORTAL DE LA MUSICA ####
    music_list = "El portal de la musica"

    # BeautifulSoup
    url = "https://www.elportaldemusica.es"
    lists = "/lists/top-100-canciones/2024"
    semana = "/6"
    f = urllib.request.urlopen(url + lists + semana)
    s = BeautifulSoup(f, "lxml")

    song_links = s.find("div", id="w1", class_="list-view").find_all(
        "div", class_="item"
    )

    for song in song_links:

        # Extracting data from the song
        song_data = song.find("a")["href"]
        f = urllib.request.urlopen(url + song_data)
        s = BeautifulSoup(f, "lxml")

        # NAME
        name = s.find("div", class_="name").text.strip()

        # Capitalize the artist's name
        words = name.split(" ")
        name = ""
        for word in words:
            name += word.capitalize() + " "
        name = name.strip()

        # POSITION
        pos = s.find("p", class_="single-list-entry-rank-position").text.strip()
        position = {music_list: pos}

        # IMAGE
        image = s.find("div", class_="lazy img-cover")["data-bg"].strip()

        # GENRE
        genre = s.find("div", class_="section-genre").text.strip()
        genre, created = Genre.objects.get_or_create(name=genre)

        # ARTIST & COLLABORATORS
        artist_info = s.find("div", class_="subname").find("a").text.strip()
        artist_info = (
            artist_info.replace("y", "/")
            .replace("&", "/")
            .replace("feat.", "/")
            .replace("ft.", "/")
            .replace("Junto a", "/")
            .replace(",", "/")
        )

        if artist_info.__contains__("/"):
            artists = artist_info.split("/")

            # Capitalize the artist's name
            artists_cap = []
            for artist in artists:
                words = artist.split(" ")
                artist = ""
                for word in words:
                    artist += word.capitalize() + " "
                artist = artist.strip()
                artists_cap.append(artist)

            artist, created = Artist.objects.get_or_create(name=artists_cap[0].strip())
            artists_collabs = [
                Artist.objects.get_or_create(name=a.strip()) for a in artists_cap[1:]
            ]
            collaborators = [artist for artist, created in artists_collabs]
        else:
            # Capitalize the artist's name
            words = artist_info.split(" ")
            artist = ""
            for word in words:
                artist += word.capitalize() + " "
            artist = artist.strip()

            artist, created = Artist.objects.get_or_create(name=artist)
            collaborators = []

        # COMPANY
        company = s.find("div", class_="detail_one").text.strip()
        artist.company = company

        # Update or create the song
        song, created = Song.objects.update_or_create(
            name=name,
            image=image,
            artist=artist,
        )

        # Update the position field
        if song.position:
            song.position[music_list] = pos
        else:
            song.position = {music_list: pos}

        artist.save()
        song.save()

        # Add the genre and the collaborators
        song.genre.add(genre)
        song.collaborators.add(*collaborators)

    return True

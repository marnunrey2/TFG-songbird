from populate.models import Genre, Artist, Album, Song

from bs4 import BeautifulSoup
import urllib.request


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
    # populate_megatop()
    # populate_los40()
    # populate_epdm()

    return


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

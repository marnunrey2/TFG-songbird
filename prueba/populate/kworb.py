from bs4 import BeautifulSoup
import urllib.request

BASE_URL = "https://kworb.net"


def kworb_scrapping():

    # BeautifulSoup
    url = f"{BASE_URL}/charts/"
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f, "lxml")

    song_links = s.find("table", class_="sortable")

    headers = song_links.find("thead").find_all("th")
    content = song_links.find("tbody").find_all("tr")

    songs = {header.text: set() for header in headers if header.text != "Country"}

    for cont in content:
        tds = cont.find_all("td")

        country = tds[0].text
        itunes_songs = get_songs(tds[1].find("a")["href"]) if tds[1].find("a") else []
        spotify_songs = get_songs(tds[2].find("a")["href"]) if tds[2].find("a") else []
        apple_music_songs = (
            get_songs(tds[3].find("a")["href"]) if tds[3].find("a") else []
        )
        youtube_songs = get_songs(tds[4].find("a")["href"]) if tds[4].find("a") else []
        shazam_songs = get_songs(tds[5].find("a")["href"]) if tds[5].find("a") else []
        deezer_songs = get_songs(tds[6].find("a")["href"]) if tds[6].find("a") else []

        songs["iTunes"].add(song for song in itunes_songs)
        songs["Spotify"].add(song for song in spotify_songs)
        songs["Apple Music"].add(song for song in apple_music_songs)
        songs["YouTube"].add(song for song in youtube_songs)
        songs["Shazam"].add(song for song in shazam_songs)
        songs["Deezer"].add(song for song in deezer_songs)

    return songs


def get_songs(href):

    # BeautifulSoup
    url = f"{BASE_URL}{href}"
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f, "lxml")

    try:
        content = s.find("table", class_="sortable").find("tbody").find_all("tr")
    except:
        return []

    songs = []

    for cont in content:
        tds = cont.find_all("td")

        if len(tds) < 3:
            song = tds[-1].text
        else:
            song = tds[2].text

        songs.append(song)

    return songs

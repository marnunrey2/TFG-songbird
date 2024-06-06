from bs4 import BeautifulSoup
import urllib.request

url = "https://www.last.fm/es/charts"
f = urllib.request.urlopen(url)
s = BeautifulSoup(f, "lxml")

song_links = (
    s.find("section", class_="charts")
    .find("table", class_="globalchart")
    .find("tbody")
    .find_all("tr")
)

for song in song_links:
    name = song.find("td", class_="globalchart-name").find("a").text.strip()
    print(name)

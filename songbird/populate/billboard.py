from bs4 import BeautifulSoup
import urllib.request


def billboard():

    # BeautifulSoup
    url = f"https://www.billboard.com/charts/hot-100/"
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f, "lxml")

    song_links = s.find("div", class_="chart-results-list").find_all(
        "div", class_="o-chart-results-list-row-container"
    )
    print(song_links)


billboard()

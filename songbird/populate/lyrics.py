from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver


def get_lyrics(song_name, artist_name):
    # Step 3
    search_query = f"{song_name} {artist_name}".replace(" ", "%20")

    # Initialize the Chrome driver
    driver = webdriver.Edge(r"C:\Users\W10\Downloads\edgedriver_win32\msedgedriver.exe")

    # BeautifulSoup
    url = f"https://genius.com/search?q={search_query}"
    driver.get(url)
    s = BeautifulSoup(driver.page_source, "lxml")

    print(s)

    # Step 6
    song_url = s.find("div", class_="u-quarter_vertical_margins u-clickable")
    print(song_url)

    # Open the song URL
    driver.get(song_url)

    # Step 8
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Step 9
    lyrics_div = soup.find("div", {"data-lyrics-container": "true"})
    print(lyrics_div.text)

    # Close the driver
    driver.quit()


# Example usage:
get_lyrics("LA RONDA", "myke towers")

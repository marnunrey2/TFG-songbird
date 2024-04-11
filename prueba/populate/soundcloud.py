# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup


# def soundcloud_scrapping():
#     #### SOUNDCLOUD ####
#     music_list = "SoundCloud"

#     # Selenium
#     url = "https://soundcloud.com/trending-music-ibe/sets/pop"
#     driver = webdriver.Firefox()  # or webdriver.Chrome() if you have Chrome
#     driver.get(url)

#     # Wait for the JavaScript to load the content
#     wait = WebDriverWait(driver, 50)  # wait up to 10 seconds
#     wait.until(
#         EC.presence_of_element_located((By.ID, "app"))
#     )  # Wait for the app container to load

#     # BeautifulSoup
#     s = BeautifulSoup(driver.page_source, "lxml")

#     # Find song links
#     song_links = s.find("div", class_="l-container l-content")

#     print(song_links)

#     driver.quit()  # don't forget to quit the driver

#     return song_links

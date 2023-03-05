import os
import time
import csv
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from helpers import scrape
from helpers import checkDuplicate
from helpers import spotifyToken
from helpers import get_spotify_uri


options = Options()
options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")
driver = Chrome(options=options)


titleBlacklist = ["Bossa Jazz Brasil", "Bossa Jazz"]
albumBlacklist = ["BJB"]

SOURCE_URL = os.getenv('SOURCE_URL')
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/api/token'

# Opening the CSV File Handle
csv_file = open('playlist.csv', 'a')

# Create the csv writer
writer = csv.writer(csv_file)

driver.get(SOURCE_URL)

# Delay to load the contents of the HTML FIle
time.sleep(2)

# Parse processed webpage with BeautifulSoup
soup = BeautifulSoup(driver.page_source, features="html.parser")

# get spotify access token
spotifyAuthToken = spotifyToken(SPOTIFY_AUTH_URL, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)


# scrape content
titles = scrape("cctitle")
artists = scrape("ccartist")
albums = scrape("ccalbum")

for (title, artist, album) in zip(titles, artists, albums):
    if (title not in titleBlacklist) and (album not in albumBlacklist):
         if checkDuplicate(title, artist):
            spotifyTrackUrl = get_spotify_uri(spotifyAuthToken, title, artist)
            print("Adding song:")
            print("title:  {}".format(title))
            print("artist: {}".format(artist))
            print("album:  {}".format(album))
            print("spotify url: {}".format(spotifyTrackUrl))
            writer.writerow([title, artist, album, spotifyTrackUrl])
    else:
        print("*** match blacklist ***")
        print("title:  {}".format(title))
        print("artist: {}".format(artist))
        print("album:  {}".format(album))
    
    print("--------------------------------------------------------")

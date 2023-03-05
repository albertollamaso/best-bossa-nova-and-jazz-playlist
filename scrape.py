import os
import time
import csv
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

def scrape(findClass):
    list = []

    content = soup.find_all(class_=findClass)
    for element in content:
        list.append(element.string)
    
    return list

def checkDuplicate(title, artist):
    df = pd.read_csv('playlist.csv', delimiter=',')
    tuples = [tuple(x) for x in df.values]
    for t in tuples:
        if (title == t[0] and artist == t[1]):
            print("this song already exists in list")
            print("song: {}".format(t[0]))
            print("artist: {}".format(t[1]))
            return False
    
    return True

options = Options()
options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")
driver = Chrome(chrome_options=options)


blacklist = ["Bossa Jazz Brasil", "Bossa Jazz"]

# Opening the CSV File Handle
csv_file = open('playlist.csv', 'a')

# Create the csv writer
writer = csv.writer(csv_file)

url = os.environ.get('URL')

driver.get(url)

# Delay to load the contents of the HTML FIle
time.sleep(2)

# Parse processed webpage with BeautifulSoup
soup = BeautifulSoup(driver.page_source, features="html.parser")



# scrape content
titles = scrape("cctitle")
artists = scrape("ccartist")
albums = scrape("ccalbum")

for (title, artist, album) in zip(titles, artists, albums):
    if title not in blacklist:
         if checkDuplicate(title, artist):
            print("Adding song:")
            writer.writerow([title,artist,album])
            print("title:  {}".format(title))
            print("artist: {}".format(artist))
            print("album:  {}".format(album))
            print("--------------------------------------------------------")

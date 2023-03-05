import os
import filecmp
from mdtable import MDTable

markdown = MDTable('playlist.csv')
markdown_string_table = markdown.get_table()
markdown.save_table('table.md')

init_readme = """# Best Bossa Nova and Jazz Playlist

This project is a web scraper that monitors a public online radio station's playlist and searches for the corresponding versions of the songs played on Spotify.
The scraped data is automatically update to the README.

## Features

- Web scraping of the radio station's playlist in real-time using BeautifulSoup and requests libraries
- Searching for the corresponding tracks on Spotify using the Spotify Web API
- Storing the scraped data in a CSV file and the README of this repository
- [TODO] Automatic creation and updating of a Spotify playlist with the corresponding tracks

## Usage

The github action runs every 5 minutes and it will monitor the radio station's playlist in real-time and search for the corresponding tracks on Spotify.

## Contributing

Contributions are welcome! Feel free to open an issue or pull request with your ideas or bug fixes.

## License

This project is licensed under the Apache License. See the `LICENSE` file for details.


"""

if not filecmp.cmp('README.md', 'table.md'):
    # update readme with new songs
    table_file = open('table.md', 'r')
    tmp_file = open('tmp.md', 'a')
    tmp_file.write(init_readme)
    tmp_file.write(table_file.read())

    tmp_file.close()
    table_file.close()
    
    os.remove('README.md')
    os.rename('tmp.md', 'README.md')


# clean out
os.remove("table.md")

import os
import filecmp
from mdtable import MDTable

markdown = MDTable('playlist.csv')
markdown_string_table = markdown.get_table()
markdown.save_table('table.md')

if not filecmp.cmp('README.md', 'table.md'):
    # update readme with new songs
    table_file = open('table.md', 'r')
    tmp_file = open('tmp.md', 'a')

    tmp_file.write('# Best Bossa Nova and Jazz Playlist')
    tmp_file.write('\n\n')
    tmp_file.write(table_file.read())

    tmp_file.close()
    table_file.close()
    
    os.remove('README.md')
    os.rename('tmp.md', 'README.md')


# clean out
os.remove("table.md")

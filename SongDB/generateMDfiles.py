import os
from SongDB import SongDatabase
from AddSongGUI import get_table_headers, get_songs_table_rows, get_event_listeners

current_file_path = os.path.abspath(__file__)
current_file_directory = os.path.dirname(current_file_path)

db = SongDatabase()
result = db.fetch_all_songs_with_attribute('difficulty', 'Expert+')
print('result from generate files file:\n\n')

for song in result:
    print(song.to_dict())

print('\n\n\n\n')
unique = db.fetch_all_unique_in_attribute('genre')
print(unique)
print('\n\n\n')


def make_front_page():
    output_string = '''---
layout: default
title: Beat Saber
nav_order: 1
has_children: true
---

```json:table
{
    "fields" : [
        {"key": "a", "label": "AA", "sortable": true},
        {"key": "b", "label": "BB"},
        {"key": "c", "label": "CC"}
    ],
    "items" : [
      {"a": "11", "b": "22", "c": "33"},
      {"a": "211", "b": "222", "c": "233"}
    ]
}
'''
    return output_string


def generate_all_files():

    # Delete everything in it
    bs_path = current_file_directory.replace('SongDB', 'BeatSaber')
    [os.remove(os.path.join(bs_path, f)) for f in os.listdir(bs_path)]
    with open(f'{bs_path}/BeatSaber.md', 'w') as mdDoc:
        mdDoc.write(make_front_page())


generate_all_files()

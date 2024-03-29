import json
import os
import re
from SongDB import SongDatabase
from Song import get_attributes_and_names

current_file_path = os.path.abspath(__file__)
current_file_directory = os.path.dirname(current_file_path)
bs_path = current_file_directory.replace('SongDB', 'BeatSaber')

db = SongDatabase()


def make_front_page():
    output_string = '''---
layout: default
title: Beat Saber
nav_order: 1
has_children: true
---

|'''
    attrs_and_names = get_attributes_and_names()
    for attr in attrs_and_names:
        name = attrs_and_names[attr]
        output_string += f'{name} |'

    output_string += f'''
    |'''

    for attr in attrs_and_names:
        output_string += f'--- |'

    output_string += f'''
    |'''

    all_songs = db.fetch_all_songs()
    for song in all_songs:
        for attr in attrs_and_names:
            val = song.to_dict()[attr]
            output_string += f'{val} |'
        output_string += f'''
    |'''
    return output_string


def make_one_song(song, parent, nav_order):
    filename = parent + song[0]['title'] + song[0]['artist']
    filename = re.sub(r'[^\w]', '', filename)
    output_string = f'''---
layout: default
title: {song[0]['title']}
parent: {parent}
grand_parent: Beat Saber
nav_order: {nav_order + 1}
has_children: false
---

## {song[0]['title']} - {song[0]['artist']}
- **Genre**: {song[0]['genre']}
- **Vibe**: {song[0]['vibe']}
- **Tolerability**: {song[0]['tolerability']}

'''
    for play in song:
        output_string += f'''
### {play['difficulty']} ({play['date_recorded']})

<iframe width="560" height="315" src="https://www.youtube.com/embed/{play['youtube_id']}?si=kK4lrMARYXlzzrIM" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

'''
    with open(f'{bs_path}/{filename}.md', 'w') as mdDoc:
        mdDoc.write(output_string)
        mdDoc.close()


def make_all_songs():
    output_string = '''---
layout: default
title: All Songs
parent: Beat Saber
nav_order: 1
has_children: true
---

'''
    grouped_songs = db.fetch_all_songs_grouped()

    for idx, song in enumerate(grouped_songs):
        one_song = song[0]
        output_string += f'''
## {one_song['title']} - {one_song['artist']}

### {one_song['difficulty']} ({one_song['date_recorded']})

<iframe width="560" height="315" src="https://www.youtube.com/embed/{one_song['youtube_id']}?si=kK4lrMARYXlzzrIM" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

'''
        make_one_song(song, "All Songs", idx)
    return output_string


def make_all_attribute_sorted():
    attributes_and_names = get_attributes_and_names()
    for attribute in attributes_and_names:
        attrName = attributes_and_names[attribute]
        output_string = f'''---
layout: default
title: {attrName}
parent: Beat Saber
nav_order: 1
has_children: true
---

'''
        uniques = db.fetch_all_unique_in_attribute(attribute)
        for unique in uniques:
            output_string += f'''## {unique}
'''
            songsHere = db.fetch_all_songs_with_attribute(attribute, unique)
            for idx, song in enumerate(songsHere):
                song = song.to_dict()
                make_one_song([song], attrName, idx + 1)
                output_string += f'''
### {song['title']} - {song['artist']}

#### {song['difficulty']} ({song['date_recorded']})

<iframe width="560" height="315" src="https://www.youtube.com/embed/{song['youtube_id']}?si=kK4lrMARYXlzzrIM" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

'''
    with open(f'{bs_path}/{attrName}.md', 'w') as mdFile:
        mdFile.write(output_string)
        mdFile.close()


def generate_all_files():
    # Delete everything in it
    [os.remove(os.path.join(bs_path, f)) for f in os.listdir(bs_path)]
    with open(f'{bs_path}/BeatSaber.md', 'w') as mdDoc:
        mdDoc.write(make_front_page())
        mdDoc.close()

    all_songs_string = make_all_songs()
    with open(f'{bs_path}/AllSongs.md', 'w') as mdDoc:
        mdDoc.write(all_songs_string)
        mdDoc.close()

    # make_all_attribute_sorted()


generate_all_files()

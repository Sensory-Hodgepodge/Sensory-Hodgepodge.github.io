import os
from SongDB import SongDatabase
from Song import get_attributes_and_names

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
    return output_string


def generate_all_files():

    # Delete everything in it
    bs_path = current_file_directory.replace('SongDB', 'BeatSaber')
    [os.remove(os.path.join(bs_path, f)) for f in os.listdir(bs_path)]
    with open(f'{bs_path}/BeatSaber.md', 'w') as mdDoc:
        mdDoc.write(make_front_page())


generate_all_files()

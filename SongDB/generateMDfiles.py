import os
from SongDB import SongDatabase
from AddSongGUI import get_table_headers, get_songs_table_rows

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
    output_string = '''
---
layout: default
title: Beat Saber
nav_order: 1
has_children: true
---
<html>
<head>
<style>
  body {
    font-family: Arial, sans-serif;
  }
  .sortable-table {
    border-collapse: collapse;
    width: 100%;
    margin-top: 20px;
  }
  .sortable-table th, .sortable-table td {
    border: 1px solid #ddd;
    text-align: left;
    padding: 8px;
  }
  .sortable-table th {
    background-color: #f2f2f2;
    
  }
  .sortable-table th:hover {
    background-color: #e1e1e1;
    cursor: default;
  }
  .sortable-table tr:nth-child(even) {
    background-color: #f9f9f9;
  }
  .sortable-table tr:hover {
  background-color: #e1e1e1;
  cursor: alias;
}
    .searchresult-container {
        display: flex;
        padding: 5px 6px 5px 0px;
        width: 100%;
        gap: 1rem;
        align-items: center;
        border-radius: 1rem;
    }
    .searchresult-container:hover {
    background-color: #e1e1e1;
    cursor: w-resize;
    }
    .searchresult-text {
        font-weight: 600;
    }
    </style>
    </head>
<body>
<table class="sortable-table">
<thead>
  <tr>
    ''' + get_table_headers() + '''
  </tr>
  </thead>
  <tbody>
''' + get_songs_table_rows() + '''
  </tbody>
</table> 
</body>

    '''
    return output_string


def generate_all_files():

    # Delete everything in it
    bs_path = current_file_directory.replace('SongDB', 'BeatSaber')
    [os.remove(os.path.join(bs_path, f)) for f in os.listdir(bs_path)]
    with open(f'{bs_path}/BeatSaber.md', 'w') as mdDoc:
        mdDoc.write(make_front_page())


generate_all_files()

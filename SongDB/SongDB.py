from tinydb import TinyDB, Query
from Song import Song
import os

current_file_path = os.path.abspath(__file__)
current_file_directory = os.path.dirname(current_file_path)


class SongDatabase:
    def __init__(self, db_path=f'{current_file_directory}/db/songs.json'):
        self.db = TinyDB(db_path)
        self.query = Query()

    def add_or_update_song(self, new_song):
        existing_song = Query()
        existing_song = self.db.search(
            (existing_song.title == new_song.title) & (existing_song.artist == new_song.artist) & (existing_song.date_recorded == new_song.date_recorded))

        if existing_song:
            self.db.update(new_song.to_dict(), doc_ids=[
                           existing_song[0].doc_id])
        else:
            self.db.insert(new_song.to_dict())

    def find_song_by_title_and_artist(self, title, artist):
        song = Query()
        result = self.db.search((song.title == title) &
                                (song.artist == artist))
        print('DB: Query: ')
        print(result)
        return [Song(**record) for record in result]

    def fetch_all_songs_with_attribute(self, attribute_name, attribute_value):
        song = Query()
        result = self.db.search(
            getattr(song, attribute_name) == attribute_value)
        print('DB Query:')
        print(result)
        return [Song(**record) for record in result]

    def fetch_all_unique_in_attribute(self, attribute):
        all = self.db.all()
        unique = []
        for song in all:
            song_dict = Song(**song).to_dict()
            if song_dict[attribute] not in unique:
                unique.append(song_dict[attribute])
        return unique

    def fetch_all_songs(self):
        all = self.db.all()
        return [Song(**song) for song in all]

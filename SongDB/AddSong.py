from Song import Song
from SongDB import SongDatabase
from datetime import datetime

new_song = Song(
    title='Example Song',
    artist='Example artist',
    date_recorded=datetime.now().strftime('%Y-%m-%d'),
    spotify_link='https://spotify.com/example AGAIN',
    youtube_link='https://youtube.com/example',
    difficulty='Medium',
    tolerability='High',
    vibe='Chill'
)


db = SongDatabase()
db.add_or_update_song(new_song)

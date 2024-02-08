class Song:
    def __init__(self, title, artist, date_recorded, spotify_link, youtube_link, difficulty, tolerability, vibe):
        self.title = title
        self.artist = artist
        self.date_recorded = date_recorded
        self.spotify_link = spotify_link
        self.youtube_link = youtube_link
        self.difficulty = difficulty
        self.tolerability = tolerability
        self.vibe = vibe

    def to_dict(self):
        return {
            'title': self.title,
            'artist': self.artist,
            'date_recorded': self.date_recorded,
            'spotify_link': self.spotify_link,
            'youtube_link': self.youtube_link,
            'difficulty': self.difficulty,
            'tolerability': self.tolerability,
            'vibe': self.vibe
        }

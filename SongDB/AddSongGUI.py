from flask import Flask, request, render_template_string
from Song import Song
from SongDB import SongDatabase

app = Flask(__name__)

# HTML template for the input form and song list
HTML_TEMPLATE = '''
<!doctype html>
<html>
<head>
    <title>Add and List Songs</title>
</head>
<body>
    <h2>Add a New Song</h2>
    <form method="post">
        Title: <input type="text" name="title"><br>
        artist: <input type="text" name="artist"><br>
        Date Recorded: <input type="text" name="date_recorded"><br>
        Spotify Link: <input type="text" name="spotify_link"><br>
        Youtube Link: <input type="text" name="youtube_link"><br>
        Difficulty: <input type="text" name="difficulty"><br>
        Tolerability: <input type="text" name="tolerability"><br>
        Vibe: <input type="text" name="vibe"><br>
        <input type="submit" value="Submit">
    </form>

    <h2>Song List</h2>
     <table>
  <tr>
    <th>Title</th>
    <th>Artist</th>
    <th>Date recorded</th>
    <th>Spotify link</th>
    <th>YouTube embed link</th>
    <th>Difficulty</th>
    <th>Tolerability</th>
    <th>Vibe</th>
    <th>Source</th>
  </tr>
  <tr>
    <td>Alfreds Futterkiste</td>
    <td>Maria Anders</td>
    <td>Germany</td>
  </tr>
  <tr>
    <td>Centro comercial Moctezuma</td>
    <td>Francisco Chang</td>
    <td>Mexico</td>
  </tr>
</table> 
    {% if songs %}
        <ul>
        {% for song in songs %}
            <li>{{ song['title'] }} by {{ song['artist'] }} - Difficulty: {{ song['difficulty'] }}, Vibe: {{ song['vibe'] }}</li>
        {% endfor %}
        </ul>
    {% else %}
        <p>No songs found.</p>
    {% endif %}
</body>
</html>
'''


@app.route('/', methods=['GET', 'POST'])
def add_song():
    db = SongDatabase()  # Initialize the database connection

    if request.method == 'POST':
        # Extract form data
        song_data = {
            'title': request.form['title'],
            'artist': request.form['artist'],
            'date_recorded': request.form['date_recorded'],
            'spotify_link': request.form['spotify_link'],
            'youtube_link': request.form['youtube_link'],
            'difficulty': request.form['difficulty'],
            'tolerability': request.form['tolerability'],
            'vibe': request.form['vibe'],
        }

        # Create a new Song instance and add it to the database
        new_song = Song(**song_data)
        db.add_or_update_song(new_song)

    # Fetch all songs from the database
    songs = db.fetch_all_songs()  # Assuming you have implemented this method in SongDB.py
    return render_template_string(HTML_TEMPLATE, songs=songs)


if __name__ == '__main__':
    app.run(debug=True)

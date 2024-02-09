import os
from flask import Flask, request, render_template_string
from Song import Song, get_attributes_and_names
from SongDB import SongDatabase
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()


def get_datalists():
    db = SongDatabase()
    songs = db.fetch_all_songs()
    lists = {"difficulty": {}, "tolerability": {},
             "vibe": {}, "source": {}, "genre": {}}
    for song_obj in songs:
        song = song_obj.to_dict()
        for attribute in song:
            if str(attribute) in lists:
                lists[str(attribute)][song[attribute]] = song[attribute]
    output_string = ""
    print("lists:")
    print(lists)
    for list in lists:
        print("legger til i liste: ", str(list))
        output_string = output_string + f'''
        <datalist id="{str(list)}Datalist">
        '''
        for opts in lists[list]:
            print("følgende valg: ", str(opts))
            output_string = output_string + f'''
                <option value="{str(opts)}">
            '''
        output_string = output_string + f'''
        </datalist>
        '''
    return output_string


def get_form_elements():
    output_string = ""
    attributes = get_attributes_and_names()
    for attribute in attributes:
        output_string = output_string + f'''<div style="width: 25rem; display: flex; justify-content: space-between; padding: 0.25rem;"><label for="{attribute}" style="align-text: right">{attributes[attribute]}:</label>
        '''
        if "date" in f'{attribute}':
            output_string = output_string + f'''
            <input type="date" name="{attribute}" name="{attribute}" id="{attribute}" style="width: 12rem">
            '''
        else:
            output_string = output_string + f'''
            <input style="width: 12rem" type="text" name="{attribute}" id="{attribute}" list="{attribute}Datalist" autocomplete="off">
            '''
        output_string = output_string + '</div>'
    return output_string


def get_table_headers():
    output_string = ""
    attributes = get_attributes_and_names()
    for idx, attribute in enumerate(attributes):
        print(attribute, attributes[attribute])
        output_string = output_string + f'''
            <th onClick="sortTable({idx})">{attributes[f'{attribute}']}</th>
            '''
    return output_string


def get_songs_table_rows():
    db = SongDatabase()
    songs = db.fetch_all_songs()
    attributes = get_attributes_and_names()
    html_string = ""
    for song in songs:
        html_string = html_string + '''
        <tr>
        '''
        for attribute in attributes:
            html_string = html_string + f'''
            <td>
                {song.to_dict()[f'{attribute}']}
            </td>
            '''
        html_string = html_string + '''
        </tr>
        '''
    return html_string


def get_event_listeners():
    output_string = ""
    attributes = get_attributes_and_names()
    for idx, attribute in enumerate(attributes):
        output_string = output_string + f'''
        document.getElementById("{f'{attribute}'}").value = this.cells[{f'{idx}'}].innerText;
        '''
    return output_string

# HTML template for the input form and song list


def HTML_TEMPLATE():
    template = '''
<!doctype html>
<html>
<head>
    <title>Add and List Songs</title>
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
    .album-cover {
    border-radius: 1rem;
    width: 64px;
    height: 64px;
    object-fit: cover;
    }
    .hidden {
        display: none !important;
    }
.loading {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .loading-spinner {
    border: 8px solid #f3f3f3;
    border-top: 8px solid #3498db;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
</style>
</head>
<body>
''' + get_datalists() + '''
    <h2>Add a New Song</h2>
    <div style="display: flex;">
    <form method="post" >
        ''' + get_form_elements() + f'''
        <input type="submit" value="Submit">
    </form>
    <div style="padding: 0.25rem; margin-left: 5rem; width: 20rem;">
    <input type="text" id="searchBox" style="width: 100%" placeholder="Search for song">
    <div id="searchresult-container-parent" style="width: 100%">
    <div class="loading hidden" id="loading">
        <div class="loading-spinner"></div>
    </div>
    {''.join(f"""
    <div class="searchresult-container hidden" id="searchresult-container{i}" onclick=>
        <img src="" class="album-cover" id="searchresult-img-{i}"  alt="album{i}" />
        <p id="searchresult-text-{i}" class="searchresult-text">DragonForce, Noen Andre - With The Power of the Saber Blade</p>
        <p id="result-{i}-title" class="hidden"></p>
        <p id="result-{i}-artist" class="hidden"></p>
        <p id="result-{i}-genius_id" class="hidden"></p>
        <p id="result-{i}-spotify_id" class="hidden"></p>
    </div>  
    """ for i in range(5))}
    </div>
    </div>
    </div>
    <h2>Song List</h2>
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
<script>

async function seeSongDetails(idx) {
    document.getElementById('loading').classList.remove('hidden')
    const genius_id = document.getElementById(`result-${idx}-genius_id`).textContent
    const spotify_id = document.getElementById(`result-${idx}-spotify_id`).textContent
    const title = document.getElementById(`result-${idx}-title`).textContent

    const songInfo = {}
    for (attr of ["title", "artist", "spotify_id"]) {
        songInfo[attr] = document.getElementById(`result-${idx}-${attr}`).textContent
    }

    if (genius_id) {
        const geniusUrl = 'https://genius-song-lyrics1.p.rapidapi.com/song/details/?id=' + genius_id;
        const geniusOptions = {
            method: 'GET',
            headers: {
                'X-RapidAPI-Key': ' ''' + os.getenv('API_KEY') + ''' ',
                'X-RapidAPI-Host': 'genius-song-lyrics1.p.rapidapi.com'
            }
        };

        try {
            const response = await fetch(geniusUrl, geniusOptions);
            const result = await response.json();
            console.log('genius response:', result)
            songInfo['spotify_id'] = result.song.spotify_uuid
            songInfo['genre'] = result.song.primary_tag.name
        } catch (error) {
            console.error(error);
        }
    }

    const youtubeUrl = 'https://youtube138.p.rapidapi.com/channel/search/?id=UC1Q6g3eqybbJCM0sq8b1SIg&q=' + title;
    const youtubeOptions = {
        method: 'GET',
        headers: {
            'X-RapidAPI-Key': ' ''' + os.getenv('API_KEY') + ''' ',
            'X-RapidAPI-Host': 'youtube138.p.rapidapi.com'
        }
    };

    try {
        const response = await fetch(youtubeUrl, youtubeOptions);
        const result = await response.json();

        songInfo['youtube_id'] = result.contents[0].video.videoId
        let youtube_title = result.contents[0].video.title

        var possibleValues = ["Easy", "Medium", "Hard", "Expert", "Expert+"];

        for (var i = 0; i < possibleValues.length; i++) {
            if (youtube_title.includes(possibleValues[i])) {
                songInfo['difficulty'] = possibleValues[i];
                break; 
            }
        }
    } catch (error) {
        console.error(error);
    }

    if (!songInfo['spotify_id']) {
        const url = 'https://''' + os.getenv('API_URL') + '''/search/?q=' + title + ' ' + songInfo['artist'] + '&type=tracks&offset=0&limit=1';
        const options = {
            method: 'GET',
            headers: {
                'X-RapidAPI-Key': ' ''' + os.getenv('API_KEY') + ''' ',
                'X-RapidAPI-Host': ' ''' + os.getenv('API_URL') + ''' '
            }
        };

        try {
            const response = await fetch(url, options);
            const result = await response.json();
            console.log(result.tracks.items[0].data.id);
            songInfo['spotify_id'] = result.tracks.items[0].data.id
        }
        catch (error) {
            console.log(error)
        }
    }

    for (attr of Object.keys(songInfo)) {
        document.getElementById(attr).value = songInfo[attr]
    }
    document.getElementById('loading').classList.add('hidden')

}

function sortTable(column) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.querySelector(".sortable-table");
  switching = true;
  // Set the sorting direction to ascending:
  dir = "asc";
  // Make a loop that will continue until no switching has been done:
  while (switching) {
    // Start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    // Loop through all table rows (except the first, which contains table headers):
    for (i = 1; i < (rows.length - 1); i++) {
      // Start by saying there should be no switching:
      shouldSwitch = false;
      // Get the two elements you want to compare, one from current row and one from the next:
      x = rows[i].getElementsByTagName("TD")[column];
      y = rows[i + 1].getElementsByTagName("TD")[column];
      // Check if the two rows should switch place, based on the direction, asc or desc:
      if (dir == "asc") {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch= true;
          break;
        }
      } else if (dir == "desc") {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          shouldSwitch= true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      // If a switch has been marked, make the switch and mark that a switch has been done:
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      // Each time a switch is done, increase this count by 1:
      switchcount ++;
    } else {
      // If no switching has been done AND the direction is "asc", set the direction to "desc" and run the while loop again.
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}

document.addEventListener("DOMContentLoaded", function() {
    var rows = document.querySelector(".sortable-table").rows;
    for (let i = 1; i < rows.length; i++) { // Start from 1 to skip table header
        rows[i].addEventListener("click", function() {
        ''' + get_event_listeners() + '''
        });
    }


    for (let i = 0; i < 5; i++) {
        let result = document.getElementById(`searchresult-container${i}`)
        result.addEventListener("click", function() {
            seeSongDetails(i)
        })
    }
});

function debounce(func, wait) {
    let timeout;

    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };

        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function foundStringInSong(string, song) {
    const normalizedStr = string.toLowerCase().replace(/[^a-z\s]/g, '');
    const normalizedTitle = song.title.toLowerCase().replace(/[^a-z\s]/g, '');
    const normalizedArtist = song.artist.toLowerCase().replace(/[^a-z\s]/g, '');

    return normalizedTitle.includes(normalizedStr) || normalizedArtist.includes(normalizedStr)
}

function foundStringInAllSongs(string, songs) {
    for (let song of songs) {
        if (foundStringInSong(string, song)) {
            return true
        }
    }
    return false
}

async function searchForSongs(query) {
    if (!query) return
    document.getElementById('loading').classList.remove('hidden')
    const url = 'https://genius-song-lyrics1.p.rapidapi.com/search/?q=' + query + '&per_page=5&page=1';
    const options = {
        method: 'GET',
        headers: {
            'X-RapidAPI-Key': ' ''' + os.getenv('API_KEY') + ''' ',
            'X-RapidAPI-Host': 'genius-song-lyrics1.p.rapidapi.com'
        }
    };

    try {
        const response = await fetch(url, options);
        const result = await response.json();
        
        function processSongs(songs) {
            return songs.map(song => {
                return {
                    songString: song.result.full_title,
                    albumLink: song.result.header_image_thumbnail_url,
                    title: song.result.title,
                    artist: song.result.primary_artist.name,
                    genius_id: song.result.id
                };
            });
        }

        let processedSongs = processSongs(result.hits);

        if (!foundStringInAllSongs(query, processedSongs)) {
            const SpotifyUrl = 'https://''' + os.getenv('API_URL') + '''/search/?q=' + query + '&type=tracks&offset=0&limit=5';
            const SpotifyOptions = {
                method: 'GET',
                headers: {
                    'X-RapidAPI-Key': ' ''' + os.getenv('API_KEY') + ''' ',
                    'X-RapidAPI-Host': ' ''' + os.getenv('API_URL') + ''' '
                }
            };

            try {
                const response = await fetch(SpotifyUrl, SpotifyOptions);
                const result = await response.json();

                processedSongs = result.tracks.items.map(song => {
                    const songName = song.data.name;
                    const artistNames = song.data.artists.items.map(artist => artist.profile.name).join(", ");
                    return {
                        songString: `${artistNames} - ${songName}`,
                        albumLink: song.data.albumOfTrack.coverArt.sources[0].url,
                        title: songName,
                        artist: artistNames,
                        spotify_id: song.data.id
                    };
                })
            } catch(error) {
                console.log(error)
            }
        }

        processedSongs.forEach((song, index) => {
            let {songString, albumLink} = song

            var pElement = document.getElementById(`searchresult-text-${index}`);
            pElement.textContent = songString; 

            var imgElement = document.getElementById(`searchresult-img-${index}`);
            imgElement.src = albumLink

            var parentDiv = document.getElementById(`searchresult-container${index}`);
            parentDiv.classList.remove('hidden');

            for (attr of ["title", "artist", "genius_id", "spotify_id"]) {
                if (attr in song) {
                    document.getElementById(`result-${index}-${attr}`).textContent = song[attr]
                } else {
                    document.getElementById(`result-${index}-${attr}`).textContent = ""
                }
            }
        })
    } catch (error) {
        console.error(error);
    }
    document.getElementById('loading').classList.add('hidden')
}

const debouncedSearch = debounce(searchForSongs, 500);

function handleSearchInput(event) {
            const elements = document.getElementsByClassName('searchresult-container');

            const elementsArray = Array.from(elements);

            elementsArray.forEach(element => {
                element.classList.add('hidden')
            });

            debouncedSearch(event.target.value);
        }
window.onload = function() {
    // Attach the input event listener to your textbox
    document.getElementById('searchBox').addEventListener('input', handleSearchInput);
};
</script>
</body>
</html>
'''
    return template


@app.route('/', methods=['GET', 'POST'])
def add_song():
    db = SongDatabase()  # Initialize the database connection

    if request.method == 'POST':
        # Extract form data
        attributes = get_attributes_and_names()
        song_data = {}
        for attribute in attributes:
            song_data[f'{attribute}'] = request.form[f'{attribute}']

        # Create a new Song instance and add it to the database
        new_song = Song(**song_data)
        db.add_or_update_song(new_song)

    return render_template_string(HTML_TEMPLATE())


if __name__ == '__main__':
    app.run(debug=True, port=5001)

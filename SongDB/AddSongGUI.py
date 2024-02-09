import os
from flask import Flask, request, render_template_string
from Song import Song, get_attributes_and_names
from SongDB import SongDatabase
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()


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
        elif "tolerability" in f'{attribute}':
            output_string = output_string + f'''
            <input style="width: 12rem" type="text" list="tolerabilityDatalist" id="tolerability" name="tolerability" autocomplete="off" />
            '''
        else:
            output_string = output_string + f'''
            <input style="width: 12rem" type="text" name="{attribute}" id="{attribute}">
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
<datalist id="tolerabilityDatalist">
  <option value="Faktisk bra sang">
  <option value="Ganske tolererbar">
  <option value="I grenseland">
  <option value="Er dette musikk?">
</datalist>
    <h2>Add a New Song</h2>
    <div style="display: flex;">
    <form method="post" >
        ''' + get_form_elements() + f'''
        <input type="submit" value="Submit">
    </form>
    <div style="padding: 0.25rem; margin-left: 5rem; width: 20rem;">
    <input type="text" id="searchBox" style="width: 100%" placeholder="Search spotify">
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
    for (attr of ["title", "artist", "spotify_id"]) {
        document.getElementById(attr).value = document.getElementById(`result-${idx}-${attr}`).textContent
    }
    const songName = document.getElementById(`result-${idx}-title`).textContent
    const spotify_id = document.getElementById(`result-${idx}-spotify_id`).textContent
    const genre = await getGenre(songName, spotify_id)
    document.getElementById('genre').value = genre
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
/*
async function getGenre(song) {
    async function getID(song) {
    
        let id = ""
        const url = 'https://genius-song-lyrics1.p.rapidapi.com/search/?q=' + song + '&per_page=10&page=1';
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
            return result.hits[0].result.id
        } catch (error) {
            console.error(error);
        }
    }

    async function getGenreFromID(id) {
        const url = 'https://genius-song-lyrics1.p.rapidapi.com/song/details/?id=' + id;
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
            return result.song.primary_tag.name
        } catch (error) {
            console.error(error);
        }
    }

    const id = await getID(song)
    const genre = await getGenreFromID(id)
    return genre
}
*/

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

async function searchForSongs(query) {
    if (!query) return
    document.getElementById('loading').classList.remove('hidden')
    const url = 'https://''' + os.getenv('API_URL') + '''/search/?q=' + query + '&type=tracks&offset=0&limit=5';
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
        console.log(result.tracks.items);
        
        function processSongs(songs) {
            return songs.map(song => {
                const songName = song.data.name;
                const artistNames = song.data.artists.items.map(artist => artist.profile.name).join(", ");
                return {
                    songString: `${artistNames} - ${songName}`,
                    albumLink: song.data.albumOfTrack.coverArt.sources[0].url,
                    title: songName,
                    artist: artistNames,
                    spotify_id: song.data.id
                };
            });
        }

        let processedSongs = processSongs(result.tracks.items);

        processedSongs.forEach((song, index) => {
            let {songString, albumLink} = song

            var pElement = document.getElementById(`searchresult-text-${index}`);
            pElement.textContent = songString; 

            var imgElement = document.getElementById(`searchresult-img-${index}`);
            imgElement.src = albumLink

            var parentDiv = document.getElementById(`searchresult-container${index}`);
            parentDiv.classList.remove('hidden');

            for (attr of ["title", "artist", "spotify_id"]) {
                document.getElementById(`result-${index}-${attr}`).textContent = song[attr]
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
    app.run(debug=True)

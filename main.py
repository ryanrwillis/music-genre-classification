from config import client_ID, client_secret

import re
import flask
import requests
import json
import playlist
from azlyrics import azlyrics
from urllib.parse import urlencode
from search import search_playlist
from build_dataset import build_dataset

app = flask.Flask(__name__)
app.config["DEBUG"] = True
client = client_ID
secret = client_secret
callbackAddress = 'http://localhost:5000/callback'

# defining what data to get from the user
scopes = 'user-read-private user-read-email user-read-currently-playing playlist-modify-public'

@app.route('/', methods=['GET'])
def main():
    return 'hello world'

@app.route('/login', methods=['GET'])
def login():
    options = {
        'client_id': client,
        'response_type': 'code',
        'redirect_uri': 'http://localhost:5000/callback',
        'scope': scopes
    }
    uri = 'https://accounts.spotify.com/authorize?' + urlencode(options)
    print(uri)
    return flask.redirect(uri)


@app.route('/callback', methods=['GET'])
def callback():
    code = flask.request.args.get('code')
    url = 'https://accounts.spotify.com/api/token'
    body = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://localhost:5000/callback',
        'client_id': client,
        'client_secret': secret
    }

    res = requests.post(url=url, data=body)
    token = json.loads(res.text)['access_token']


    bar = playlist.Playlist(id='37i9dQZF1E35k73659EuOH', auth_token=token)
    songs = bar.get_tracks()
    songs_short = songs[:10]

    dataset = build_dataset(
        genre_list=['rap', 'country', 'rock', 'edm', 'folk', 'christian', 'metal', 'punk'],
        token=token,
    )
    print(dataset)
    return({'set': dataset})
    # return(json.dumps(songs_short))
app.run()
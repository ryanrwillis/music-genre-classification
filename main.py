from config import client_ID, client_secret

import flask
import requests
import json
from urllib.parse import urlencode

app = flask.Flask(__name__)
app.config["DEBUG"] = True
client = client_ID
secret = client_secret
callback = 'http://localhost:5000/callback'

# defining what data to get from the user
scopes = 'user-read-private user-read-email user-read-currently-playing playlist-read-private playlist-modify-public'

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
    # return 'hello world'

    res = requests.post(url=url, data=body)
    token = json.loads(res.text)['access_token']

    foo = requests.get(url= 'https://api.spotify.com/v1/me', headers={'Authorization': 'Bearer ' + token})
    #
    print(json.loads(foo.text))
    # User = user.User(json.loads(res.text)['access_token'], json.loads(res.text)['expires_in'])
    # User.get_playlists()
    # lyrics = 'foo'
    # output = lyrics + '\n metadata:' + str(vars(User))
    return(token)


app.run()
from globals import spotify_api_base
import requests
import json
import urllib
from urllib.parse import urlencode


def search_playlist(token, key, limit=50):
    res = requests.get(url=(spotify_api_base + 'search?' + urlencode({
        'q': key,
        'type': 'playlist',
        'limit': str(limit)
    })),
                    headers={'Authorization': 'Bearer ' + token})

    return json.loads(res.text)


# Playlist Object
# Ryan Willis
# March 2020

import requests
import json
from globals import spotify_api_base
from urllib.parse import urlencode


class Playlist:

    def __init__(self, id, auth_token):
        self.id = id
        self.auth_token = auth_token

    def get_tracks(self):
        songs = []
        res = requests.get(url=spotify_api_base + 'playlists/' + self.id + '/tracks?',
                           headers={'Authorization': 'Bearer ' + self.auth_token})
        for song in json.loads(res.text)['items']:
            songs.append({
                'name': song['track']['name'],
                'id': song['track']['id'],
                'artist': song['track']['artists'][0]['name'],
                'explicit': song['track']['explicit'],
                'release_date': song['track']['album']['release_date'],
                'uri': song['track']['uri']
            })

        if 'next' in json.loads(res.text):
            while json.loads(res.text).get('next') is not None:
                res = requests.get(url=json.loads(res.text)['next'],
                                   headers={'Authorization': 'Bearer ' + self.auth_token})
                for song in json.loads(res.text)['items']:
                    songs.append({
                        'name': song['track']['name'],
                        'id': song['track']['id'],
                        'artist': song['track']['artists'][0]['name'],
                        'explicit': song['track']['explicit'],
                        'release_date': song['track']['album']['release_date'],
                        'uri': song['track']['uri']
                    })
        return songs

    # Removes a song of id 'id' from the playlist
    def remove_song(self, uris):
        data = []
        for uri in uris:
            data.append({'uri': uri})

        res = requests.delete(url=spotify_api_base + 'playlists/'+self.id+'/tracks',
                        headers={'Authorization': 'Bearer ' + self.auth_token,
                                 'Content-Type': 'application/json'},
                        json={
                            'tracks': data
                        })
        if res.status_code is not 200:
            print('delete failed, probably being rate limited')
from search import search_playlist
from playlist import Playlist
from azlyrics import azlyrics
from config import mongo_connect_uri
from globals import spotify_api_base
import pymongo
import requests
import json
import re

def build_dataset(genre_list, token, playlist_per_genre=8):
    client = pymongo.MongoClient(mongo_connect_uri)
    db = client.songs
    collection = db['songs']

    playlist_index = []
    for genre in genre_list:
        search = search_playlist(token=token, key=genre, limit=playlist_per_genre)['playlists']['items']
        for playlist in search:
            playlist_index.append({
                'genre': genre,
                'name': playlist['name'],
                'id': playlist['id']
            })

    for index in playlist_index:
        playlist_songs = Playlist(id=index['id'], auth_token=token).get_tracks()
        for song in playlist_songs:

            audio_analysis = requests.get(spotify_api_base + 'audio-analysis/' + song['id'],
                                          headers={'Authorization': 'Bearer ' + token})

            song['audio_analysis'] = {
                'sections': json.loads(audio_analysis.text)['sections'],
                'track': json.loads(audio_analysis.text)['track']
            }

            audio_features = requests.get(spotify_api_base + 'audio-features/' + song['id'],
                                          headers={'Authorization': 'Bearer ' + token})

            song['audio-features'] = json.loads(audio_features.text)

            song['genre'] = index['genre']
            song['from_playlist'] = {
                'name': index['name'],
                'id': index['id']
            }
            # print(collection.insert_one(song).inserted_id)
            criteria = {'id': song['id']}
            print(collection.update(criteria, song, upsert=True))
        index['tracks'] = playlist_songs

    return playlist_index

from search import search_playlist
from playlist import Playlist
from azlyrics import azlyrics
import re

def build_dataset(genre_list, token, playlist_per_genre=1):
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
        playlist_songs = Playlist(id=index['id'], auth_token=token).get_tracks()[:15]
        for song in playlist_songs:
            song_nm = re.sub("[\(\[].*?[\)\]]", "", song['name'])
            song_nm = re.sub("[\(\[]\?*?[\)\]]", "", song['name'])
            song_nm = re.sub("[\(\[]\&*?[\)\]]", "", song['name'])
            lyrics = azlyrics.lyrics(artist=song['artist'], song=song_nm)
            print(song_nm)
            song['lyrics'] = lyrics
            # if 'Error' not in lyrics:
            #     song['lyrics'] = lyrics
        index['tracks'] = playlist_songs

    return playlist_index

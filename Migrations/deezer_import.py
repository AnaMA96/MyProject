import requests
import json
import base64
from urllib.parse import urlencode

me_url = 'https://api.deezer.com/user/me'

def getDeezerCredentials():
    with open('json/deezer_credentials.json') as json_file:
        return json.load(json_file)

def getToken():
    return getDeezerCredentials()['access_token']

def getSpotifyJson():
     with open('json/playlists.json') as json_file:
        return json.load(json_file)

def getDeezer(url, query_params={}, params = {}, headers = {}):
    query_params['output'] = 'json'
    query_params['access_token'] = getToken()
    url += f'?{urlencode(query_params)}'
    response = requests.get(url, data=params, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {'Error': 'Something went wrong'}

def searchTrackByName(name, artists_names):
    print(f'SEARCHING BY NAME: {name}')
    url = 'https://api.deezer.com/search/track'
    response_tracks_json = getDeezer(url, query_params={'q': name})
    for track in response_tracks_json['data']:
        if ((track['title'].lower() or track['title_short'].lower()) == name) and (track['artist']['name'].lower() in artists_names):
            return track
    return None

def searchTrack(isrc, name, artists_names):
    url = f'https://api.deezer.com/2.0/track/isrc:{isrc}'
    response = requests.get(url)
    if response.status_code != 200:
        track = searchTrackByName(name, artists_names)
        print(f'searching track: {name}, track: {track}')
        return track
    else:
        print(f'searching track: {name}, response: {response}')
        return response.json()
    
def postPlaylist(name, user_id):
    query_params = {}
    url = f'https://api.deezer.com/user/{user_id}/playlists'
    query_params['output'] = 'json'
    query_params['access_token'] = getToken()
    query_params['title'] = name
    url += f'?{urlencode(query_params)}'
    response = requests.post(url)
    print(response.json())
    response_json = response.json()
    if 'id' in response_json:
        return str(response_json['id'])
    else:
        return None

def postPlaylistTracks(playlist_id, tracks_ids):
    query_params = {}
    url = f'https://api.deezer.com/playlist/{playlist_id}/tracks'
    query_params['output'] = 'json'
    query_params['access_token'] = getToken()
    query_params['songs'] = tracks_ids
    url += f'?{urlencode(query_params)}'
    response = requests.post(url)
    

def iteratePlaylists(user_id):
    spotify_json = getSpotifyJson()
    for playlist in spotify_json:
        playlist_name = playlist['name']
        print(f'Playlists tracks: {playlist_name}')
        playlist_id = postPlaylist(playlist_name, user_id)
        if playlist_id and 'tracks_list' in playlist:
            tracks_ids = ''
            for track in playlist['tracks_list']:
                track_isrc = ''
                if 'isrc' in track['track']['external_ids']:
                    track['track']['external_ids']['isrc']
                    track_name = track['track']['name'].lower()
                    artists_names = []
                    for artist in track['track']['artists']:
                        artists_names.append(artist['name'].lower())
                    track_found = searchTrack(track_isrc, track_name, artists_names)
                    if 'id' in track_found:
                        if tracks_ids == '':
                            tracks_ids += str(track_found['id'])
                        else:
                            t_id = str(track_found['id'])
                            tracks_ids += f',{t_id}'
            postPlaylistTracks(playlist_id, tracks_ids)
            

def main_deezer_import():
    me_info = getDeezer(me_url)
    iteratePlaylists(str(me_info['id']))



if __name__ == "__main__":
    main_deezer_import()



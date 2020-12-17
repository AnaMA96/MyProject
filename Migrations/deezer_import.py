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
            print(f"Found: {name}")
            return track
    return {'Error': 'Not found'}

def searchTrack(isrc, name, artists_names):
    print(f"SEARCHING BY ISRC: {isrc}")
    url = f'https://api.deezer.com/2.0/track/isrc:{isrc}'
    
    response = requests.get(url)
    response_json = response.json()
    if 'Error' in response_json or 'error' in response_json:
        track = searchTrackByName(name, artists_names)
        return track
    else:
        print(f'Found: {isrc}, response: {response}')
        return response_json
    
def postPlaylist(name, user_id):
    print(f"Creating playlist: {name}")
    query_params = {}
    url = f'https://api.deezer.com/user/{user_id}/playlists'
    query_params['output'] = 'json'
    query_params['access_token'] = getToken()
    query_params['title'] = name
    url += f'?{urlencode(query_params)}'
    response = requests.post(url)
    print(f"Created: {response.json()}")
    response_json = response.json()
    if 'id' in response_json:
        return str(response_json['id'])
    else:
        return None

def postPlaylistTracks(playlist_id, tracks_ids):
    print(f"Adding playlist tracks")
    query_params = {}
    url = f'https://api.deezer.com/playlist/{playlist_id}/tracks'
    query_params['output'] = 'json'
    query_params['access_token'] = getToken()
    query_params['songs'] = tracks_ids
    url += f'?{urlencode(query_params)}'
    response = requests.post(url)
    print(f"{response}")

def iteratePlaylists(user_id):
    spotify_json = getSpotifyJson()
    for playlist in spotify_json:
        playlist_name = playlist['name']
        print(f'Playlists tracks: {playlist_name}')
        playlist_id = postPlaylist(playlist_name, user_id)
        if playlist_id and 'tracks_list' in playlist:
            tracks_ids = set()
            for track in playlist['tracks_list']:
                track_isrc = ''
                if 'isrc' in track['track']['external_ids']:
                    track_isrc = track['track']['external_ids']['isrc']
                    track_name = track['track']['name'].lower()
                    artists_names = []
                    for artist in track['track']['artists']:
                        artists_names.append(artist['name'].lower())
                    track_found = searchTrack(track_isrc, track_name, artists_names)
                    if 'id' in track_found:
                        tracks_ids.add(str(track_found['id']))
            tarcks_ids = list(tracks_ids)

            tracks_ids_aux = []
            for track_id in tracks_ids:
                tracks_ids_aux.append(track_id)
                if len(tracks_ids_aux) == 100:
                    tracks = ','.join(tracks_ids_aux)
                    postPlaylistTracks(playlist_id, tracks)
                    tracks_ids_aux = []
    
            if len(tracks_ids_aux) > 0:
                tracks = ','.join(tracks_ids_aux)
                postPlaylistTracks(playlist_id, tracks)

def main_deezer_import():
    me_info = getDeezer(me_url)
    iteratePlaylists(str(me_info['id']))



if __name__ == "__main__":
    main_deezer_import()



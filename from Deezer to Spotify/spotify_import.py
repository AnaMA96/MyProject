import requests
import json
import base64
from urllib.parse import urlencode
from spotify_export import get, getTokenType, getAccessToken

me_url = 'https://api.spotify.com/v1/me'

def getCredentials():
    with open('../json/credentials.json') as json_file:
        return json.load(json_file)

def post(url, params={}, should_refresh_token=True):
    headers = {'Authorization':  getTokenType() + ' ' +  getAccessToken()}
    response = requests.post(url, data=params, headers=headers)
    print(response.json())
    if response.status_code >= 200 and response.status_code < 300:
        return response.json()
    elif response.status_code == 401 and should_refresh_token:
        if refreshToken():
            return post(url, params=params, headers=headers, should_refresh_token=False)
        else:
            return {'Error': 'Something went wrong'}
    else:
        return {'Error': 'Something went wrong'}


def getDeezerJson():
     with open('../json/deezer_playlists.json') as json_file:
        return json.load(json_file)


def searchTrackByNameSpoti(title, deezer_artists_names):
    print(f'SEARCHING BY NAME: {title}')
    query_params = urlencode({'q': name, 'type': track})
    url = f'https://api.spotify.com/v1/search?{query_params}'
    response_tracks_json = get(url)
    for track in response_tracks_json['tracks']:
        artists_names = []
        for artist in track['tracks']['artists']:
            artists_names.append(artist['name'].lower())
        if ((track['name'].lower() == title)):
            for deezer_artist_name in deezer_artists_names:
                if deezer_artist_name in artists_names:
                    return track
    return None

def searchTrack(isrc, name, artists_names):
    url = f'https://api.spotify.com/v1/search?type=track&q=isrc:{isrc}'
    response_json = get(url)
    if 'tracks' in response_json and 'items' in response_json['tracks'] and len(response_json['tracks']['items']) == 0:
        track = searchTrackByNameSpoti(tile, artists_names)
        print(f'searching track: {name}, track: {track}')
        return track
    else:
        print(f'searching track: {name}, response: {response_json}')
        return response_json['tracks']['items'][0]

def postPlaylistSpoti(name, user_id):
    params = {
        "name": name,
        "public": "true"
        }
    url = f'https://api.spotify.com/v1/users/{user_id}/playlists'
    response_json = post(url, params=json.dumps(params))
    print(f"POST playlists: {response_json}")
    if 'id' in response_json:
        return str(response_json['id'])
    else:
        return None

def postPlaylistTracks(playlist_id, tracks_uris):
    if len(tracks_uris) == 0:
        return

    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    tracks_uris_param = []
    for track_uri in tracks_uris:
        tracks_uris_param.append(track_uri)
        if len(tracks_uris_param) == 100:
            post_tracks_url = url + '?' + urlencode({'uris': ','.join(tracks_uris_param)})        
            print(post_tracks_url)
            post(post_tracks_url)
            tracks_uris_param = []
    
    if len(tracks_uris_param) > 0:
        post_tracks_url = url + '?' + urlencode({'uris': ','.join(tracks_uris_param)})
        post(post_tracks_url)

def iteratePlaylists(user_id):
    deezer_json = getDeezerJson()
    for playlist in deezer_json:
        playlist_name = playlist['title']
        print(f'Playlists tracks: {playlist_name}')
        playlist_id = postPlaylistSpoti(playlist_name, user_id)
        if playlist_id and 'tracks_list' in playlist:
            tracks_uris = []
            for track in playlist['tracks_list']:
                if 'isrc' in track:
                    track_isrc = track['isrc']
                    track_name = track['title'].lower()
                    artists_names = []
                    for artist in track['contributors']:
                        artists_names.append(artist['name'].lower())
                    track_found = searchTrack(track_isrc, track_name, artists_names)
                    if 'uri' in track_found:
                        tracks_uris.append(track_found['uri'])
            print(tracks_uris)
            postPlaylistTracks(playlist_id, tracks_uris)
            

def main():
    me_info = get(me_url)
    print(f"IMPORT MAIN: {me_info}")
    iteratePlaylists(str(me_info['id']))



if __name__ == "__main__":
    main()

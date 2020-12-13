import requests
import json
import base64

me_url = 'https://api.deezer.com/user/me'

def getDeezerCredentials():
    with open('deezer_credentials.json') as json_file:
        return json.load(json_file)

def getToken():
    return getDeezerCredentials()['access_token']

def getSpotifyJson():
     with open('playlists.json') as json_file:
        return json.load(json_file)

def getDeezer(url, params = {}, headers = {}):
    url += f'?output=json&access_token={getToken()}'
    response = requests.get(url, data=params, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {'Error': 'Something went wrong'}

def searchTrackByName(isrc, name, artist_name):
    url = f'https://api.deezer.com/search/track?q={name}'
    response_tracks_json = getDeezer(url)
    print(f'searching track: {name}, response: {response_tracks_json}')
    for track in response_tracks_json['data']:
        

def searchTrackByIsrc(isrc, name):
    url = f'https://api.deezer.com/2.0/track/isrc:{isrc}'
    response_json = requests.get(url).status_code
    print(f'searching track: {name}, response: {response_json}')

def iteratePlaylists():
    spotify_json = getSpotifyJson()
    for playlist in spotify_json:
        playlist_name = playlist['name']
        print(f'Playlists tracks: {playlist_name}')
        for track in playlist['tracks_list']:
            track_isrc = track['track']['external_ids']['isrc']
            track_name = track['track']['name']
            searchTrackByIsrc(track_isrc, track_name)

def main():
    me_info = getDeezer(me_url)
    iteratePlaylists()

if __name__ == "__main__":
    main()

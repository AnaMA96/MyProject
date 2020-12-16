import requests
import json
import base64
import os
from dotenv import load_dotenv
load_dotenv()

clientid = os.getenv('Client_ID')
clientsecret = os.getenv('Client_Secret')

mePlaylistUrl = 'https://api.spotify.com/v1/me/playlists'
playlistTraksUrl = 'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'

def refreshToken():
    url = "https://accounts.spotify.com/api/token"
    params = {
        'grant_type': 'refresh_token', 
        'refresh_token': getRefreshToken(),
        }

    authorization = base64.b64encode(bytes(clientid + ':' + clientsecret, 'utf-8'))
    response = requests.post(url, data=params, headers={'Authorization': 'Basic ' + authorization.decode('utf-8')})
    print(f"REFRESH TOKEN: {response.json()}")
    credentials_json = getCredentials()
    for k,v in response.json().items():
            credentials_json[k] = v
    with open('../json/credentials.json', 'w') as outfile:
        json.dump(credentials_json, outfile)
    
    if response.status_code == 200:
        return True
    else:
        return False


def getCredentials():
    with open('../json/credentials.json') as json_file:
        return json.load(json_file)

def getAccessToken():
    return getCredentials()['access_token']
    
def getTokenType():
    return getCredentials()['token_type']

def getRefreshToken():
    return getCredentials()['refresh_token']

def get(url, params={}, should_refresh_token=True):
    headers = {'Authorization':  getTokenType() + ' ' +  getAccessToken()}
    response = requests.get(url, data=params, headers=headers)

    if response.status_code == 200:
        print(f"GET: {response.json()}")
        return response.json()
    elif response.status_code == 401 and should_refresh_token:
        if refreshToken():
            return get(url, params, headers)
        else:
            return {'Error': 'Something went wrong'}
    else:
        return {'Error': 'Something went wrong'}
        

def getUserPlaylistsPaginated(items, url):
    if not url:
        return

    response_json = get(url)
    items += response_json['items']

    getUserPlaylistsPaginated(items, response_json['next'])


def getUserPlaylists():
    items = []
    getUserPlaylistsPaginated(items, mePlaylistUrl)
    return items


def getUserPlaylistsTraks(playlists):
    for playlist in playlists:
        playlist['tracks_list'] = []
        getUserPlaylistsTracksPaginated(playlist, playlistTraksUrl.format(playlist_id = playlist['id']))
        print(playlist['id'] + ': ' + str(len(playlist['tracks_list'])) + ' ' + str(playlist['tracks']['total']))

def getUserPlaylistsTracksPaginated(playlist, url):
    if not url:
        return

    response_json = get(url)
    tracks_list = playlist['tracks_list']
    tracks_list += response_json['items']
    playlist['tracks_list'] = tracks_list

    getUserPlaylistsTracksPaginated(playlist, response_json['next'])

def main():
    playlists = getUserPlaylists()
    getUserPlaylistsTraks(playlists)
    with open('../json/playlists.json', 'w') as outfile:
        json.dump(playlists, outfile)

if __name__ == "__main__":
    main()
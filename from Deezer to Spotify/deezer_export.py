import requests
import json
import base64
import os
from dotenv import load_dotenv
load_dotenv()
from deezer_import import getDeezer

clientid = os.getenv('Client_ID')
clientsecret = os.getenv('Client_Secret')

myPlaylistUrl = 'https://api.deezer.com/user/me/playlists'
playlistTraksUrl = 'https://api.deezer.com/playlist/{playlist_id}/tracks'

def getDeezerCredentials():
    with open('../json/deezer_credentials.json') as json_file:
        return json.load(json_file)

def getToken():
    return getDeezerCredentials()['access_token']

def getUserPlaylists(url):
    if not url:
        return
    response_json = getDeezer(url)
    return response_json['data']

def getUserPlaylistsTraks(playlists):
    for playlist in playlists:
        playlist['tracks_list'] = []
        getUserPlaylistsTracksPaginated(playlist, playlistTraksUrl.format(playlist_id = playlist['id']))
        print(playlist)
        print(str(playlist['id']) + ': ' + str(len(playlist['tracks_list'])))

def getUserPlaylistsTracksPaginated(playlist, url):
    if not url:
        return

    response_json = getDeezer(url)
    tracks_list = playlist['tracks_list']
    tracks_list += response_json['data']
    tracks_isrc_list = []
    for track in tracks_list:
        track_id = track['id']
        url = f'https://api.deezer.com/track/{track_id}'
        tracks_isrc_list.append(getDeezer(url))
    playlist['tracks_list'] = tracks_isrc_list

    print(response_json)
    if 'next' in response_json:
        getUserPlaylistsTracksPaginated(playlist, response_json['next'])

def main():
    playlists = getUserPlaylists(myPlaylistUrl)
    getUserPlaylistsTraks(playlists)
    with open('../json/deezer_playlists.json', 'w') as outfile:
        json.dump(playlists, outfile)

if __name__ == "__main__":
    main()
from Migrations.deezer_import import getDeezer, getToken, me_url
from urllib.parse import urlencode
import requests, json

me_url = 'https://api.deezer.com/user/me'

def getDeezerCredentials():
    with open('json/deezer_credentials.json') as json_file:
        return json.load(json_file)

def getToken():
    return getDeezerCredentials()['access_token']

def getUserPlaylists():
	me_info = getDeezer(me_url)
	user_id = me_info['id']
	url = f'https://api.deezer.com/user/{user_id}/playlists'
	response_json = getDeezer(url)
	return response_json['data']

def deletePlaylist(playlist_id):
	url = f'https://api.deezer.com/playlist/{playlist_id}'
	query_params = {'access_token': getToken()}
	url += f'?{urlencode(query_params)}'
	response = requests.delete(url)
	print(response)

def deleteUserPlaylists():
	playlists = getUserPlaylists()

	for playlist in playlists:
		if 'id' in playlist:
			deletePlaylist(str(playlist['id']))

def main():
	deleteUserPlaylists()

if __name__ == "__main__":
    main()
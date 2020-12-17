from flask import Flask, request
import requests
import json
import base64
import json
from urllib.parse import urlencode
import os
from dotenv import load_dotenv
load_dotenv()
from Oauth.spotify_OAuth2 import oauth_spoti
from Oauth.deezer_OAuth2 import oauth_deezer

from Migrations.deezer_export import main_deezer_export
from Migrations.spotify_import import main_spoti_import

from Migrations.spotify_export import main_spoti_export
from Migrations.deezer_import import main_deezer_import

clientid = os.getenv('Client_ID')
clientsecret = os.getenv('Client_Secret')
deezerAppId = os.getenv('DEEZER_APP_ID')
deezerSecret = os.getenv('DEEZER_SECRET')
app = Flask(__name__)

global isDeezerImport

@app.route("/spotify/callback")
def spotify_callback():
	code = request.args.get('code')
	if code:
		getSpotifyCredentials(code, '/spotify/callback')
	return "You finally called me back!"

@app.route("/deezer/callback")
def deezer_callback():
	global isDeezerImport
	code = request.args.get('code')
	if code:
		getDeezerCredentials(code)

		if isDeezerImport == True:
			main_deezer_import()
		elif isDeezerImport == False:
			main_deezer_export()
			if os.path.isfile('json/credentials.json'):
				main_spoti_import()
			else:
				oauth_spoti('/spotify/import/callback')

		isDeezerImport = None

	return "You finally called me back!"

@app.route("/spotify/export/callback")
def spotify_callback_export():
	code = request.args.get('code')
	if code:
		getSpotifyCredentials(code, '/spotify/export/callback')
		main_spoti_export()
		if os.path.isfile('json/deezer_credentials.json'):
			main_deezer_import()
		else:
			oauth_deezer('/deezer/callback')
	return "You finally called me back!"

@app.route("/spotify/import/callback")
def spotify_callback_import():
	code = request.args.get('code')
	if code:
		getSpotifyCredentials(code, '/spotify/import/callback')
		main_spoti_import()
	return "You finally called me back!"

def getSpotifyCredentials(code, redirect):
	provider_url = "https://accounts.spotify.com/api/token"

	params = {
	'grant_type': 'authorization_code',
	'code': code,
	'redirect_uri': f'http://127.0.0.1:5000{redirect}'
	}

	authorization = base64.b64encode(bytes(clientid + ':' + clientsecret, 'utf-8'))
	print(clientid)
	print(clientsecret)
	response = requests.post(provider_url, data=params, headers={'Authorization': 'Basic ' + authorization.decode('utf-8')})
	print(response.json())
	with open("json/credentials.json", "w") as outfile: 
		json.dump(response.json(), outfile) 
	print(response.json())

def getDeezerCredentials(code):
	provider_url = "https://connect.deezer.com/oauth/access_token.php"

	params = urlencode({
		'app_id': deezerAppId,
		'secret': deezerSecret,
		'code': code,
		'output': 'json'
		})

	response = requests.post(provider_url + '?' + params)
	with open("json/deezer_credentials.json", "w") as outfile:
		json.dump(response.json(), outfile)
	
@app.route("/spotify/login")
def calling_main_spoti():
	global isDeezerImport
	if os.path.isfile('json/credentials.json'):
		main_spoti_export()
		if os.path.isfile('json/deezer_credentials.json'):
			main_deezer_import()
		else:
			isDeezerImport = True
			oauth_deezer('/deezer/callback')
	else:
		oauth_spoti('/spotify/export/callback')
		
	return 'Please, be patient, we are bringing back your music!!'

@app.route("/deezer/login")
def calling_main_deezer():
	global isDeezerImport
	isDeezerImport = None
	if os.path.isfile('json/deezer_credentials.json'):
		main_deezer_export()
		if os.path.isfile('json/credentials.json'):
			main_spoti_import()
		else:
			oauth_spoti('/spotify/import/callback')
	else:
		isDeezerImport = False
		oauth_deezer('/deezer/callback')

	return 'Please, be patient, we are bringing back your music!!'

@app.route("/")
def index_api():

    HtmlFile = open('templates/menu.html', 'r', encoding='utf-8')
    index_api = HtmlFile.read() 
    return index_api






app.run(debug=True, port=5000)
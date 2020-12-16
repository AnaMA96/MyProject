from flask import Flask, request
import requests
import json
import base64
import json
from urllib.parse import urlencode
import os
from dotenv import load_dotenv
load_dotenv()
from Oauth.spotify_OAuth2 import main_spoti
from Oauth.deezer_OAuth2 import main_deezer


clientid = os.getenv('Client_ID')
clientsecret = os.getenv('Client_Secret')
deezerAppId = os.getenv('DEEZER_APP_ID')
deezerSecret = os.getenv('DEEZER_SECRET')
app = Flask(__name__)

@app.route("/spotify/callback")
def spotify_callback():
	code = request.args.get('code')
	if code:
		getSpotifyCredentials(code)
	return "You finally called me back!"

@app.route("/deezer/callback")
def deezer_callback():
	code = request.args.get('code')
	if code:
		getDeezerCredentials(code)
	return "Deezer called me back"

def getSpotifyCredentials(code):
	provider_url = "https://accounts.spotify.com/api/token"

	params = {
	'grant_type': 'authorization_code',
	'code': code,
	'redirect_uri': 'http://127.0.0.1:5000/spotify/callback'
	}

	authorization = base64.b64encode(bytes(clientid + ':' + clientsecret, 'utf-8'))
	print(clientid)
	print(clientsecret)
	response = requests.post(provider_url, data=params, headers={'Authorization': 'Basic ' + authorization.decode('utf-8')})
	with open("credentials.json", "w") as outfile: 
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
	with open("deezer_credentials.json", "w") as outfile:
		json.dump(response.json(), outfile)
	
@app.route("/spotify/login")
def calling_main_spoti():
	main_spoti()
	return 'We are redirecting you to login!'

@app.route("/deezer/login")
def calling_main_deezer():
	main_deezer()
	return 'We are redirecting you to login!'

@app.route("/")
def index_api():
    HtmlFile = open('templates.menu.html', 'r', encoding='utf-8')
    index_api = HtmlFile.read() 
    return index_api






app.run(debug=True, port=5000)
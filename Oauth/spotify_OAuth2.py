import requests
import pandas as pd
import matplotlib.pyplot as plt
from urllib.parse import urlencode
import os
from dotenv import load_dotenv
load_dotenv()
import webbrowser

clientid = os.getenv('Client_ID')
clientsecret = os.getenv('Client_Secret')

def open(redirect):
    provider_url = "https://accounts.spotify.com/authorize"

    params = urlencode({
        'client_id': clientid,
        'scope': 'playlist-read-private playlist-read-collaborative user-follow-read user-library-read user-read-email playlist-modify-public playlist-modify-private',
        'redirect_uri': f'http://127.0.0.1:5000{redirect}',
        'response_type': 'code'
    })

    url = provider_url + '?' + params
    print(url)
    webbrowser.open(url)

def oauth_spoti(redirect):
    open(redirect)

def main_spoti():
    open('/spotify/callback')
    

if __name__ == "__main__":
    main_spoti()




import requests
import pandas as pd
import matplotlib.pyplot as plt
from urllib.parse import urlencode
import os
from dotenv import load_dotenv
load_dotenv()
import webbrowser
from flask import Flask, request 
app = Flask (__name__)

clientid = os.getenv('Client_ID')
clientsecret = os.getenv('Client_Secret')

def main():
    provider_url = "https://accounts.spotify.com/authorize"

    params = urlencode({
        'client_id': clientid,
        'scope': 'playlist-read-private playlist-read-collaborative user-follow-read user-library-read user-read-email',
        'redirect_uri': 'http://127.0.0.1:5000/spotify/callback',
        'response_type': 'code'
    })

    url = provider_url + '?' + params
    print(url)
    webbrowser.open(url)
    

if __name__ == "__main__":
    main()




import requests
import pandas as pd
from urllib.parse import urlencode
import os
from dotenv import load_dotenv
load_dotenv()
import webbrowser
deezerAppId = os.getenv('DEEZER_APP_ID')
deezerSecret = os.getenv('DEEZER_SECRET')

def main_deezer():
    #https://connect.deezer.com/oauth/auth.php?app_id=YOUR_APP_ID&redirect_uri=YOUR_REDIRECT_URI&perms=basic_access,email
    provider_url = "https://connect.deezer.com/oauth/auth.php"

    params = urlencode({
        'app_id': deezerAppId,
        'perms': 'basic_access,email,offline_access,manage_library',
        'redirect_uri': 'http://localhost:5000/deezer/callback'
    })

    url = provider_url + '?' + params
    print(url)
    webbrowser.open(url)
    

if __name__ == "__main__":
    main_deezer()



import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
load_dotenv() #1

def get_spotify_client(scope = 'user-library-read user-read-currently-playing user-top-read'):
    return spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

#print(sp.current_user()) #2
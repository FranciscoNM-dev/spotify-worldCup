import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
load_dotenv() #1

oauth = SpotifyOAuth(scope='user-top-read', show_dialog=True)

def get_spotify_client(scope = 'user-top-read'):
    return spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

#print(sp.current_user()) #2

def get_auth_url():
    return oauth.get_authorize_url()

def get_token_code(code):
    return oauth.get_access_token(code)

def get_spotify_client_web(access_token): #scope "ya va en el token"
    return spotipy.Spotify(auth=access_token)

def refresh_access_token(refresh_token): #Para renovar access_token, que caduca en una hora
    token_info = oauth.refresh_access_token(refresh_token)
    return token_info['access_token']
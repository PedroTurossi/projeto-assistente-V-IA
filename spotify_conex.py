from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from configparser import ConfigParser

app = Flask(__name__)


app.secret_key = 'Ogj53kSFk9875'
app.config['SESSION_COOKIE_NAME'] = 'Cookie'
TOKEN_INFO = 'token_info'

@app.route('/')
def login():
    sp_oauth = create_spotify_oath()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oath()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('getTracks', _external=True))

@app.route('/getTracks')
def getTracks():
    try:
        token_info = get_token()
    except:
        print('usuário não logado')
        redirect('login', _external=False)
    sp = spotipy.Spotify(auth=token_info['access_token'])
    

    try:
        return sp.current_user_playing_track()
        # return "Música iniciada com sucesso"
    except spotipy.exceptions.SpotifyException as e:
        return f"Erro ao iniciar a música: {e}"

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise 'exception'
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oath()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

def busca_musica():
    token_info = get_token()
    sp = spotipy.Spotify(auth=token_info['access_token'])
    

def create_spotify_oath():
    config = ConfigParser()
    config.read('chave_spotify.ini')
    return SpotifyOAuth(
        client_id = config.get('ID_KEY', 'spotify_id'),
        client_secret = config.get('SECRET_KEY', 'spotify_key'),
        redirect_uri=url_for('redirectPage', _external=True),
        scope='user-library-read user-read-currently-playing user-modify-playback-state user-read-playback-state app-remote-control'
    )
from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os, time, webbrowser
from dotenv import load_dotenv

# Load in the environment vairables from the .env file
load_dotenv()
app_secret = os.getenv("APP_SECRET")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
source_name = os.getenv("SOURCE_PLAYLIST")
destination_name = os.getenv("DESTINATION_PLAYLIST")

app = Flask(__name__)

app.config["SESSON_COOKIE_NAME"] = "Spotify Cookie"
app.secret_key = app_secret

TOKEN = "spotify token"

@app.route("/")
def start():
    spotify_auth_url = new_spotify_oauth().get_authorize_url()
    return redirect(spotify_auth_url)

def new_spotify_oauth():
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=url_for("spotify_auth", _external = True),
        scope="user-library-read playlist-modify-public playlist-modify-private"
    )

@app.route("/auth")
def spotify_auth():
    session.clear()
    code = request.args.get("code")
    token_info = new_spotify_oauth().get_access_token(code)
    session[TOKEN] = token_info
    return redirect("/test")

def get_spotify_token():
    token_info = session.get(TOKEN, None)

    # Have the user authenticate with Spotify if they have not already
    if not token_info:
        redirect("/")
    
    # Refresh the token if necessary
    now = int(time.time())
    is_expired = (token_info["expires_at"] - now) < 60
    if is_expired:
        spotify_oauth = new_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info["refresh_token"])

    return token_info

@app.route("/source")
def get_all_songs():
    return None

@app.route("/dest")
def shuffle():
    return None


app.run(debug=True)
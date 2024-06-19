from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os, time, webbrowser, random
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
    # Redirect to the url for Spotify authentication.
    spotify_auth_url = new_spotify_oauth().get_authorize_url()
    return redirect(spotify_auth_url)

def new_spotify_oauth():
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=url_for("spotify_auth", _external = True),
        scope="user-library-read playlist-read-private playlist-modify-public playlist-modify-private"
    )

@app.route("/auth")
def spotify_auth():
    # Store the access token resulting from the authentication
    session.clear()
    code = request.args.get("code")
    token_info = new_spotify_oauth().get_access_token(code)
    session[TOKEN] = token_info
    return redirect("/shuffle")

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

@app.route("/shuffle")
def shuffle_songs():
    # Attempt to get the authentication token
    try: 
        token_info = get_spotify_token()
    except:
        print('User not logged in')
        return redirect("/")
    
    spotify = spotipy.Spotify(auth=token_info['access_token'])
    user_id = spotify.current_user()['id']

    source_id = None
    destination_id = None
    
    # Get the ids of the two playlists this app interacts with
    playlists = spotify.user_playlists(user_id)['items']
    for playlist in playlists:
        if(playlist['name'] == source_name):
            source_id = playlist['id']
        if(playlist['name'] == destination_name):
            destination_id = playlist['id']
    
    # Check the ids
    if not source_id:
        return f'Please create a source playlist named "{source_name}", or change which playlist is the source in the .env file.'
    if not destination_id:
        # Create the destination playlist if it was not already present.
        destination_id = spotify.user_playlist_create(user_id, destination_name, False, False, f'Random songs selected from playlist "{source_name}"')["id"]
    
    # Get the uris for the songs in the source playlist
    source_playlist = spotify.playlist_items(source_id)
    source_songs = []
    for song in source_playlist["items"]:
        source_songs.append(song['track']['uri'])

    # Remove all songs from the destination playlist
    destination_playlist = spotify.playlist_items(destination_id)
    destination_songs = []
    for song in destination_playlist["items"]:
        destination_songs.append(song['track']['uri'])
    spotify.playlist_remove_all_occurrences_of_items(destination_id, destination_songs)

    # Add a random sample of songs from the source playlist.
    spotify.playlist_add_items(destination_id, random.sample(source_songs, 50))

    return "Done"

webbrowser.open('http://127.0.0.1:5000/', new=2)
app.run(debug=True)
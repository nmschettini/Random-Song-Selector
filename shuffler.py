from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os, time, webbrowser
from dotenv import load_dotenv

# Load in the environment vairables from the .env file
load_dotenv()
app_secret = os.getenv("APP_SECRET")
spotify_client_id = os.getenv("CLIENT_ID")
spotify_client_secret = os.getenv("CLIENT_SECRET")
source_name = os.getenv("SOURCE_PLAYLIST")
destination_name = os.getenv("DESTINATION_PLAYLIST")

app = Flask(__name__)

app.config["SESSON_COOKIE_NAME"] = "Spotify Cookie"
app.secret_key = app_secret

TOKEN = "spotify token"
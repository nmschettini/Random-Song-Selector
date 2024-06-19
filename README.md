# Spotify Song Shuffler
## Description
This app makes use of Flask and Spotipy to select a random subset of songs from one playlist that will make up a seperate playlist.

## Requirements
- spotipy 
- Flask 
- python-dotenv

## Instructions
1. Create a Spotify app at https://developer.spotify.com/dashboard
2. Set the redirect uri of that app to be http://127.0.0.1:5000/auth
3. Replace the values in the .env file for APP_SECRET, CLIENT_ID, and CLIENT_SECRET. CLIENT_ID and CLIENT_SECRET come from the spotify for developers dashboard. APP_SECRET can be any made up secret key you want.
4. Run the app by doing "python shuffler.py" in your command prompt
5. Follow the instructions to authenticate with spotify

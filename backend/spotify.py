from flask import session
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API credentials (from Spotify Developer Dashboard)
CLIENT_ID = 'd3dfbb511519452eb37598a2f6bff37d'
CLIENT_SECRET = '95ee10c92e874b158386029f13b13456'
REDIRECT_URI = 'https://www.moodmusic.club/callback'

# Initialize Spotify OAuth
sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET,
                         redirect_uri=REDIRECT_URI,
                         scope="user-library-read playlist-modify-public")

# Function to get access token
def get_spotify_client():
    token_info = session.get('token_info', None)
    if not token_info:
        return None
    sp = spotipy.Spotify(auth=token_info['access_token'])
    return sp

# Function to fetch user data
def get_user_profile(sp):
    return sp.current_user()

# Function to get liked songs
def get_liked_songs(sp):
    return sp.current_user_saved_tracks()

# Add more functions as needed (e.g., search, create playlists)

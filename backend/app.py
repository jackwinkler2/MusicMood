from flask import Flask, redirect, session, request
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Make sure to set this

# Spotify OAuth setup
CLIENT_ID = 'd3dfbb511519452eb37598a2f6bff37d'  # Replace with your Spotify client ID
CLIENT_SECRET = '95ee10c92e874b158386029f13b13456'  # Replace with your Spotify client secret
REDIRECT_URI = 'https://www.moodmusic.club/'  # Ensure this matches your Spotify Developer redirect URI

# Initialize Spotify OAuth
sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET,
                         redirect_uri=REDIRECT_URI,
                         scope="user-library-read user-top-read")  # Add scopes based on the data you need

@app.route('/')
def index():
    return '<a href="/login">Login with Spotify</a>'

@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()  # Redirects to Spotify's login page
    return redirect(auth_url)

@app.route('/callback')
def callback():
    token_info = sp_oauth.get_access_token(request.args['code'])  # Exchange code for token
    session['token_info'] = token_info  # Save token in session
    return redirect('/profile')  # Redirect to profile or dashboard

@app.route('/profile')
def profile():
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect('/')
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    user = sp.current_user()
    return f"Hello, {user['display_name']}!<br>Your top track: {user['followers']['total']} followers"

if __name__ == '__main__':
    app.run(debug=True)
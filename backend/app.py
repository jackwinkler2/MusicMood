from flask import Flask, redirect, session, request
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import secrets
import logging

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  

# Spotify OAuth setup
CLIENT_ID = 'd3dfbb511519452eb37598a2f6bff37d'  
CLIENT_SECRET = '95ee10c92e874b158386029f13b13456'  
REDIRECT_URI = 'https://www.moodmusic.club/callback'  

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
    app.logger.debug(f"Callback request args: {request.args}")

    try:
        # Check if 'code' parameter exists in the callback request
        code = request.args.get('code', None)
        if not code:
            app.logger.error("No authorization code returned in the callback.")
            return "No authorization code received", 400

        # Exchange the authorization code for an access token
        try:
            token_info = sp_oauth.get_access_token(code)
            if not token_info or 'access_token' not in token_info:
                raise ValueError("Failed to retrieve valid access token.")
            app.logger.debug(f"Token info: {token_info}")
        except ValueError as ve:
            app.logger.error(f"Token exchange failed: {str(ve)}")
            return f"Token exchange failed: {str(ve)}", 400
        except Exception as e:
            app.logger.error(f"Unexpected error during token exchange: {str(e)}")
            return f"Error during token exchange: {str(e)}", 400

        # Save token in session, ensuring the session is active
        try:
            session['token_info'] = token_info
        except Exception as e:
            app.logger.error(f"Error saving token to session: {str(e)}")
            return f"Error saving token to session: {str(e)}", 400

        # Redirect to profile or dashboard
        try:
            return redirect('/')  # Redirect to the main page or dashboard
        except Exception as e:
            app.logger.error(f"Error during redirect: {str(e)}")
            return f"Error during redirect: {str(e)}", 400

    except Exception as e:
        app.logger.error(f"Error during callback: {str(e)}")
        return f"Error during callback: {str(e)}", 400  # Return a generic 500 error for unexpected failures


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
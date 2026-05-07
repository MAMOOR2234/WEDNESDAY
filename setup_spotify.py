"""One-time Spotify OAuth setup. Run: python setup_spotify.py"""

import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:8888/callback")

print("=== Spotify Setup ===")


import spotipy
from spotipy.oauth2 import SpotifyOAuth

scopes = "user-modify-playback-state user-read-playback-state user-read-currently-playing"

auth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,\
    scope=scopes,
    cache_path=".spotify_token_cache",
    open_browser=False,
)

auth_url = auth.get_authorize_url()
print("\n1. Open this URL in your browser:\n")
print(f"   {auth_url}\n")
print("2. Log in and click Agree.")
print("3. You'll be redirected to a page that might not load — that's fine.")
print("4. Copy the FULL URL from your browser address bar and paste it here.\n")

response_url = input("Paste the redirect URL here: ").strip()

code = auth.parse_response_code(response_url)
token = auth.get_access_token(code, as_dict=False)

if token:
    print("\nSuccess! Spotify is authorized. You can now use Wednesday to control music.")
else:
    print("\nSomething went wrong. Try again.")

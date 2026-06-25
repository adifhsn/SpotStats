# pip install spotipy

import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id = "your-client-id",
    client_secret = "your-client-secret",
    redirect_uri = "http://127.0.0.1:8888/callback",
    scope = "user-top-read"
))

term_length = "N/A"

while (term_length == "N/A"):


    user_input = input("""
Which length would you like SpotStats to search? (Please select an option 1-3)
1. Short Term (Last 4 weeks)
2. Medium Term (Last 6 Months)
3. Long Term (All Time)
""")

    if user_input == "1":
        term_length = "short_term" # last 4 weeks
        break
    elif user_input == "2":
        term_length = "medium_term" # last 6 months
        break
    elif user_input == "3":
        term_length = "long_term" # all time
        break
    else:
        print("Not a valid input. Try again.")
        

print()

top_tracks = sp.current_user_top_tracks(limit=5, time_range=term_length)

print("My Top Songs:")
for i, track in enumerate(top_tracks["items"]):
    print(f'{i+1}. {track["name"]} by {track["artists"][0]["name"]}') # main artist

print()

top_artists = sp.current_user_top_artists(limit=5, time_range=term_length)

print("My Top Artists:")
for i, artist in enumerate(top_artists["items"]):
    print(f'{i+1}. {artist["name"]}')



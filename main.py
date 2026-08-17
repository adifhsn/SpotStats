import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sys
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-top-read"
))


def get_term_length():
    term_length = "N/A"
    while (term_length == "N/A"):
        user_input = input("""Which length would you like SpotStats to search? (Please select an option 1-3)
1. Short Term (Last 4 weeks)
2. Medium Term (Last 6 Months)
3. Long Term (All Time)
""")

        if user_input == "1":
            term_length = "short_term"  # last 4 weeks
        elif user_input == "2":
            term_length = "medium_term"  # last 6 months
        elif user_input == "3":
            term_length = "long_term"  # all time
        else:
            print("Not a valid input. Try again.")
    return term_length

term_length = get_term_length()

def get_top_tracks(term_length):
    try:
        top_tracks = sp.current_user_top_tracks(limit=5, time_range=term_length)
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error connecting to the Spotify API: {e}")
        sys.exit()
    print("My Top Songs:")
    for i, track in enumerate(top_tracks["items"]):
        if track["artists"] != []:
            print(f'{i+1}. {track["name"]} by {track["artists"][0]["name"]}')  # main artist only
        else:
            print(f'{i+1}. {track["name"]}')
    return top_tracks

def get_top_artists(term_length):
    try:
        top_artists = sp.current_user_top_artists(limit=5, time_range=term_length)
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error connecting to the Spotify API: {e}")
        sys.exit()
    print("My Top Artists:")
    for i, artist in enumerate(top_artists["items"]):
        print(f'{i+1}. {artist["name"]}')
    return top_artists

print()
tracks_data = get_top_tracks(term_length)
print()
artists_data = get_top_artists(term_length)

tracks_df = pd.DataFrame(tracks_data["items"])
tracks_df["artist_name"] = tracks_df["artists"].apply(lambda trackartist: trackartist[0]["name"])
tracks_df = tracks_df[["name", "artist_name", "uri"]]
artists_df = pd.DataFrame(artists_data["items"])
artists_df = artists_df[["name", "uri"]]
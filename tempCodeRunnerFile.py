# pip install spotipy 
# pip install python-dotenv

# you could also do pip install spotipy python-dotenv and keep going 

""" 
Git Notes:
git add .gitignore -> adds .gitignore file
git status -> shows you new or modified files (except the ones in .gitignore)
git add . -> "everything in this folder and subfolders that isn't ignored (step before committing)
git commit -m "your message here" -> "-m" flag followed by a message in quotes describes what changed (ex: git commit -m "Add .env support, clean up loop, update README")
git push -> pushes the local commits (the ones saved with git commit) to the repository
git pull -> downloads any committs from GitHub that you don't have locally and merges them to current branch
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sys
from dotenv import load_dotenv # dotenv package
import os
import pandas as pd # gives the module a shorter nickname that can be used in the code (ex: panda.DataFrame() -> pd.DataFrame())
# spotipy isn't just one file, it's a package made of multiple sub folders/files inside it
# one of those is oauth2 which contains a class called SpotifyOAuth
# from X import yu means go into module x and pull outt just this one specific thing Y so I can use it directly by name
# import SpotifyOAuth by itself wouldn't work because it isn't a library, it's a class that lives inside spotify.oauth2

load_dotenv() # looks for .env in folder, reads data, and loads each into the program's enviroment variables (same place os.getenv() looks)
# for github prokects create a file named .gitignore and add ".env" (one entry per line) - ignores the file itself
# you can't ignore .gitignore itself

# .gitignore - git add .gitignore (adds it) - git status (shows you the new file and modified files) just to make sure it works

#.env is for secrets, things that would be dangerous if someone else saw them

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
# spotipy.Spotify(...) is the object you'll actually use to make API calls (requesting Spotify's servers asking for specific data) like getting top tracks
# auth_manager checks if it is an authorized app/user
    client_id=os.getenv("SPOTIFY_CLIENT_ID"), # in .env don't put a space between the variable and key
    # don't forget to set the client_id to the .env
    # it does not have to be SPOTIFY_CLIENT_ID specfically, we just picked that for readability
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"), #.env file variables should be all caps
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-top-read"
    # no spaces around = for keyword args (client_id=...), but keep spaces for real variable assignment (x = "y")
))


def get_term_length(): # get_term_length not term_length because there is already a variabl with that name (naming conflict)
    term_length = "N/A"
    while (term_length == "N/A"):
        user_input = input("""Which length would you like SpotStats to search? (Please select an option 1-3)
1. Short Term (Last 4 weeks)
2. Medium Term (Last 6 Months)
3. Long Term (All Time)
""")
    
        if user_input == "1":
            term_length = "short_term" # last 4 weeks *
            #break # a break would be redundant because you change term_lemgth
        elif user_input == "2":
            term_length = "medium_term" # last 6 months *
        elif user_input == "3":
            term_length = "long_term" # all time *
        else:
            print("Not a valid input. Try again.") 
    return term_length # return instead of print because it returns the value back to wherever the function was called so you can store it and use it (ex: term_length = get_term_length())

term_length = get_term_length() # set as variable and call so you don't ask the questions twice

def get_top_tracks(term_length): # use a parameter when the value CHANGES or the function needs it do it's job, skip it (use a global variable) only for things th at never change
    try: # error handling
        top_tracks = sp.current_user_top_tracks(limit=5, time_range=term_length)
        #print(top_tracks)
    except spotipy.exceptions.SpotifyException as e: # try except syntax 
        print(f"Error connecting to the Spotify API: {e}") # don't forget {e}
        sys.exit() # stops program
    # spotipy.exceptions.SpotifyException - "go into the spotipy library, then into its exceptions file, and grab the SpotifyException class"
    # so when you write except, yhou can be specific about catching Spotify-related problems specfically, rather than accidentally catching bugs in you rown code (like a typo error[NameError])
    # Some examples that could be caught by spotipy.exceptions.SpotifyException are "invalid token", "rate limited exceeded", "bad request"
    # Some examples that wouldn't be caught by spotipy.exceptions.SpotifyException are no internet connection at all (usually a different error like requests.exceptions.ConnectionError [since it never reaches the Spotify's server]), a typo or bug in the code (ex: referencing a variable that doesn't exist), that would be a normal Python error
    print("My Top Songs:")
    for i, track in enumerate(top_tracks["items"]): # enumerate(iterable, start=#) replaces range(len(iterable))
        if track["artists"] != []: # checks if artists is a blank list (no artists)
            print(f'{i+1}. {track["name"]} by {track["artists"][0]["name"]}') # main artist only *
        else: # you could also use try except withh IndexError (raises when you try to access a list index that doesn't exist like[0] on an empty list)
            print(f'{i+1}. {track["name"]}')
    return top_tracks # hands the raw Spotify data back to the function that it can be grabbed otherwise the data is trapped in the function

def get_top_artists(term_length):
    try:
        top_artists = sp.current_user_top_artists(limit=5, time_range=term_length)
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error connecting to the Spotify API: {e}")
        sys.exit() # you can't subsitute it with return because return just sends a value back while sys exist stops the program entirely
    print("My Top Artists:")
    for i, artist in enumerate(top_artists["items"]):
        print(f'{i+1}. {artist["name"]}')
    return top_artists # you need to return for every function when using panda because you need the actual data to build a table

print() # adds a newline
tracks_data = get_top_tracks(term_length) #  this line calls the function
print()
artists_data = get_top_artists(term_length)

tracks_df = pd.DataFrame(tracks_data["items"]) # searches the top_tracks dictionary for "items" key
tracks_df["artist_name"] = tracks_df["artists"].apply(lambda trackartist: trackartist[0]["name"]) # tracks_df["artist name"] creates a brand new column  called "artist_name"
                                                                     # .apply() runs a function on every value in the col one row at a time and builds a new col from the results
                                                                     # lamba x: ??? a mini one line function, x represents one row's artists value at a time, so when Pandas runs -> row 1, x = row's artists lists, row 2, x = row2 artists list, etc
                                                                     # lambda trackx: is the same as def something(trackx), lambda is useful here because you need a small one time use function that will never be called again
tracks_df = tracks_df[["name", "artist_name", "uri"]] # only keeps name, artist name, and uri
artists_df = pd.DataFrame(artists_data["items"]) # DataFrame (df) is a data structure in Pandas, basically a table with rows and cols (similar to a SQL table), converts the list of track dicitionaries
artists_df = artists_df[["name", "uri"]]  # only keeps name and uri

#print(tracks_df) # basically displays everything SPotify gave us displayed as a table with lots of columns
print(artists_df)
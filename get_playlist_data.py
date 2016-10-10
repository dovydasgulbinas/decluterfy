# shows a user's playlists (need to be authenticated via oauth)
# to call this script use: python get_playlist_data.py 199434580
import pprint
import sys
import os
import subprocess
import time,json

import spotipy

import spotipy.util as util

def show_all_playlist_songs(playlist_id):
    """Takes in playlist ID and returns a list of songs that belong to that playlist."""
    pass


def show_tracks(tracks):
    for i, item in enumerate(tracks):
        track = item['track']

        print( "{}. {} -- {} \t {}".format(i, track['artists'][0]['name'], track['name'], track['id']))
        # print("   %d %32.32s %s \t %s" % (i, track['artists'][0]['name'], track['name'], track['id']))


def get_audio_features(track_ids):
    """Takes a list of song ids and returns their audio features"""
    start = time.time()
    features = sp.audio_features(track_ids)
    delta = time.time() - start
    print(json.dumps(features, indent=4))
    print ("features retrieved in %.2f seconds" % (delta,))


if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Whoops, need your username!")
    print("usage: python user_playlists.py [username]")
    sys.exit()

token = util.prompt_for_user_token(username)

if token:
    sp = spotipy.Spotify(auth=token)
    playlists = sp.user_playlists(username)
    # enums all the playlists that belong to a selected user
    playlists = list(enumerate(playlists['items'],start=0))
    for index, playlist in  playlists:
        print(" #{} \t{} \t{}".format(index, playlist['id'],playlist['name']))

    selected = int(raw_input("Please enter the playlist number with your songs: "))
else:
    print("Can't get token for", username)


# extracting songs from a selected playlist:
playlist = playlists[selected][1]

# this method is designed to actualy get the songs that belong to a user
results = sp.user_playlist(username, playlist['id'], fields="tracks")

tracks = results['tracks']['items']
show_tracks(tracks)

# Grabs a track id and expands it to a list
track_ids =  [track_id['track']['id'] for track_id in tracks]




# print(track_ids)

get_audio_features(track_ids)






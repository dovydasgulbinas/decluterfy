import logging
import pandas
import spotipy.util as util

from spotipy_client import MLearnipy

username = 'coder-hermes'


def print_separator(message='', width=80, separator='=', add_spaces=True):
    print('')
    print(message.center(width, separator))
    print('')


def fetch_token(username='coder-hermes'):
    return util.prompt_for_user_token(username)


def list_playlists_and_chose_one(sp, username):
    """Lists all all playlists user has and returns id of a chosen pl"""
    print_separator()

    playlists = sp.user_playlists(username)
    playlists = list(enumerate(playlists['items'], start=0))
    for index, playlist in playlists:
        print(" #{} \t{} \t{}".format(index, playlist['id'], playlist['name']))

    print_separator()

    no_input = True
    while no_input:
        try:
            selected = int(input("Please enter which playlist you want to Decluterfy:"))
        except Exception as e:
            print("You wrong data input: \"{}\"".format(e))
            no_input = True
        else:
            no_input = False

    print('')
    # list -> enum tuple -> playlist object
    return playlists[selected][1]['id']


def list_playlist_songs(sp, playlist_id ):
    """Uses instance of Mlearnipy to list all songs of a playlist"""
    results = sp.user_playlist(username, playlist_id, fields="tracks")
    tracks = results['tracks']['items']
    for i, item in enumerate(tracks):
        track = item['track']
        print("{}. {} -- {} \t {}".format(i, track['artists'][0]['name'], track['name'], track['id']))


def main():
    token = fetch_token()
    if token:
        sp = MLearnipy(username, auth=token)

        # Lets you co chose decluter pl
        pl_id = list_playlists_and_chose_one(sp, username)

        # TODO: Generate playlist id list without decluter playlist

            # TODO: Fetch i-th playlist songs

            # TODO: Fetch i-th playlist features

            # TODO: Append i-th playlist features to `data` object

        # Print songs contained in a PL
        list_playlist_songs(sp, pl_id)

        # Generate a list of song ids
        song_list = sp.fetch_all_song_ids_from_a_playlist(pl_id)

        # Extract features of those songs
        attrs = ['id', 'duration_ms']
        data = sp.fetch_filtered_features(pl_id, attrs)


        # TODO: DO ML analysis with decision tree




if __name__ == '__main__':
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()

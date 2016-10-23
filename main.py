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
    playlists = sp.user_playlists(username)
    playlists = list(enumerate(playlists['items'], start=0))
    for index, playlist in playlists:
        print(" #{} \t{} \t{}".format(index, playlist['id'], playlist['name']))

    print_separator()
    selected = int(input("Please enter the playlist number with your songs: "))
    print('')
    # list -> enum tuple -> playlist object
    return playlists[selected][1]['id']


def main():
    token = fetch_token()
    if token:
        sp = MLearnipy(username, auth=token)
        pl_id = list_playlists_and_chose_one(sp, username)

        # TODO: Print songs contained in a PL

        # Todo: Generate a list of song ids
        song_list = sp.fetch
        # TODO: Extract features of those songs

        # TODO: Fetch filtered data and parse it to pandas frame

        # TODO: DO ML analysis with decision tree




if __name__ == '__main__':
    logger = logging.getLogger()
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    main()

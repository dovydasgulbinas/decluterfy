import logging
import pandas
import spotipy.util as util

from spotipy_client import MLearnipy

username = 'coder-hermes'


def fetch_token(username='coder-hermes'):
    return util.prompt_for_user_token(username)


def main():
    token = fetch_token()
    if token:
        sp = MLearnipy(username, auth=token)

        # Lets you co chose decluter pl
        # pl_id = list_playlists_and_chose_one(sp, username)

        playlists = sp.list_playlists_and_chose_one(username)
        pl_id = playlists[0]

        # TODO: call fetch filtered features

        # Print songs contained in a PL
        sp.list_playlist_songs(pl_id)

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

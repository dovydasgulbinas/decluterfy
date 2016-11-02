import logging
import pandas
import spotipy.util as util

from spotipy_client import MLearnipy

username = 'coder-hermes'
default_features = ['id', 'energy']


def fetch_token(username='coder-hermes'):
    return util.prompt_for_user_token(username)


def main():
    token = fetch_token()
    if token:
        sp = MLearnipy(username, auth=token)

        features = sp.get_user_song_data_and_playlist_to_decluter(default_features)
        print(features[0])

        sp.print_separator(' All other features ')
        print(features[1])

        # TODO: DO ML analysis with decision tree


if __name__ == '__main__':
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()

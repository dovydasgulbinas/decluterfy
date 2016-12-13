import logging
import spotipy.util as util

from ml_classifier import TestClassifier
from spotipy_client import MLearnipy
from ml_items import DatasetFormer

username = 'coder-hermes'

selected_features = [
    "id",
    "duration_ms",
    "acousticness",
    "tempo",
    "speechiness",
    "mode",
    "danceability",
    "liveness",
    "instrumentalness",
    "loudness",
    "time_signature",
    "energy",
    "valence",
    "key"
]


def fetch_token(username='coder-hermes'):
    return util.prompt_for_user_token(username)


def main():
    token = fetch_token()
    if token:
        sp = MLearnipy(username, auth=token)

        unsorted_playlist, all_playlists = sp.get_target_and_all_other_pls(selected_features)

        # print(unsorted_playlist)

        # sp.print_separator(' All other features ')
        # print(all_playlists)

        # Form a data-frame for ml analysis
        all_pls = DatasetFormer(all_playlists, 'playlist_id')
        unsorted_pls = DatasetFormer(unsorted_playlist, 'playlist_id')

        # data magic
        print(all_pls.target)
        print(all_pls.feature_names)
        print(all_pls.data)
        print(all_pls.target_names)

        print(all_pls.targets_original)

        # TODO: DO ML analysis with decision tree
        test_classifier_obj = TestClassifier


if __name__ == '__main__':
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()

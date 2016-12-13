import logging
import spotipy.util as util

from spotipy_client import MLearnipy
from ml_items import DatasetFormer
from sklearn import tree

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

def predict_playlists_for_unsorted_songs(already_sorted_set, incorrectly_sorted_set):
    decision_tree_classifier = tree.DecisionTreeClassifier()

    songs_not_in_unsorted_playlist = already_sorted_set.data
    playlists_for_sorted_songs = already_sorted_set.target
    decision_tree_classifier.fit(songs_not_in_unsorted_playlist, playlists_for_sorted_songs)

    incorrectly_sorted_songs = incorrectly_sorted_set.data
    playlists_for_unsorted_songs = decision_tree_classifier.predict(incorrectly_sorted_songs)

    return playlists_for_unsorted_songs
    

def main():
    token = fetch_token()
    if token:
        sp = MLearnipy(username, auth=token)

        unsorted_playlist, all_playlists = sp.get_target_and_all_other_pls(selected_features)

        # print(unsorted_playlist)

        # sp.print_separator(' All other features ')
        # print(all_playlists)

        # Form a data-frame for ml analysis
        already_sorted_set = DatasetFormer(all_playlists, 'playlist_id', ['id'])
        incorrectly_sorted_set = DatasetFormer(unsorted_playlist, 'playlist_id', ['id'])

        # playlists_for_unsorted_songs contains ids for playlists to which unsorted songs have to be moved
        # elements of playlists_for_unsorted_songs are in the same order as songs in incorrectly_sorted_set
        playlists_for_unsorted_songs = predict_playlists_for_unsorted_songs(already_sorted_set, incorrectly_sorted_set)



if __name__ == '__main__':
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()

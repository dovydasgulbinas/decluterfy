
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

        # Form a data-frame for ml analysis
        already_sorted_set = DatasetFormer(all_playlists, 'playlist_id', ['id'])
        incorrectly_sorted_set = DatasetFormer(unsorted_playlist, 'playlist_id', ['id'])

        # playlists_for_unsorted_songs contains ids for playlists to which unsorted songs have to be moved
        # elements of playlists_for_unsorted_songs are in the same order as songs in incorrectly_sorted_set
        playlists_for_unsorted_songs = predict_playlists_for_unsorted_songs(already_sorted_set, incorrectly_sorted_set)

        logger.debug("predicted list: {}".format(playlists_for_unsorted_songs))
        logger.debug("names: {}".format(already_sorted_set.target_names))
        logger.debug("ids : {}".format(already_sorted_set.targets_as_ids))

        remaped_playlist = already_sorted_set.remap_list_of_targets_to_initial_value(playlists_for_unsorted_songs)
        logger.debug("Songs remapped: {}".format(remaped_playlist))

        # returns destination playlist from their respective ids
        pl_names = sp.last_fetch_of_all_pls

        sp.print_separator(' Decluter suggestions ')

        # gets all song ids
        song_ids_list = incorrectly_sorted_set.popped_entries['id']

        for index,playlist in list(enumerate(remaped_playlist, start=0)):
            # todo add song names here:
            print('#{}\t{}\t->\t{}'.format(index, song_ids_list[index], sp.find_in_list_of_tuples(pl_names, playlist, 0, 1)))


        

if __name__ == '__main__':
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()

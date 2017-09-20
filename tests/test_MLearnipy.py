from unittest.mock import MagicMock
import pytest
from playlist_mock_60_songs import playlist, mock_audio_features, mock_audio_features_100, \
    mock_audio_features_any
import json

from spotipy_client import MLearnipy

username = 'coder-hermes'
playlist_id = '0tLRGkAKOmWk62BxU6OvW8'
pl_1_song_id = '6O7qFEXmLQcOsV37wrgJDz'
pl_1_song_energy = 0.621
pl_1_song_tempo = 89.926
selected_features = ['id', 'energy', 'tempo']

pl_feats = {}
pl_feats['id'] = [pl_1_song_id] * 60
pl_feats['energy'] = [pl_1_song_energy] * 60
pl_feats['tempo'] = [pl_1_song_tempo] * 60


@pytest.fixture(scope='module')
def token():
    # fake token that spotify api issues
    return 'AQBYJKF4y8_eNFbHurDzttkDawFdDqUaHtvWUnssvaR9MYsqCTzQkakMT5wMA-07ztmNOs99RCRi-E5h2Ndv88BoRCMLWn7BCcQc6V6vJmzKkJxTDChX36WWbo3tyGBvxiZfU15FunPJsuP5c0bjR8oChscnsa3rcOk5CN98K3c2WHep4lXNx82zRX3sb7jtKv9e2B7-sA'


@pytest.fixture(scope='module')
def sp():
    learnipy = MLearnipy(username, auth=token())
    # creates a fake python object for further testing
    learnipy.user_playlist_tracks = MagicMock(return_value=playlist)
    learnipy.audio_features = MagicMock(return_value=mock_audio_features)
    # sets default username for the instance
    learnipy.default_username = username
    return learnipy

new_return = [{"id": [pl_1_song_id] * 60, "energy": [pl_1_song_energy] * 60}, [playlist_id]*60]

@pytest.fixture(scope='module')
def spp():
    learnipy = MLearnipy(username, auth=token())
    # creates a fake python object for further testing
    learnipy.user_playlist_tracks = MagicMock(return_value=playlist)
    learnipy.audio_features = MagicMock(return_value=mock_audio_features)
    learnipy.fetch_filtered_features = MagicMock(
        return_value=new_return)

    # sets default username for the instance
    learnipy.default_username = username
    return learnipy

class TestMLearnipy:
    def test__generate_offsets(self):
        assert sp()._generate_offsets(55) == [0]
        assert sp()._generate_offsets(101) == [0, 100]
        assert sp()._generate_offsets(300) == [0, 100, 200]
        assert sp()._generate_offsets(333) == [0, 100, 200, 300]

    def test__count_number_of_requests(self):
        assert sp()._count_number_of_requests(55) == 1
        assert sp()._count_number_of_requests(333) == 4
        assert sp()._count_number_of_requests(444) == 5

    def test__fetch_number_of_songs_in_playlist(self):
        assert sp()._fetch_number_of_songs_in_playlist(playlist_id) == 60

    def test_fetch_all_song_ids_from_a_playlist_with_60_songs(self):
        # the playlist has 60 identical songs therefore we generate a list w/ 60 of them
        assert sp().fetch_all_song_ids_from_a_playlist(playlist_id)[0] == ([pl_1_song_id] * 60)
        assert sp().fetch_all_song_ids_from_a_playlist(playlist_id)[1] == ([playlist_id] * 60)

    def test_fetch_song_features_with_60_ids(self):
        assert sp()._fetch_song_features(([pl_1_song_id] * 60), print_json=False) == mock_audio_features

    def test_fetch_song_features__with_120_ids(self):
        lp = MLearnipy(username, auth=token())
        # creates a fake python object for further testing
        lp.audio_features = MagicMock(return_value=mock_audio_features_any * 60)

        assert lp._fetch_song_features(([pl_1_song_id] * 120)) == mock_audio_features_any * 120

    def test_fetch_song_features__with_3_ids(self):
        lp = MLearnipy(username, auth=token())
        # creates a fake python object for further testing
        lp.user_playlist_tracks = MagicMock(return_value=playlist)
        lp.audio_features = MagicMock(return_value=mock_audio_features_any * 3)

        assert lp._fetch_song_features(([pl_1_song_id] * 3)) == mock_audio_features_any * 3

    def test_fetch_filtered_features__all_60_ids_match(self):
        fff = sp().fetch_filtered_features(playlist_id, ['id'])[0]
        assert fff['id'] == [pl_1_song_id] * 60

    def test__slice_to_multiple_lists__limit2_odd_number_items(self):
        assert sp()._slice_to_multiple_lists([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]

    def test__slice_to_multiple_lists__limit2_equal_number_items(self):
        assert sp()._slice_to_multiple_lists([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]

    def test__slice_to_multiple_lists__limit3_equal_number_items(self):
        assert sp()._slice_to_multiple_lists([1, 2, 3, 4], 3) == [[1, 2, 3], [4]]

    def test__slice_to_multiple_lists__limit3_odd_number_items(self):
        assert sp()._slice_to_multiple_lists([1, 2, 3, 4, 5], 3) == [[1, 2, 3], [4, 5]]

    def test_get_all_users_songs_w_selected_features(self):
        pls = [playlist_id, playlist_id]
        fs = ['id']

        assert spp(). \
                   get_all_users_songs_w_selected_features(pls, fs)[0] == {"id": [pl_1_song_id] * 120}

    def test_get_all_users_songs_w_selected_features__two_attrs(self):
        def sppp():
            learnipy = MLearnipy(username, auth=token())
            # creates a fake python object for further testing
            learnipy.user_playlist_tracks = MagicMock(return_value=playlist)
            learnipy.audio_features = MagicMock(return_value=mock_audio_features)
            learnipy.fetch_filtered_features = MagicMock(
                return_value=[{'id': [pl_1_song_id] * 2, 'energy': [pl_1_song_energy] * 2}, [playlist_id]*2])

            # sets default username for the instance
            learnipy.default_username = username
            return learnipy

        pls = [playlist_id]
        c = {'id': [pl_1_song_id] * 2, 'energy': [pl_1_song_energy] * 2}
        m = sppp().get_all_users_songs_w_selected_features(pls, ['id', 'energy'])

        assert m[0] == c

    def test_get_all_users_songs_w_selected_features__3_attrs(self):
        def sppp():
            learnipy = MLearnipy(username, auth=token())
            # creates a fake python object for further testing
            learnipy.user_playlist_tracks = MagicMock(return_value=playlist)
            learnipy.audio_features = MagicMock(return_value=mock_audio_features)
            learnipy.fetch_filtered_features = MagicMock(
                return_value=[{'id': [pl_1_song_id] * 2, 'energy': [pl_1_song_energy] * 2,
                              'tempo': [pl_1_song_tempo] * 2}, [playlist_id]*2])

            # sets default username for the instance
            learnipy.default_username = username
            return learnipy

        pls = [playlist_id]
        c = {'id': [pl_1_song_id] * 2, 'energy': [pl_1_song_energy] * 2, 'tempo': [pl_1_song_tempo] * 2}
        m = sppp().get_all_users_songs_w_selected_features(pls, ['id', 'energy', 'tempo'])

        assert m[0] == c

    def test_get_all_users_songs_w_selected_features_n_attrs(self):
        def sppp():
            learnipy = MLearnipy(username, auth=token())
            # creates a fake python object for further testing
            learnipy.user_playlist_tracks = MagicMock(return_value=playlist)
            learnipy.audio_features = MagicMock(return_value=mock_audio_features)
            learnipy.fetch_filtered_features = MagicMock(
                return_value=[{'id': [pl_1_song_id] * 2, 'energy': [pl_1_song_energy] * 2,
                              'tempo': [pl_1_song_tempo] * 2}, [playlist_id]*2])

            # sets default username for the instance
            learnipy.default_username = username
            return learnipy

        pls = [playlist_id, playlist_id]
        c = [{'id': [pl_1_song_id] * 4, 'energy': [pl_1_song_energy] * 4, 'tempo': [pl_1_song_tempo] * 4}, [playlist_id]*4]
        m = sppp().get_all_users_songs_w_selected_features(pls, ['id', 'energy', 'tempo'])

        assert m[0] == c[0]

    def test_find_in_list_of_tuples(self):

       assert MLearnipy.find_in_list_of_tuples([('axa','alfa'),('bxb', 'beta')], 'bxb', 0,1) == 'beta'

    def test_find_in_list_of_tuples_no_value(self):

       assert MLearnipy.find_in_list_of_tuples([('axa','alfa'),('bxb', 'beta')], '', 0,1) == None

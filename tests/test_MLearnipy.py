from unittest.mock import MagicMock
import pytest
from playlist_mock_60_songs import mini_ob, playlist

from spotipy_client import MLearnipy

username = 'coder-hermes'
playlist_id = '0tLRGkAKOmWk62BxU6OvW8'
pl_1_song_id = '6O7qFEXmLQcOsV37wrgJDz'


@pytest.fixture(scope='module')
def token():
    # fake token that spotify api issues
    return 'AQBYJKF4y8_eNFbHurDzttkDawFdDqUaHtvWUnssvaR9MYsqCTzQkakMT5wMA-07ztmNOs99RCRi-E5h2Ndv88BoRCMLWn7BCcQc6V6vJmzKkJxTDChX36WWbo3tyGBvxiZfU15FunPJsuP5c0bjR8oChscnsa3rcOk5CN98K3c2WHep4lXNx82zRX3sb7jtKv9e2B7-sA'


@pytest.fixture(scope='module')
def sp():
    learnipy = MLearnipy(auth=token())
    # creates a fake python object for further testing
    learnipy.user_playlist_tracks = MagicMock(return_value=playlist)
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
        assert sp().fetch_all_song_ids_from_a_playlist(playlist_id) == ([pl_1_song_id]*60)

    def test_fetch_all_song_ids_from_a_playlist_with_120_songs(self):
        assert sp().fetch_all_song_ids_from_a_playlist(playlist_id) == ([pl_2_song_id_1] * 60 + [pl_2_song_id_2] * 60)
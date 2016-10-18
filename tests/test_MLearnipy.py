from unittest.mock import MagicMock
import pytest
import spotipy.util as util

from spotipy_client import MLearnipy

username = '1199434580'
playlist_id = '0tLRGkAKOmWk62BxU6OvW8'


@pytest.fixture(scope='module')
def token():
    #fake token that spotify api issues
    return 'AQBYJKF4y8_eNFbHurDzttkDawFdDqUaHtvWUnssvaR9MYsqCTzQkakMT5wMA-07ztmNOs99RCRi-E5h2Ndv88BoRCMLWn7BCcQc6V6vJmzKkJxTDChX36WWbo3tyGBvxiZfU15FunPJsuP5c0bjR8oChscnsa3rcOk5CN98K3c2WHep4lXNx82zRX3sb7jtKv9e2B7-sA'


@pytest.fixture(scope='module')
def sp():
    from playlist_mock_60_songs import playlist
    learnipy = MLearnipy(auth=token())
    learnipy.user_playlist_tracks(return_value=playlist)
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







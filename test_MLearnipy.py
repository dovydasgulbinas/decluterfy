from unittest import TestCase
import pytest

import spotipy.util as util
from spotipy_client import MLearnipy

username = '1199434580'
playlist_id = '0tLRGkAKOmWk62BxU6OvW8'


@pytest.fixture(scope='module')
def token():
    #return util.prompt_for_user_token(username)
    return 'AQBYJKF4y8_eNFbHurDzttkDawFdDqUaHtvWUnssvaR9MYsqCTzQkakMT5wMA-07ztmNOs99RCRi-E5h2Ndv88BoRCMLWn7BCcQc6V6vJmzKkJxTDChX36WWbo3tyGBvxiZfU15FunPJsuP5c0bjR8oChscnsa3rcOk5CN98K3c2WHep4lXNx82zRX3sb7jtKv9e2B7-sA'


@pytest.fixture(scope='module')
def sp():
    return MLearnipy(default_username=username, auth=token())


class TestMLearnipy(TestCase):
    def test__count_number_of_requests(self):
        assert sp()._count_number_of_requests(55) == 1
        assert sp()._count_number_of_requests(333) == 4
        assert sp()._count_number_of_requests(444) == 5

    def test__generate_offsets(self):
        assert sp()._generate_offsets(55) == [0]
        assert sp()._generate_offsets(101) == [0, 100]
        assert sp()._generate_offsets(300) == [0, 100, 200]
        assert sp()._generate_offsets(333) == [0, 100, 200, 300]

    # def test__get_number_of_songs_in_playlist(self):
    #     assert sp()._fetch_number_of_songs_in_playlist(playlist_id=playlist_id) == 192


        # def test_fetch_all_song_ids_from_a_playlist(self):
        #     self.fail()




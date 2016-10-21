import logging
import json
import time

import spotipy
import spotipy.util as util

logger = logging.getLogger('/.spotipy_client')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class MLearnipy(spotipy.Spotify):
    """Allows to use Spotify API with no hard limitations. It also outputs some data in numpy convienent method"""

    def __init__(self, username, limit=100,  ignore_parent=False, auth=None, requests_session=True,
                 client_credentials_manager=None):
        self._default_username = username
        if not ignore_parent:
            super().__init__(auth, requests_session, client_credentials_manager)
        self.limit = limit
        self._last_playlist = None
        self._last_playlist_id = None

    @property
    def default_username(self):
        return self._default_username

    @default_username.setter
    def default_username(self, username):
        self._default_username = username

    @property
    def last_playlist(self):
        return self._last_playlist

    @last_playlist.setter
    def last_playlist(self, data):
        self._last_playlist = data

    def _count_number_of_requests(self, total_tracks):
        requests_needed = total_tracks // self.limit
        if total_tracks % self.limit != 0:
            # the remainder is not zero meaning that we will need one more request
            requests_needed += 1
            logger.debug("Requests needed: {}".format(requests_needed))
        return requests_needed

    def _generate_offsets(self, total_tracks):
        requests_needed = self._count_number_of_requests(total_tracks)
        result = []
        for request in range(0, requests_needed):
            result.append(self.limit * request)
        return result

    def _fetch_number_of_songs_in_playlist(self, playlist_id):
        self._last_playlist_id = playlist_id
        username = self._default_username
        return self.user_playlist_tracks(username, playlist_id, limit=1)['total']

# todo: refactor me to be used as a general method for multiple requests with arguments [][]
    def fetch_all_song_ids_from_a_playlist(self, playlist_id, username=None):
        """Takes in a playlist id and returns all songs in a given playlist."""
        self._last_playlist_id = playlist_id
        username = self._default_username
        items = []
        num_songs = self._fetch_number_of_songs_in_playlist(playlist_id)
        offsets = self._generate_offsets(num_songs)
        num_requests = self._count_number_of_requests(num_songs)
        for request in range(0, num_requests):
            playlist = self.user_playlist_tracks(username, playlist_id, offset=offsets[request], limit=self.limit)
            self._last_playlist = playlist
            # [333]-> [100, 100, 100, 33], [120] -> [100, 20], [60] -> [60]
            # l ast offset minus the total num of songs

            if request < num_requests - 1:
                songs_per_request = self.limit
            else:
                # makes sure we don't go out of playlist list index
                songs_per_request = num_songs - offsets[request]
            logger.debug("SONGS PER REQUEST: {}".format(songs_per_request))
            for i in range(0, songs_per_request):
                logger.debug("i:{}, spr:{}, rq:{}".format(i, songs_per_request,request))
                playlist_songs = playlist['items'][i]['track']['id']
                items.append(playlist_songs)
        return items

    def _fetch_song_features(self, id_list, print_json = False):
        """Takes a list of song ids and returns list of their audio features"""
        start = time.time()
        features = self.audio_features(id_list)
        delta = time.time() - start
        if print_json:
            print(json.dumps(features, indent=4))
        logger.info("Total {} features retrieved in {} seconds".format(len(features),delta))
        return features['audio_features']

    def fetch_filtered_features(self, playlist_id, selected_features):
        """ Fetches audio features of all songs in a given playlist

        Arguments:
            - playlist_id - a Spotify playlist ID
            - selected_features - a list of strings that can be found in Spotify API audio-features

        Returns dictionary with following structure:
                {
                "id": [1,2, ... nSongs],
                "duration_ms": [1,2, ... nSongs],
                "danceability": [1,2, ... nSongs],
                ...
                }
        """
        selection = {}

        for feature in selected_features:
            selection[feature] = []

        logger.debug(selection)

        id_list = self.fetch_all_song_ids_from_a_playlist(playlist_id)
        all_features = self._fetch_song_features(id_list)
        logger.debug(all_features)

        for songs_features in all_features:
            for index in selection:
                #logger.debug(songs_features)
                #logger.debug(index)
                selection[index].append(songs_features[index])

        logger.debug(selection)
        return selection






def main():
    # username = str(input("Please enter your Spotify ID: eg. 1199434580"))
    username = 'coder-hermes'
    pl_id = '67hGMCzFtkcQEnZyJT4yCJ'
    token = util.prompt_for_user_token(username)
    # Grabs a OAuth token
    if token:
        sp = MLearnipy(auth=token)
        sp.default_username = username
        logger.debug('NUM SONGS: {}'.format(sp._fetch_number_of_songs_in_playlist(pl_id)))
        # sp.fetch_all_song_ids_from_a_playlist(pl_id)
        song_list = sp.fetch_all_song_ids_from_a_playlist(pl_id)
        for song_id in enumerate(song_list):
            logger.debug('{}. {}'.format(song_id[0],song_id[1]))
    else:
        logger.debug('You do not have a token')


if __name__ == '__main__':
    main()

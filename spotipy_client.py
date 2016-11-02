import logging
import json
import time

import spotipy
import spotipy.util as util

logger = logging.getLogger('/.spotipy_client')


class MLearnipy(spotipy.Spotify):
    """Allows to use Spotify API with no hard limitations. It also outputs some data in numpy convienent method"""

    def __init__(self, username, limit=100, ignore_parent=False, auth=None, requests_session=True,
                 client_credentials_manager=None):
        self._default_username = username
        if not ignore_parent:
            super().__init__(auth, requests_session, client_credentials_manager)
        self.limit = limit
        self._last_playlist = None
        self._last_playlist_id = None

    def print_separator(self, message='', width=80, separator='=', add_spaces=True):
        print('')
        print(str(message).center(width, separator))
        print('')

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

    def _slice_to_multiple_lists(self, list, limit=None):
        """Takes in a list and slices it based on the limit RETURNS list of sliced lists

        Arguments:
            - list - any list
            - limit - maximum size on sub-list
        """
        result = []
        if not limit:
            logger.debug("Using default limit")
            limit = self.limit
        else:
            logger.debug("Using limit from the argument")

        l = len(list)

        n_lists = l // limit
        remainder = l % limit

        if (remainder) != 0:
            n_lists += 1

        logger.debug('Number of sub-lists: {}'.format(n_lists))
        # 0 - 1
        # 2 - 3
        # 4 - 5

        for i in range(1, n_lists + 1):
            start = (i - 1) * limit
            end = (i) * limit
            # logger.debug('List iterrator: {} | {}'.format(start, end))
            sub_list = list[start:end]
            result.append(sub_list)
        logger.debug(result)
        return result

    # todo: refactor me to be used as a general method for multiple requests with arguments [][]
    def fetch_all_song_ids_from_a_playlist(self, playlist_id):
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
                # logger.debug("i:{}, spr:{}, rq:{}".format(i, songs_per_request,request))
                playlist_songs = playlist['items'][i]['track']['id']
                items.append(playlist_songs)
        return items

    def _fetch_song_features(self, id_list, print_json=False):
        """Takes a list of song ids and returns list of their audio features"""
        features = []
        sliced_ids = self._slice_to_multiple_lists(id_list)
        start = time.time()

        # todo: must be enumerated of something
        for i in sliced_ids:
            logger.debug('Sliced ids:{}'.format(i))
            features.extend(self.audio_features(i))

        delta = time.time() - start
        if print_json:
            print(json.dumps(features, indent=4))
        logger.info("Total {} features retrieved in {} seconds".format(len(features), delta))
        return features

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
                logger.debug(songs_features)
                logger.debug(index)
                selection[index].append(songs_features[index])

        logger.debug(selection)
        return selection

    def list_playlists_and_chose_one(self, username=None):
        """Lists all all playlists user has and returns id of a chosen pl and a list of all pls"""
        if not username:
            username = self.default_username
        self.print_separator()
        playlists = self.user_playlists(username)
        pl_ids = []
        pl_excluded = []

        playlists = list(enumerate(playlists['items'], start=0))
        for index, playlist in playlists:

            if playlist['owner']['id'] == username:
                print(" #{} \t{} \t{}".format(index, playlist['id'], playlist['name']))
                # generates a list of playlists that only belong to a user
                pl_ids.append(playlist['id'])
            else:
                # prints the playlists that user does not own
                print(" -- \t{} \t{}".format(playlist['id'], playlist['name']))
                pl_excluded.append(index)

        self.print_separator()
        no_input = True
        selected = None
        while no_input:
            try:
                selected = int(input("Please enter which playlist you want to Decluterfy:\n"))
            except Exception as e:
                print('You wrong data input: "{}"\n'.format(e))
                no_input = True
            else:
                if selected not in pl_excluded:
                    no_input = False
                else:
                    logger.debug(selected, pl_excluded)
                    print("The playlist you chose does not belong to you, please chose another \n")
                    no_input = True

        print('')
        logger.debug((playlists[selected][1]['id'], pl_ids))
        # a tuple
        logger.info('Number of fetched playlists: {}'.format(len(pl_ids)))
        return (playlists[selected][1]['id']), pl_ids

    def list_playlist_songs(self, playlist_id):
        """list all songs of a users playlist it uses default id as users id."""
        results = self.user_playlist(self.default_username, playlist_id, fields="tracks")
        tracks = results['tracks']['items']
        for i, item in enumerate(tracks):
            track = item['track']
            print("{}. {} -- {} \t {}".format(i, track['artists'][0]['name'], track['name'], track['id']))

    # FIXME: Refactor to utils class
    def substract_lists(self, x, y):
        """Utility method that makes a sublist of two lists RETURNS: list"""
        z = list(set(x) - set(y))
        return z

    def get_all_users_songs_w_selected_features(self, playlist_ids, selected_features):
        """Gets selected features from all the songs user has. Returns dict

        Arguments:
            - playlist_ids - a list of playlist ids that belong to a user
            - selected_features - a list of strings that can be found in Spotify API audio-features

        Returns dictionary with following structure:
                {
                "id": [1,2, ... nSongs],
                "duration_ms": [1,2, ... nSongs],
                "danceability": [1,2, ... nSongs],
                ...
                }
        """
        result = dict.fromkeys(selected_features, [])
        logger.debug('CALLING: get_all_users_songs_w_selected_features')
        # self.print_separator(selected_features)
        # self.print_separator(result)

        for playlist_id in playlist_ids:
            # returns filtered features of a single playlist
            playlist_features = self.fetch_filtered_features(playlist_id, selected_features)

            for feature in selected_features:
                result[feature] = result[feature] + playlist_features[feature]

        return result

    def get_user_song_data_and_playlist_to_decluter(self, selected_features):
        """Gets all user songs by selected features.

        Arguments:
            - selected_features - a list of strings that can be found in Spotify API audio-features

        Returns a tuple of all playlist features excluding selected, returns selected as a new dict
        (      {
                "id": [1,2, ... xSongs],
                "duration_ms": [1,2, ... xSongs],
                "danceability": [1,2, ... xSongs],
                ...
                },
                     {
                "id": [1,2, ... ySongs],
                "duration_ms": [1,2, ... ySongs],
                "danceability": [1,2, ... ySongs],
                ...
                }


         )
        """

        pls = self.list_playlists_and_chose_one()
        selected_pl = pls[0]  # gets one id of a playlist
        other_pls = self.substract_lists(pls[1], [selected_pl])  # get a list of remaining playlist ids

        spf = self.get_all_users_songs_w_selected_features([selected_pl], selected_features)
        sof = self.get_all_users_songs_w_selected_features(other_pls, selected_features)

        spf_len = len(spf[selected_features[0]])
        sof_len = len(sof[selected_features[0]])
        total_len = sof_len + spf_len

        logger.info('Total features received: {} + {} = {}'.format(spf_len, sof_len, total_len))

        return spf, sof


class DatasetFormer:
    """Takes in a dictionary with lists inside and constructs ML friendly datastructure."""

    def __init__(self, data_frame, target_field):
        """Takes in a datastructure.

        Arguments:
        - data_frame - a data frame that has keys and lists assgined to arbitrary keys e.g:
                    {
                    "height": [1,2, ... n-th_sample],
                    "length": [1,2, ... n-th_sample],
                    "eye_color": [1,2, ... n-th_sample],
                    "target_feature": ['child', 'adult', 'teen']
                    ...
                    }
        - target_field - the label(str)  by which data is classified

        """

        self._data_frame = data_frame

    def generate_objects(self):
        """Runs all methods that are required to generate a ML dataset."""
        pass


def main():
    # username = str(input("Please enter your Spotify ID: eg. 1199434580"))
    pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    main()

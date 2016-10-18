import logging
import json
import spotipy
import spotipy.util as util

logger = logging.getLogger('/.spotipy_client')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class MLearnipy(spotipy.Spotify):
    limit = 100

    def __init__(self, ignore_parent=False, auth=None, requests_session=True,
                 client_credentials_manager=None):
        self._default_username = None
        if not ignore_parent:
            super().__init__(auth, requests_session, client_credentials_manager)


    @property
    def default_username(self):
        return self._default_username

    @default_username.setter
    def default_username(self, username):
        self._default_username = username


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

    def _fetch_number_of_songs_in_playlist(self, playlist_id, username=None):
        if not username:
            username = self.default_username
        return self.user_playlist_tracks(username, playlist_id, limit=1)['total']


    def fetch_all_song_ids_from_a_playlist(self, playlist_id, username=None):
        """Takes in a playlist id and returns all songs in a given playlist."""
        if not username:
            username = self.default_username

        items = []

        num_songs = self._fetch_number_of_songs_in_playlist(playlist_id)
        offsets = self._generate_offsets(num_songs)
        num_requests = self._count_number_of_requests(num_songs)


        for request in range(0, num_requests):
            result.append(self.user_playlist_tracks(username, playlist_id, offset=offsets[request], limit=self.limit)['items'])


        # #prints out all the data:
        #     for i in range(0, num_songs):
        #         id = playlist_tracks_and_meta['items'][i]['track']['id']
        #         song_name = playlist_tracks_and_meta['items'][i]['track']['name']
        #         print(id, song_name)



def main():
    # username = str(input("Please enter your Spotify ID: eg. 1199434580"))
    username = 'coder-hermes'
    pl_id = '6eqDI9wH4BW6lbEckWWAAD'
    token = util.prompt_for_user_token(username)
    # Grabs a OAuth token
    if token:
        sp = MLearnipy(auth=token)
        logger.debug('NUM SONGS: {}'.format(sp._fetch_number_of_songs_in_playlist(pl_id)))
        # sp.fetch_all_song_ids_from_a_playlist(pl_id)
    else:
        logger.debug('You do not have a token')






if __name__ == '__main__':
    main()





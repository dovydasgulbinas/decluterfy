import logging
import spotipy.util as util

from ml_classifier import TestClassifier
from spotipy_client import MLearnipy

username = 'coder-hermes'
default_features = ['id', 'energy']


def fetch_token(username='coder-hermes'):
    return util.prompt_for_user_token(username)


def main():
    token = fetch_token()
    if token:
        sp = MLearnipy(username, auth=token)

        features = sp.get_target_and_all_other_pls(default_features)
        print(features[0])

        sp.print_separator(' All other features ')
        print(features[1])

        # TODO: DO ML analysis with decision tree
        test_classifier_obj = TestClassifier

if __name__ == '__main__':
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()

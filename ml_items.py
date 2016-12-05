import logging

logger = logging.getLogger('.ml-items')

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

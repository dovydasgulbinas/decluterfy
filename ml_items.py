import logging

logger = logging.getLogger('.ml-items')

"""

 - You need to split your data and and targets(classes)
 - Training data must be majority of the data in our dataset
 - We can get a sub list from a list by passing a sublist to the index e.g: superSet[] -> subSet = superSet[[0,1,5]]
 - When extracting test data we must choose both data and their targets

DataStructure should be:
Storage -- list storage below

    data[feature1, feature2, ...] -- list of features -->

        features = [fv1, fv2, fv3]
        features_names = [fn1, fn2] # fn are unique while fv are not

        target[] = [tv1, tv2, tv3]
        target_names[] = [tn1, tn2] # tn are unique while tv are not
"""


class DatasetFormer:
    """Takes in a dictionary with lists inside and constructs ML friendly datastructure."""

    def __init__(self, data_frame, target_keys):
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

    @staticmethod
    def generate_int_id_index(item_list):
        """Takes in a list of data evaluates its uniquines and repopulates it with indexes."""
        result_ids = []
        result_vals = []

        for item in item_list:
            id = item_list.index(item)
            if id not in result_ids:
                result_ids.append(id)
                result_vals.append(item_list[id])

        return result_ids, result_vals

    @staticmethod
    def generate_int_ids_of_items(item_list, unique_list):
        """Takes a list of immutable data and returns a list of their ids.

        :param item_list: list of any immutable data
        :param unique_list: list
        :return: list of ints
        """
        return list(map(lambda x: unique_list.index(x), item_list))

    def generate_objects(self):
        """Runs all methods that are required to generate a ML dataset."""
        pass


def main():
    # username = str(input("Please enter your Spotify ID: eg. 1199434580"))
    pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    main()

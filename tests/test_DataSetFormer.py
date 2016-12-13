import logging
import pytest
from ml_items import DatasetFormer

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

@pytest.fixture(scope='module')
def df():
    data_frame = {
        "a": [1, 2, 3, 4],
        "test_target": ['aa','bb','bb','dd'],
        "c": [11, 12, 13, 14]
    }

    ob = DatasetFormer(data_frame, 'test_target')
    # initialize final structure
    return ob

def df_popped():
    data_frame = {
        "a": [1, 2, 3, 4],
        "test_target": ['aa','bb','bb','dd'],
        "c": [11, 12, 13, 14],
        "e": [55, 66, 77, 88]
    }

    ob = DatasetFormer(data_frame, 'test_target', ["a", "e"])
    # initialize final structure
    return ob


class TestDatasetFormer:
    def test_generate_int_id_index(self):
        assert DatasetFormer.generate_int_id_index(["yes", "no", "maybe", "yes"]) == ([0, 1, 2], ["yes", "no", "maybe"])

    def test_generate_int_id_index_same_items(self):
        assert DatasetFormer.generate_int_id_index(["yes", "yes"]) == ([0], ["yes"])

    def test_generate_int_id_index_same_alternating(self):
        assert DatasetFormer.generate_int_id_index(["yes", "no", "no", "yes"]) == ([0, 1], ["yes", "no"])

    def test_generate_int_ids_of_items(self):
        assert DatasetFormer.generate_int_ids_of_items(["a", "c", "a"], ["a", "c"]) == [0, 1, 0]

    def test_structure_as_row(self):
        dict = {
            "a": [1, 2, 3, 4],
            "b": [9, 8, 7, 6],
            "c": [11, 12, 13, 14]
        }
        assert DatasetFormer.structure_as_row(["a", "b"], dict, 0) == [1, 9]

    def test_structure_as_row_c(self):
        dict = {
            "a": [1, 2, 3, 4],
            "b": [9, 8, 7, 6],
            "c": [11, 12, 13, 14]
        }
        assert DatasetFormer.structure_as_row(["c"], dict, 3) == [14]

    def test__structurize_dict_array_feature_names(self):
        # must be a sorted dict key list
        assert df().feature_names == ['a', 'c']

    def test__structurize_dict_array_target_names(self):
        assert df().target_names == ['aa', 'bb', 'dd']

    def test__structurize_dict_array_targets(self):
        assert df().target == [0,1,1,2]

    def test__structurize_dict_array_data(self):
        assert df().data[0] == [1,11]
        assert df().data[1] == [2,12]
        assert df().data[2] == [3,13]
        assert df().data[3] == [4,14]

    def test__structurize_dict_array_original_targets_are_ok(self):
        assert df().targets_original == ['aa','bb','bb','dd']

    def test__pop_internal_keys__are_removed(self):
        assert df_popped().feature_names == ["c"]

    def test__pop_internal_keys__dict_is_popped_correctly(self):
        popped = {
            "a": [1, 2, 3, 4],
            "e": [55, 66, 77, 88]
        }

        assert df_popped().popped_entries == popped

    def test__remap_list_of_targets_to_initial_value(self):
        ttl = ['aa', 'bb', 'bb', 'dd']
        tti = [1,2,2,3]
        result = df().remap_list_of_targets_to_initial_value(tti)

        assert result == ttl










    





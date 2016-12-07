import pytest
from ml_items import DatasetFormer

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


    





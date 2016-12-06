import pytest
from ml_items import DatasetFormer


@pytest.fixture(scope='module')
def df():
    data_frame = {
        "color": ['red', 'green', 'blue'],
        "genre": ['Classical', 'Electro', 'Rock'],
        "size": [1, 2, 3],
        "target": ['BAD', 'OK', 'OK']
    }
    ob = DatasetFormer(data_frame, 'target')
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

    def test__structurize_dict_array(self):
        # how full route and see if data is prepared correctly a final method
        assert 5 == 9

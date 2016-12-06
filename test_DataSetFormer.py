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

import pytest
from spotipy_client import DatasetFormer


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


# class TestDatasetFormer:
#     def test_generate_objects(self):
#         assert df().generate_objeycts()


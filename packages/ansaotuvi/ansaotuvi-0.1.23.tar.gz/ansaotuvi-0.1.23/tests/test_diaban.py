import unittest

import pytest

from ansaotuvi.DiaBan import diaBan


@pytest.mark.diaban
class TestDiaBan(unittest.TestCase):
    def test_diaban_is_initializable(self):
        tmpThienCan = {
            "id": 1,
            "chuCaiDau": "G",
            "tenCan": "Giáp",
            "nguHanh": "M",
            "nguHanhID": 2,
            "vitriDiaBan": 3,
            'amDuong': 1
        }
        diaban = diaBan(1, 10, tmpThienCan)
        if diaban:
            self.assertTrue(diaban)

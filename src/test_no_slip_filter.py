
import pytest
import numpy as np
from no_slip_filter import NoSlipFilter
from no_slip_filter import Create_Mask


@pytest.fixture
def no_slip_filter_instance():
    return NoSlipFilter()


def test_test():
    test_int = 1
    assert test_int == 1


def test_fail():
    test_int =2
    assert test_int == 2


# test that the no slip filter in initalized
def test_initialization(no_slip_filter_instance):

    assert no_slip_filter_instance is not None


class Mesh:
    def __init__(self, points):
        self.Points = points


def test_create_mask():
    Volume_Mesh = Mesh(np.array(
        [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]
    ))
    Wall_Mesh = Mesh(np.array([[1.0, 2.0, 3.0], [7.0, 8.0, 8.0]]))

    mask = Create_Mask(Volume_Mesh, Wall_Mesh)

    expected_mask = np.array([True, False, False])

    assert np.array_equal(mask, expected_mask)


import pytest
# from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase
from no_slip_filter import NoSlipFilter


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

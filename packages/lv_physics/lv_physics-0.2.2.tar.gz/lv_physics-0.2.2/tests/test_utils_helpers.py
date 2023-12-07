import numpy as np
import pytest

from lv_physics.utils.helpers import ComplexUnsupportedError, complex_error_message


def test_complex_error_message():
    """ """
    input_1 = 1 + 2.0j
    input_2 = np.array([3, 4.0j])

    error_message = "Unsupported complex inputs: {'input_1': (1+2j), 'input_2': array([3.+0.j, 0.+4.j])}"

    assert complex_error_message(input_1=input_1, input_2=input_2) == error_message

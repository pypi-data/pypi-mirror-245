import re
from dataclasses import Field, dataclass
from datetime import datetime, timezone
from typing import Callable

import numpy as np
import pytest
from dataclasses_json import dataclass_json
from numpy import array, complex_, float_, int_, ndarray
from numpy.typing import NDArray

from lv_physics.utils.dataclass_helpers import (
    array_factory,
    array_field,
    array_zero_factory,
    complex_array_decoder,
    complex_array_encoder,
    complex_array_field,
    datetime_factory,
    datetime_field,
    datetime_zero_factory,
)


# ----------------------------------------------------------------------------------------------------------------------


def test_datetime_factory():
    """
    Tests the datetime factory functions.
    """
    # make sure that the factories are themselves functions
    assert isinstance(datetime_factory(1970, 1, 1), Callable)
    assert isinstance(datetime_zero_factory, Callable)

    # make sure they produce the right values
    dttm = datetime_factory(1970, 1, 1)()
    dttm_zero = datetime_zero_factory()

    assert isinstance(dttm, datetime)
    assert isinstance(dttm_zero, datetime)
    assert dttm.timestamp() == 0.0
    assert dttm_zero.timestamp() == 0.0


def test_datetime_field():
    """
    Tests the datetime field function.
    """
    datetime_field_with_init = datetime_field(default_factory=datetime_zero_factory)
    datetime_field_no_init = datetime_field(default_factory=False)

    assert isinstance(datetime_field_with_init, Field)
    assert isinstance(datetime_field_no_init, Field)

    @dataclass_json
    @dataclass
    class TestObject:
        dttm: datetime = datetime_field(default_factory=datetime_zero_factory)

    test_obj = TestObject.from_dict({"dttm": "1970-01-01T00:00:00+00:00"})

    assert isinstance(test_obj.to_dict(), dict)
    assert isinstance(test_obj.dttm, datetime)


def test_array_factory():
    """
    Tests the array factory functions.
    """
    vector_zero_factory = array_zero_factory(shape=3, dtype=float_)
    assert isinstance(vector_zero_factory, Callable)

    nvector_zero_factory = array_zero_factory(shape=(5, 3), dtype=float_)
    assert isinstance(nvector_zero_factory, Callable)

    complex_vector_factory = array_zero_factory(shape=3, dtype=complex_)
    assert isinstance(complex_vector_factory, Callable)


def test_array_field():
    """
    Tests the array field function.
    """
    # TEST FOR A SINGLE VECTOR FIELD

    vector_zero_factory = array_zero_factory(shape=3, dtype=float_)
    vector_field_with_init = array_field(default_factory=vector_zero_factory)
    vector_field_no_init = array_field(default_factory=None)

    assert isinstance(vector_field_with_init, Field)
    assert isinstance(vector_field_no_init, Field)

    @dataclass_json
    @dataclass
    class TestObject:
        vec: NDArray = array_field(default_factory=vector_zero_factory)

    test_obj = TestObject.from_dict({"vec": [2.0, 3.0, 1.0]})

    assert isinstance(test_obj.to_dict(), dict)
    assert isinstance(test_obj.vec, ndarray)

    # TEST FOR AN N-VECTOR FIELD

    nvector_zero_factory = array_zero_factory(shape=(5, 3), dtype=float_)
    nvector_field_with_init = array_field(default_factory=nvector_zero_factory)
    nvector_field_no_init = array_field(default_factory=None)

    assert isinstance(nvector_field_with_init, Field)
    assert isinstance(nvector_field_no_init, Field)

    @dataclass_json
    @dataclass
    class TestObject:
        nvec: NDArray = array_field(default_factory=nvector_zero_factory)

    test_obj = TestObject.from_dict({"nvec": [[2.0, 3.0, 1.0], [1.0, 1.0, 1.0]]})

    assert isinstance(test_obj.to_dict(), dict)
    assert isinstance(test_obj.nvec, ndarray)


def test_complex_array_field():
    """
    Tests the complex vector dataclass field function.
    """
    # TEST FOR A SINGLE COMPLEX VECTOR FIELD

    complex_vector_factory = array_zero_factory(shape=3, dtype=complex_)
    complex_vector_field_with_init = complex_array_field(default_factory=complex_vector_factory)
    complex_vector_field_no_init = complex_array_field(default_factory=None)

    assert isinstance(complex_vector_field_with_init, Field)
    assert isinstance(complex_vector_field_no_init, Field)

    @dataclass_json
    @dataclass
    class TestObject:
        vec: NDArray = complex_array_field(default_factory=complex_vector_factory)

    test_obj = TestObject.from_dict({"vec": ["2.+1.j", "3.", "1.j"]})

    assert isinstance(test_obj.to_dict(), dict)
    assert isinstance(test_obj.vec, ndarray)

    # TEST FOR AN N-VECTOR FIELD

    complex_nvector_factory = array_zero_factory(shape=(5, 3), dtype=complex_)
    complex_nvector_field_with_init = array_field(default_factory=complex_nvector_factory)
    complex_nvector_field_no_init = array_field(default_factory=None)

    assert isinstance(complex_nvector_field_with_init, Field)
    assert isinstance(complex_nvector_field_no_init, Field)

    @dataclass_json
    @dataclass
    class TestObject:
        nvec: NDArray = array_field(default_factory=complex_nvector_factory)

    test_obj = TestObject.from_dict({"nvec": [["2.+1.j", "3.", "1.j"], ["2.+1.j", "3.", "1.j"]]})

    assert isinstance(test_obj.to_dict(), dict)
    assert isinstance(test_obj.nvec, ndarray)

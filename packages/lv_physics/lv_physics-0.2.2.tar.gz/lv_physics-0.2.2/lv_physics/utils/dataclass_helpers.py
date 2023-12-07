from dataclasses import field
from datetime import datetime, timezone
from typing import Callable

from dataclasses_json import config
from marshmallow import fields
from numpy import array, complex_, ndarray, str_, zeros


def array_factory(obj, dtype):
    """
    Produces a factory, a callable which instantiates the provided obj as an array.
    """
    return lambda: array(obj, dtype=dtype)


def array_zero_factory(shape, dtype):
    """
    Produces a factory, a callable which instantiates the provided obj as a zero valued array.
    """
    return lambda: zeros(shape, dtype=dtype)


def datetime_factory(*args):
    return lambda: datetime(*args, tzinfo=timezone.utc)


def datetime_zero_factory():
    return datetime(1970, 1, 1, tzinfo=timezone.utc)


def complex_array_encoder(complex_array):
    """
    Returns an NDArray[complex_] object from a list object with complex convertable entries.

    :param complex_array: an NDArray[complex_] to be converted
    :returns: a list (of lists if necessary) of complex formatted strings
    """
    return array(complex_array, dtype=str_).tolist()


def complex_array_decoder(complex_list):
    """
    Returns an NDArray[complex_] object from a list object with complex convertable entries.

    :param complex_list: a list (of lists if necessary) of complex formatted strings
    :returns: an NDArray[complex_] to be converted
    """
    return array(complex_list, dtype=complex_)


def datetime_field(default_factory: Callable = None):
    """
    Returns a dataclass field for a datetime object.

    :param default_factory: a function to initialize the attribute
    """
    datetime_config = config(
        encoder=datetime.isoformat,
        decoder=datetime.fromisoformat,
        mm_field=fields.DateTime(format="iso"),
    )

    if default_factory is None:
        return field(metadata=datetime_config)
    else:
        return field(metadata=datetime_config, default_factory=default_factory)


def array_field(default_factory: Callable = None):
    """
    Returns a dataclass field for a vector object of type (NDArray[float_]).

    :param default_factory: a function to initialize the attribute
    """
    vector_config = config(encoder=ndarray.tolist, decoder=array)

    if default_factory is None:
        return field(metadata=vector_config)
    else:
        return field(metadata=vector_config, default_factory=default_factory)


def complex_array_field(default_factory: Callable = None):
    """
    Returns a dataclass field for a complex vector object of type (NDArray[complex_]).

    :param default_factory: a function to initialize the attribute
    """
    vector_config = config(encoder=complex_array_encoder, decoder=complex_array_decoder)

    if default_factory is None:
        return field(metadata=vector_config)
    else:
        return field(metadata=vector_config, default_factory=default_factory)

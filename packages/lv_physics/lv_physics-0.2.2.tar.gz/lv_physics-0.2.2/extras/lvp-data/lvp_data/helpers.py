from typing import List, Tuple, Union

from numpy import ndarray


def match_str(arg: Union[int, Tuple[int, ...]]) -> str:
    """
    Creates an appropriate string for a 'WHERE' statement based on the input type.
    """
    match_str = None

    if isinstance(arg, int):
        match_str = f"= {arg}"
    elif isinstance(arg, (list, tuple, ndarray)):
        match_str = f"IN {arg}"

    return match_str

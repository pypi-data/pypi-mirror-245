import numpy as np


class ComplexUnsupportedError(AssertionError):
    """
    Custom error for lv_common.vectors functions to raise when receiving unsupported complex dtypes.
    """

    def __init__(self, message, error):
        super().__init__(message)
        self.error = error


def complex_error_message(**kwargs):
    """
    Returns the unsupported complex input string for all objects given in the kwargs which are complex.  Any arguments
    or quantities of a function which should break if complex should be provided to this function as a kwarg.
    """
    complex_inputs = {k: v for k, v in kwargs.items() if np.iscomplexobj(v)}

    return f"Unsupported complex inputs: { complex_inputs }"


def progress_bar(n, N, bar_length=40):
    """
    prints a progress bar.
    """
    p = int(bar_length * n / N) + 1
    q = bar_length - p

    print(f"progress: [{p * '=' + '>' + q * ' '}]", end="\r")

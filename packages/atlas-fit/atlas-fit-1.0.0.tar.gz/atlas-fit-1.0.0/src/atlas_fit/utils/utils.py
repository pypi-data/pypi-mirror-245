"""
Module for utility methods
"""
from typing import Union
import numpy as np


def parse_shape(string: str) -> tuple:
    """
    Parsing a python-like slice input string (e.g., [1,2:5]) to slices
    for using with numpy arrays.
    """
    string = string.strip("[]")
    return tuple(to_slice(d) if ':' in d else to_int(d) for d in string.split(","))


def to_slice(string: str, delimiter: str = ':') -> slice:
    """:returns: a slice with start and stop taken from the string, seperated by delimiter, e.g. 3:7"""
    start, stop = string.split(delimiter)
    return slice(to_int(start), to_int(stop))


def to_int(string: str) -> Union[int, None]:
    """:returns: an integer if the string is numeric"""
    if string.strip().isnumeric():
        return int(string)
    return None


def find_nearest(array: np.array, value: float) -> float:
    array = np.asarray(array)
    return float(array[(np.abs(array - value)).argmin()])

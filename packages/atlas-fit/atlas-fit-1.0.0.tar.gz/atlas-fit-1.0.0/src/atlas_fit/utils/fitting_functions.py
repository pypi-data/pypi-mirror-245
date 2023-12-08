from typing import Union

import numpy as np


def gaussian(x: Union[np.array, float], amplitude: float, mean: float, sigma: float) -> Union[np.array, float]:
    """
    Fitting function for [Gaussian normal distribution](https://en.wikipedia.org/wiki/Normal_distribution).

    Signature follows requirements for `scipy.optimize.curve_fit` callable,
    see [curve_fit documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html).
    It takes the independent variable as the first argument and the parameters to fit as separate remaining arguments.

    ### Params
    - `x` The free variable
    - `amplitude` The amplitude
    - `mean` The center of the peak
    - `sigma` The standard deviation (The width of the peak)

    ### Returns
    The y value
    """
    return amplitude * np.exp(-np.power(x - mean, 2.) / (2 * np.power(sigma, 2.)))


def overlapping_gaussian(x, *args):
    """
    Fitting function for data with (potentially) overlapping gaussian shaped peaks.
    Parameters are similar to `gaussian`. Always only one x, but the other params may come in packs of three.

    See `gaussian` for further details
    """
    return sum(gaussian(x, *args[i*3:(i+1)*3]) for i in range(int(len(args) / 3)))

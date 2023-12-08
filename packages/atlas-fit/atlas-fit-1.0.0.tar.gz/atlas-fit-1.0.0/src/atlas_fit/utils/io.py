"""
Module for I/O interaction
"""
import logging
from contextlib import contextmanager

import numpy as np
from astropy.io import fits


log = logging.getLogger()


def read_fits_data(path: str, hdu: int = 0) -> np.array:
    """Read the data part of a fits file from the given path"""
    log.info('Reading: "%s"', path)
    with fits.open(path) as hdul:
        hdul[hdu].verify('silentfix')
        return hdul[hdu].data


@contextmanager
def read_hdu(path: str, hdu: int = 0) -> fits.hdu:
    """Read the full HDU from fits file"""
    log.info('Reading: "%s"', path)
    with fits.open(path) as hdul:
        hdul[hdu].verify('silentfix')
        yield hdul[hdu]

import os
import numpy as np

# Root directory of the package
ROOT_DIR = os.path.abspath(os.path.dirname(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

# Conversion factors

M2NM = 1e+9
"""Meter [m] to Nano Meter [nm] conversion factor"""

UM2NM = 1e-3
"""micro meter [um] to nano meter [nm] conversion factor"""

ANGSTROM2NM = 1 / 10
"""Angstrom [A] to nano meter [nm] conversion factor"""

NM2ANGSTROM = 10
"""nano meter [nm] to Angstrom [A] conversion factor"""

FWHM2SIGMA = np.sqrt(8 * np.log(2))
"""Convert the FWHM of a gaussian to sigma"""

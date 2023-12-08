#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Base class for an atlas implementation

@author: hoelken
"""
from typing import Union

import numpy as np
from copy import copy


class Atlas:
    """
    Base class for an atlas implementation
    """

    def __init__(self, start: float, stop: float):
        #: Wavelength to start to read from
        self.start = start
        #: Wavelength to read to
        self.stop = stop
        # Containers for the loaded atlas
        #: Wavelength
        self.wl = []
        #: Intensity
        self.intensity = []
        #: (Quasi-) continuum
        self.continuum = []
        self._wl_poly = None

    def load(self):
        """Read the content of the atlas to mem"""
        raise NotImplementedError('Derived class does not implement this method.')
        pass

    def convert_wl(self, factor) -> None:
        """
        Convert the WL by the given factor.
        Default is Angstrom, use `factor=1/10` to convert to [nm].
        """
        self.wl = np.array(self.wl)
        self.wl = self.wl * factor

    def __len__(self) -> int:
        return len(self.wl)

    def copy(self):
        return copy(self)

    def wl_func(self, px_value: Union[float, np.array]) -> Union[float, np.array]:
        if self._wl_poly is None:
            self._wl_poly = np.polynomial.Polynomial.fit(np.arange(len(self.wl)), self.wl, deg=9)

        return self._wl_poly(px_value)

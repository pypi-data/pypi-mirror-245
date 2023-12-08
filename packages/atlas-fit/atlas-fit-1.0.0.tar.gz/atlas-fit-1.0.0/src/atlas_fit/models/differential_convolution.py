from dataclasses import dataclass

import numpy as np
from scipy.signal import fftconvolve

from ..base.constants import FWHM2SIGMA
from ..utils.fitting_functions import gaussian


@dataclass
class FWHM:
    data: float
    atlas: float
    _delta: float = None

    @property
    def delta(self) -> float:
        if self._delta is None:
            self._delta = np.abs(self.data - self.atlas)
        return self._delta


class DifferentialSpectralPSF:

    def __init__(self, fwhm: FWHM):
        self.fwhm = fwhm
        self._delta_spsf = None

    def convolve(self, data: np.array, wl: np.array):
        self._gen_convolution_function(wl)
        return self._convolve_data(data)

    def _gen_convolution_function(self, wl: np.array):
        xes = np.arange(len(wl))
        dispersion = (wl[1:] - wl[:-1]).mean()
        sigma = self._fwhm2std() / dispersion
        self._delta_spsf = gaussian(xes, mean=len(wl)/2, sigma=sigma, amplitude=1)
        amp = 1/np.sum(self._delta_spsf)
        self._delta_spsf = gaussian(xes, mean=len(wl)/2, sigma=sigma, amplitude=amp)

    def _convolve_data(self, data: np.array) -> np.array:
        convolved = fftconvolve(data, self._delta_spsf, mode='same')
        return convolved * np.mean(data) / np.mean(convolved)

    def _fwhm2std(self):
        # Function to convert FWHM (Gamma) to standard deviation (sigma)
        return self.fwhm.delta / FWHM2SIGMA

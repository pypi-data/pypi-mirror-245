from __future__ import annotations

import logging

import numpy as np
from scipy import signal
from scipy.ndimage import zoom
from scipy.interpolate import UnivariateSpline
from spectroflat.fitting.line_fit import LineFit

from ..base.config import Fitting

log = logging.getLogger()


class Spectrum:
    """
    The Spectrum class allows to model certain properties of a solar intensity spectrum.
    - fitting the continuum gradient
    - correct for fitted continuum
    - detecting line cores of prominent absorption lines.
    """

    def __init__(self, spectrum: np.array, peaks: list = None, window: int = 0):
        self._window = window // 2
        self.data = spectrum
        self.continuum_fit = None
        self.peaks = peaks
        self.lines = []
        self.bad_lines = []
        self._cont_points = []
        self._xes = np.arange(len(spectrum))
        self.continuum_correction = np.ones(len(spectrum))

    def prepare(self, stray_light: float, fitting: Fitting = Fitting()):
        self.apply_lowpass_filter_correction(fitting)
        self.apply_offset(stray_light)
        self.normalize()
        self.straighten(fitting)
        self.fit_lines()

    def apply_lowpass_filter_correction(self, fitting: Fitting = Fitting()) -> np.array:
        if fitting.continuum_filter_order is None:
            return

        sos = signal.butter(fitting.continuum_filter_order, 4 / len(self.data), btype='lowpass', output='sos')
        zi = signal.sosfilt_zi(sos)
        filtered = signal.sosfilt(sos, self.data, zi=self.data[0] * zi)
        self.continuum_correction = filtered[0] / np.mean(filtered[0])
        self.data = np.true_divide(self.data.astype('float32'), self.continuum_correction.astype('float32'),
                                   out=self.data.astype('float32'), where=self.continuum_correction != 0,
                                   dtype='float64')

    def apply_offset(self, percent: float):
        self.data -= self.data.mean() * percent / 100

    def normalize(self, mean=1):
        self.data = (self.data / self.data.mean()) * mean

    def straighten(self, fitting: Fitting = Fitting(), correction: np.array = None) -> Spectrum:
        self.fit_continuum(fitting)
        self._adjust_height(correction)
        return self

    def fit_continuum(self, fitting: Fitting = Fitting()) -> Spectrum:
        self._guess_continuum_points(fitting.continuum_points)
        self._filter_continuum_points()
        self._interp_continuum(fitting.continuum_spline_degree, fitting.continuum_spline_smoothing)
        return self

    def _guess_continuum_points(self, num: int = 120) -> None:
        if len(self._cont_points) > 0:
            return

        s = len(self.data) // num
        for i in range(0, len(self.data), s):
            sp = self.data[i:i + s]
            p = np.argmax(sp)
            self._cont_points.append(p + i)

    def _interp_continuum(self, spline_deg: int = 5, smoothing: int = 1) -> None:
        values = self._mean_continuum_values()
        if values:
            self.continuum_interpolation = UnivariateSpline(self._cont_points, values, k=spline_deg, s=smoothing)
        else:
            self.continuum_interpolation = np.poly1d(1.0000000000001)

    def _filter_continuum_points(self, gradient_degree: int = 11, max_deviation: float = 0.09) -> None:
        values = self._mean_continuum_values()
        continuum_fit = np.polynomial.Polynomial.fit(self._cont_points, values, gradient_degree)
        yes = continuum_fit(self._xes)
        self._cont_points = [p for i, p in enumerate(self._cont_points) if values[i] > yes[p] - yes[p] * max_deviation]

    def _mean_continuum_values(self):
        return [self.data[max(0, p - 1):min(p + 2, len(self.data))].mean() for p in self._cont_points]

    def _adjust_height(self, correction: np.array = None) -> None:
        y_values = self.fitted_continuum(self._xes)
        if correction is not None:
            y_values += zoom(correction, len(self.data) / len(correction), order=5)
        self.continuum_correction *= y_values
        self.data /= y_values

    def fitted_continuum(self, xes: np.array) -> np.array:
        return self.continuum_interpolation(xes)

    def fit_lines(self) -> Spectrum:
        row = self.data * -1
        row = row - row.min()
        self.lines = [self.fit_peak(p, row) for p in self.peaks]
        self.bad_lines = [i for i, v in enumerate(self.lines) if v is None]
        return self

    def fit_peak(self, peak: int, row: np.array):
        a, b = self._get_borders(peak, 2)
        peak = a + np.argmax(row[a:b])
        for m in [1, 2]:
            a, b = self._get_borders(peak, m)
            lf = LineFit(np.arange(a, b), row[a:b], error_threshold=0.6)
            try:
                lf.run()
                return lf.max_location
            except RuntimeError:
                pass
        return None

    def _get_borders(self, peak: int, multi: int):
        return int(max(0, peak - (self._window * multi))), int(min(len(self), peak + (self._window * multi) + 1))

    def __len__(self) -> int:
        return len(self.data)

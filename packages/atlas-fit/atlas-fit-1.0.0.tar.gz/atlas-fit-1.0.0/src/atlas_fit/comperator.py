from __future__ import annotations

import logging
import warnings

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.ndimage import zoom
from scipy.optimize import brute
from scipy.signal import resample

from .atlantes import atlas_factory
from .base.config import Config
from .base.constants import NM2ANGSTROM
from .models import Spectrum
from .models.differential_convolution import FWHM, DifferentialSpectralPSF
from .models.model_convolution import ModelPSF

log = logging.getLogger()


class Comperator:
    """
    Base class for Atlas and spectral comparison.
    Performs the atlas fit based on the given configuration.
    - Continuum gradient correction
    - Wavelength calibration
    """

    def __init__(self, spectrum: np.array, config: Config, points: dict):
        self._conf = config
        self._points = points
        self.spectrum = Spectrum(spectrum, points['data'], config.input.line_window)
        self.asp = None
        self.atlas = None
        self.dispersion = None
        self._new_xes = None
        self.deg = 0

    def run(self) -> Comperator:
        self._prepare_spectrum()
        self._load_atlas()
        self._find_lines_in_atlas()
        self._fit_dispersion()
        self._correct_data_continuum()
        return self

    def _prepare_spectrum(self) -> None:
        self.spectrum.prepare(self._conf.input.stray_light, self._conf.fitting)
        if self._conf.debug:
            self._debug_plot_fits('data')

    def _load_atlas(self) -> None:
        self._read_atlas()
        self._convolute_atlas()
        self._add_stray_light()

    def _read_atlas(self) -> None:
        log.info('Reading: %s from (%s)', (self._conf.input.wl_start, self._conf.input.wl_end), self._conf.atlas)
        self.atlas = atlas_factory(self._conf.atlas.key, self._conf.input.wl_start, self._conf.input.wl_end,
                                   conversion=NM2ANGSTROM)

    def _convolute_atlas(self):
        self._conf.atlas.compute_fwhm(self._conf.input.central_wl)
        if self._conf.input.model_psf is not None:
            log.info('Using PSF Model to prime atlas')
            mpsf = ModelPSF(self._conf.input.model_psf)
            self.atlas.intensity = mpsf.convolve(self.atlas.intensity, self.atlas.wl)
            return

        if None in [self._conf.atlas.fwhm, self._conf.input.fwhm]:
            log.warning('No differential convolution data (FWHM for atlas and/or data) not configured.')
            log.info('skipping differential convolution...')
            return

        fwhm = FWHM(atlas=self._conf.atlas.fwhm, data=self._conf.input.fwhm)
        log.info('Convoluting atlas with a gaussian-function with FWHM %.2e', fwhm.delta)
        spsf = DifferentialSpectralPSF(fwhm)
        self.atlas.intensity = spsf.convolve(self.atlas.intensity, self.atlas.wl)

    def _add_stray_light(self):
        self.atlas.intensity + (self.atlas.intensity.mean() * self._conf.input.stray_light)

    def _find_lines_in_atlas(self) -> None:
        wls = list(self.atlas.wl)
        peaks = [wls.index(p) for p in self._points['atlas']]
        self.asp = Spectrum(self.atlas.intensity, peaks, self._conf.atlas.line_window)
        self.asp.fit_lines()
        if self._conf.debug:
            self._debug_plot_fits('Atlas')

    def _fit_dispersion(self) -> None:
        if self.asp.bad_lines or self.spectrum.bad_lines:
            self._clean_lines()
        self._peaks_sp = np.array(self.spectrum.lines)[:len(self.asp.lines)].astype(float)
        self._peaks_asp = np.array(self.asp.lines)[:len(self.spectrum.lines)].astype(float)
        log.info('%d data peaks and %d atlas peaks left...', len(self._peaks_sp), len(self._peaks_asp))
        self._gen_reference()
        self._find_fit()
        log.info('Best dispersion fit found for polynomial order %d as:\n %s', self.deg, self.dispersion)

    def _gen_reference(self):
        self._ref = resample(self.asp.data, len(self.spectrum.data))
        self._wl = zoom(self.atlas.wl, len(self.spectrum.data) / len(self.asp.data), order=5)

    def _clean_lines(self) -> None:
        nans = list(np.argwhere(np.isnan(np.array(self.asp.lines).astype(float))))
        nans = [int(n) for n in nans]
        nans.sort(reverse=True)
        for nan in nans:
            self.asp.lines.pop(nan)
            self.spectrum.lines.pop(nan)
        nans = list(np.argwhere(np.isnan(np.array(self.spectrum.lines).astype(float))))
        nans = [int(n) for n in nans]
        nans.sort(reverse=True)
        for nan in nans:
            if nan < len(self.asp.lines):
                self.asp.lines.pop(nan)
            if nan < len(self.spectrum.lines):
                self.spectrum.lines.pop(nan)

    def _find_fit(self):
        with warnings.catch_warnings():
            # We do a brute force approach for the best deg. Thus, we can safely ignore RankWarnings.
            warnings.filterwarnings('ignore', message='.*The fit may.*')
            res = brute(self._chi2_error,
                        (slice(self._conf.fitting.dispersion_min_degree,
                               self._conf.fitting.dispersion_max_degree + 1, 1),))
            self.deg = int(np.round(res))
            self._polyfit(self.deg)

    def _chi2_error(self, deg: tuple) -> float:
        try:
            self._polyfit(int(np.round(deg)))
            return self._compute_fit_error()
        except (TypeError, ValueError) as e:
            log.error('Error on deg=%d:\n%s', deg, e)
            return np.infty

    def _polyfit(self, deg: int):
        self.dispersion = np.polynomial.Polynomial.fit(self._peaks_sp, self._peaks_asp, deg)

    def _compute_fit_error(self):
        current = self._current_profile()
        return self._error_without_masked_lines(current)

    def _current_profile(self):
        xes = np.arange(len(self.spectrum.data))
        current = self.warp_profile(self.spectrum.data, xes)
        return current / np.mean(current)

    def _error_without_masked_lines(self, current: np.array) -> float:
        error = (current - self._ref) ** 2 / self._ref ** 2
        win = self._conf.input.line_window // 2
        for line in self._conf.fitting.stray_light_ignored_lines:
            pos = np.argmin(np.abs(self._wl - float(line)))
            start = max(0, pos - win)
            stop = min(pos + win, len(self._wl))
            error[start:stop] = error[start:stop] / 2
        return float(np.sum(error))

    def _correct_data_continuum(self):
        self.asp.fit_continuum(self._conf.fitting)
        yes = self.asp.fitted_continuum(np.arange(len(self.asp.data)))
        correction = self.atlas.continuum - yes

        mean = self.atlas.intensity.mean()
        self.spectrum.normalize(mean=mean)
        self.spectrum.straighten(self._conf.fitting, correction=correction)
        self.spectrum.normalize(mean=mean)

    def warp_profile(self, profile: np.array, xes: np.array) -> np.array:
        return CubicSpline(self.new_data_xes, profile)(xes)

    @property
    def new_data_xes(self):
        xes = np.arange(len(self.spectrum.data))
        new_xes = self.dispersion(xes)
        self._new_xes = np.maximum.accumulate(
            (new_xes - new_xes.min()) / (new_xes.max() - new_xes.min()) * np.max(xes))

        return self._new_xes

    def _debug_plot_fits(self, what: str):
        data = self.spectrum if what == 'data' else self.asp
        nlines = len(data.peaks)
        fig, ax = plt.subplots(nrows=4, ncols=(nlines // 4) + (nlines % 4), sharey='all')
        fig.suptitle(f'Fitted line centers in {what}')
        win = self._conf.input.line_window // 2 if what == 'data' else self._conf.atlas.line_window // 2
        c = 0
        roi = data.data[data.peaks[0]:data.peaks[-1]]
        for i in range(nlines):
            p = data.peaks[i]
            w = max(win, np.abs(p - data.lines[i])) if data.lines[i] is not None else win
            w += 2
            r = i % 4
            ax[r, c].plot(data.data)
            if data.lines[i] is None:
                ax[r, c].text(.5, .1, 'NO FIT', ha='center', va='bottom', color='red', transform=ax[r, c].transAxes)
            else:
                ax[r, c].axvline(x=float(data.lines[i]), color='orange')
            ax[r, c].axvline(x=p, linestyle='--')
            ax[r, c].set_xlim([p - w, p + w])
            ax[r, c].set_ylim([roi.min(), roi.max()])
            if r == 3:
                c += 1
        plt.show()

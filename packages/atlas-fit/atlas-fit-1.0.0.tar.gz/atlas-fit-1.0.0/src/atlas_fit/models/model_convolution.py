import numpy as np
from scipy.signal import fftconvolve
from scipy.ndimage import zoom


class ModelPSF:

    def __init__(self, psf_file: str):
        self._file = psf_file
        self._wl = None
        self._psf = None
        self._spsf = None

    def convolve(self, data: np.array, wl: np.array):
        self._load()
        self._gen_convolution_function(wl)
        return self._convolve_data(data)

    def _load(self):
        data = np.loadtxt(self._file, delimiter=',').T
        self._wl, self._psf = data[0], data[1]

    def _gen_convolution_function(self, wl: np.array):
        self._spsf = zoom(self._psf, len(self._wl)/len(wl), order=5)

    def _convolve_data(self, data: np.array) -> np.array:
        convolved = fftconvolve(data, self._spsf, mode='same')
        return convolved * np.mean(data) / np.mean(convolved)

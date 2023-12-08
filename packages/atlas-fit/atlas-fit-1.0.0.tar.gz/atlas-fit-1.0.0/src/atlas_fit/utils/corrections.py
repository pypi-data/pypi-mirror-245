import numpy as np

from ..base.config import Fitting
from ..atlantes import Atlas
from ..models import Spectrum


def compute_continuum_fit_error(atlas: Atlas, config: Fitting) -> np.array:
    atlas_intensity = Spectrum(atlas.intensity)
    atlas_intensity.fit_continuum(config)
    yes = atlas_intensity.fitted_continuum(np.arange(len(atlas)))
    return atlas.continuum - yes


def prepare_spectrum(data: np.array, config: Fitting,
                     target_mean: float, error_correction: np.array) -> Spectrum:
    s = Spectrum(data)
    s.apply_lowpass_filter_correction(config)
    s.normalize(target_mean)
    s.straighten(config, error_correction * (s.data.mean() / target_mean))
    return s

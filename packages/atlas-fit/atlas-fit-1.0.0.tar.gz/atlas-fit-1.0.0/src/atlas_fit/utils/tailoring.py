import numpy as np

from ..atlantes import atlas_factory, Atlas
from ..base.config import Config
from ..base.constants import NM2ANGSTROM
from ..comperator import Comperator
from ..models.model_convolution import ModelPSF


def select_best_atlas_range(comp: Comperator, conf: Config) -> Atlas:
    wl_values = comp.atlas.wl_func(comp.dispersion(np.arange(len(comp.spectrum.data))))
    lower = min(wl_values.min(), comp.atlas.wl.min())
    upper = max(wl_values.max(), comp.atlas.wl.max())
    atlas = atlas_factory(conf.atlas.key, lower, upper, conversion=NM2ANGSTROM)

    min_x = np.argmin(np.abs(atlas.wl - wl_values.min()))
    max_x = np.argmin(np.abs(atlas.wl - wl_values.max()))
    atlas.wl = atlas.wl[min_x:max_x]
    atlas.intensity = atlas.intensity[min_x:max_x]
    atlas.continuum = atlas.continuum[min_x:max_x]
    if conf.input.model_psf is not None:
        mpsf = ModelPSF(conf.input.model_psf)
        atlas.intensity = mpsf.convolve(atlas.intensity, atlas.wl)
    return atlas


def select_data_fit_region(comp: Comperator, atlas: Atlas) -> tuple:
    xes = np.arange(len(comp.spectrum.data))
    wl_values = comp.atlas.wl_func(comp.dispersion(xes))
    min_x = np.argmin(np.abs(wl_values - atlas.wl.min()))
    max_x = np.argmin(np.abs(wl_values - atlas.wl.max()))
    return min_x, max_x

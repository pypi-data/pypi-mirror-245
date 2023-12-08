from dataclasses import dataclass, field

import yaml

from .constants import M2NM


class ConfigItem:
    """
    Configuration Item base class to provide generic methods
    """

    def __init__(self, **args):
        pass

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create a config item from a dictionary.

        All instance variable names are supported as keywords.
        All keywords are optional, if the keyword is not present the default will be used.
        """

        return cls(**data)

    def _repr(self):
        txt = f'--- {self.__class__.__name__} ---\n'
        for field_name, value in self.__dict__.items():
            txt += '{:<17} = {}\n'.format(field_name, value)
        return txt


@dataclass
class Data(ConfigItem):
    """Configuration for the input data"""

    corrected_frame: str = None
    """
    Path to the Input file to use for extraction of spectrum.
    Should be de-smiled, and first order flat corrected.
    Must be fits format.
    """

    offset_map: str = None
    """Path to the OffsetMap to amend."""

    soft_flat: str = None
    """Path to the Soft Flat to amend."""

    mod_states: int = 4
    """Number of modulation states"""

    roi: str = None
    """
    The region of interest to extrac from the input frame, in typical python format.
    Selected ROI must result in a 1D horizontal spectrum.
    """

    correction_roi: str = None
    """
    The region of interest to correct, in typical python format. Will only take y,x dimensions
    """

    wl_start: float = None
    """Lower wavelength border of the data in [nm]"""

    wl_end: float = None
    """Upper wavelength border of the data in [nm]"""

    flipped: bool = False
    """Flag to indicate if the data is flipped in spectral dimension"""

    stray_light: float = 0
    """Anticipated stray-light component in percent [%]"""

    line_window: int = 10
    """The window [px] for the gauss-fit to operate in around detected line cores"""

    fwhm: float = None
    """The FWHM of the spectrum data at central wl [nm]"""

    model_psf: str = None
    """Optional path to a file with a spectral PSF model."""

    def __repr__(self):
        return self._repr()

    @property
    def central_wl(self) -> float:
        return (self.wl_start + self.wl_end) / 2


@dataclass
class Fitting(ConfigItem):
    """Configuration for the fitting parameters"""

    continuum_filter_order: int = None
    """Order of the lowpass-prefilter to apply. Use None to deactivate"""

    continuum_spline_degree: int = 3
    """Spline degree for the continuum fit"""

    continuum_spline_smoothing: int = 1
    """Spline smoothing factor for the continuum fit"""

    continuum_points: int = 100
    """Number of anchor points to derive the continuum from"""

    dispersion_min_degree: int = 2
    """Maximal dispersion degree to try"""

    dispersion_max_degree: int = 10
    """Maximal dispersion degree to try"""

    stray_light_ignored_lines: list = ()
    """A list of wavelength position of lines to ignore during stray light fitting (e.g., tellurics)"""

    max_stray_light: int = 50
    """Max allowed stray light value in percent [%]"""

    max_fwhm: float = 2e-2
    """Max allowed FWHM value to fit"""

    squash_offsets: bool = True
    """
    Flag to indicate if the offsets that have been determined per mod state shall be averaged.
    It is envisaged to do so (hence the default), since this will help reducing polarimetric artifacts in most cases.
    Only in known cases of "differential moving lines" (e.g. due to the polarizer) the modulated correction can be
    beneficial.
    """

    save_dispersion_function: bool = False
    """If set to true the fitted dispersion function will be saved in a numpy txt format"""

    def __repr__(self):
        return self._repr()


@dataclass
class Atlas(ConfigItem):
    """Atlas configuration"""

    key: str = 'fts'
    """
    The atlas to use.
    - 'fts', 'hhdc': Hamburg disk center (Neckel et al.) (default),
    - 'hhavrg': Hamburg disk average (Neckel et al.),
    - 'sss' Second Solar Spectrum (Stenflo & Gandorfer)
    """

    line_window: int = 10
    """The window [px] for the gauss-fit to operate in around detected line cores"""

    fwhm: float = None
    """The FWHM of the atlas spectrum at central wl [nm]"""

    def compute_fwhm(self, wl: float):
        if self.fwhm is not None:
            return self.fwhm

        if self.key in ['fts', 'hhdc']:
            # currently we only compute FWHM for disk center atlas and return None otherwise.
            self.fwhm = wl ** 2 / (2 * M2NM)

        return self.fwhm

    @staticmethod
    def from_data(data: Data):
        return Atlas(line_window=data.line_window)

    def update(self, data: dict):
        for key, value in data.items():
            self.__setattr__(key, value)
        return self

    def __repr__(self):
        return self._repr()


@dataclass
class Config:
    """
    Configuration DataItem
    """

    label: str = 'Input'
    """Label string used in plots."""

    debug: bool = False
    """Turn debug mode on and off"""

    input: Data = field(default_factory=Data)
    """Input data configuration"""

    atlas: Atlas = field(default_factory=Atlas)
    """Atlas selection and configuration"""

    fitting: Fitting = field(default_factory=Fitting)
    """Atlas selection and configuration"""

    @staticmethod
    def from_dict(data: dict):
        """
        Create a config from a dictionary.

        All instance variable names are supported as keywords.
        All keywords are optional, if the keyword is not present the default will be used.
        """
        data['input'] = Data.from_dict(data['input'])
        if 'fitting' in data:
            data['fitting'] = Fitting.from_dict(data['fitting'])
        data['atlas'] = Atlas.from_data(data['input']).update(data['atlas'])
        return Config(**data)

    @staticmethod
    def from_yaml(path: str):
        """Load config from a yaml file"""
        with open(path, 'r') as f:
            return Config.from_dict(yaml.safe_load(f))

    def __repr__(self):
        txt = '== ACTIVE CONFIGURATION ==\n'
        txt += '{:<17} = {}\n'.format('label', self.label)
        for section in ['input', 'fitting', 'atlas']:
            txt += repr(self.__getattribute__(section))
        return txt

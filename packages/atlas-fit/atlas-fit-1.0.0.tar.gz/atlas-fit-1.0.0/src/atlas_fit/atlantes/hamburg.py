#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module to access the original Hamburg atlas (Neckel et al.).
Per default located in `data/atlases/FTS-Atlas`

@author: hoelken
"""
import os

import numpy as np

from .atlas import Atlas
from ..base.constants import ROOT_DIR
from ..base.errors import IllegalStateError


class FTSAtlas(Atlas):
    """
    Hamburg FTS Atlas data class
    """

    #: ATLAS_LOCATION
    ATLAS_LOCATION = os.path.join(ROOT_DIR, '..', 'data', 'FTS-Atlas')

    def __init__(self, start: float, stop: float, location: str = ATLAS_LOCATION):
        # list of file paths
        self.files = [os.path.join(location, f) for f in self._atlas_files()]
        # Containers for the loaded atlas
        # Build class
        super().__init__(start, stop)

    def load(self):
        """Read the content of the atlas to mem"""
        if len(self.wl) > 0:
            return self

        if not os.path.exists(self.files[0]):
            file0 = os.path.relpath(self.files[0])
            readme = os.path.abspath(os.path.join(FTSAtlas.ATLAS_LOCATION, '../..', 'Readme.md'))
            raise IllegalStateError(f'{file0} not found. Atlas not available.\nSee {readme} for details.')

        self._load_data()
        self.wl = np.array(self.wl)
        self.intensity = np.array(self.intensity)
        self.continuum = np.array(self.continuum)
        if len(self.wl) < 1:
            raise IllegalStateError('Could not load wavelengths from atlas')
        return self

    def _load_data(self) -> None:
        for num, file in enumerate(self.files):
            if not self._load_file(os.path.relpath(file)):
                return

    def _load_file(self, file: str):
        with open(file) as f:
            for line in f:
                content = line.split()
                wl = float(content[0])
                if wl > self.stop:
                    return False

                if wl < self.start:
                    continue

                self.wl.append(wl)
                self.intensity.append(float(content[1]))
                self.continuum.append(float(content[2]))
            return True

    def _atlas_files(self):
        raise NotImplementedError()


class FTSDCAtlas(FTSAtlas):
    #: List of file names forming the Hamburg Atlas
    #: 1 to 10: Disk Average, 11 to 20: Disk center.
    ATLAS_FILES = [f'file{i:02d}' for i in range(11, 21)]

    def _atlas_files(self):
        return self.ATLAS_FILES


class FTSAvrgAtlas(FTSAtlas):
    #: List of file names forming the Hamburg Atlas
    #: 1 to 10: Disk Average, 11 to 20: Disk center.
    ATLAS_FILES = [f'file{i:02d}' for i in range(1, 11)]

    def _atlas_files(self):
        return self.ATLAS_FILES

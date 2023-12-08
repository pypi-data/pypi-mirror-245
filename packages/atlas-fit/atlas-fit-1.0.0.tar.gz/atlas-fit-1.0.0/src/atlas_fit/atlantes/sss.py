#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module to access the second solar spectrum atlas
provided in electronic form by IRSOL as a compilation
by Stenflo (2014), based on the atlas of Gandorfer
(2000, 2002, 2005).
Per default located in `data/atlases/SSS-Atlas`

@author: hoelken
"""
import os
import numpy as np

from .atlas import Atlas
from ..base.errors import IllegalStateError
from ..base.constants import ROOT_DIR


class SSSAtlas(Atlas):
    """
    SSS Atlas data class
    """

    #: ATLAS_LOCATION
    ATLAS_LOCATION = os.path.join(ROOT_DIR, '..', 'data', 'SSS-Atlas')
    #: ATLAS FILE NAME
    ATLAS_FILE = 'SSSatlas.txt'
    #: Number of rows to ignore ad the beginning (inclusive)
    HEADER_ROWS = 4

    def __init__(self, start: float, stop: float, location: str = ATLAS_LOCATION):
        # list of file pathes
        self.file = os.path.join(location, SSSAtlas.ATLAS_FILE)
        # Containers for the loaded atlas
        #: Stokes Q/I
        self.stokes_q = []
        #: Stokes Q/I smoothed
        self.stokes_q_smoothed = []
        # Build class
        super().__init__(start, stop)

    def load(self):
        """Read the content of the atlas to memory"""
        if len(self.wl) > 0:
            return self

        if not os.path.exists(self.file):
            file = os.path.relpath(self.file)
            readme = os.path.abspath(os.path.join(SSSAtlas.ATLAS_LOCATION, '../..', 'Readme.md'))
            raise IllegalStateError(f'{file} not found. Atlas not available.\nSee {readme} for details.')

        self.__load_data()
        self.wl = np.array(self.wl)
        self.stokes_q = np.array(self.stokes_q)
        self.stokes_q_smoothed = np.array(self.stokes_q_smoothed)
        self.continuum = np.array(self.continuum)
        self.intensity = np.array(self.intensity)
        if len(self.wl) < 1:
            raise IllegalStateError('Could not load wavelengths from atlas')
        return self

    def __load_data(self) -> None:
        with open(self.file) as f:
            line_nr = -1
            for line in f:
                line_nr += 1
                if line_nr < SSSAtlas.HEADER_ROWS:
                    continue

                content = line.split()
                wl = float(content[0])
                if wl > self.stop:
                    return

                if wl < self.start:
                    continue

                self.wl.append(wl)
                self.intensity.append(float(content[1]))
                self.stokes_q.append(float(content[2]))
                self.stokes_q_smoothed.append(float(content[3]))
                self.continuum.append(float(content[4]))

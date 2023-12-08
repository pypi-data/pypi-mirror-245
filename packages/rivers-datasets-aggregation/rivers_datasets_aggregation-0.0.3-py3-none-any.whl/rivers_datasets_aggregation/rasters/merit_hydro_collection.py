#!/usr/bin/env python
# coding: utf8
#
# Copyright 2023 CS GROUP
# Licensed to CS GROUP (CS) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# CS licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""MERIT-Hydro rasters collection."""

# pylint: disable=consider-using-f-string, invalid-name, consider-iterating-dictionary
# pylint: disable=no-value-for-parameter, keyword-arg-before-vararg, arguments-differ
import os

import rasterio

from .egm2008 import EGM2008RastersCollection
from .rasters_collection import RastersCollection


class MeritHydroCollection(RastersCollection):
    """MERIT-Hydro rasters collection."""

    def __init__(self, sourcedir, cache_size=10, vertical_datum="EGM96", **kwargs):
        """Constructor."""

        super().__init__(sourcedir, cache_size)

        self._vertical_datum = vertical_datum

        if vertical_datum != "EGM96":
            print(kwargs.keys())
            if "EGM96_DIR" not in kwargs.keys():
                raise ValueError("keyword argument 'EGM96_DIR' requested")
            self.EGM96_DIR = kwargs["EGM96_DIR"]
            self.rasterEGM96 = rasterio.open(os.path.join(self.EGM96_DIR, "ww15mgh.asc"))
            self.bandEGM96 = self.rasterEGM96.read(1)

        elif vertical_datum == "EGM2008":
            if "EGM2008_DIR" not in kwargs.keys():
                raise ValueError("keyword argument 'EGM2008_DIR' requested")
            self.EGM2008_DIR = kwargs["EGM2008_DIR"]
            self.EGM2008 = EGM2008RastersCollection(self.EGM2008_DIR)

    def get_tile_info(self, lon, lat, var, **kwargs):
        """Get tile information from latitude and longitude query."""

        # Compute tile and group names
        if lat >= 0.0:
            tile = "n%02i" % (int(lat / 5) * 5)
            group = "n%02i" % (int(lat / 30) * 30)
        else:
            tile = "s%02i" % ((int(-lat / 5) + 1) * 5)
            group = "s%02i" % ((int(-lat / 30) + 1) * 30)
        if lon >= 0.0:
            tile += "e%03i" % (int(lon / 5) * 5)
            group += "e%03i" % (int(lon / 30) * 30)
        else:
            tile += "w%03i" % ((int(-lon / 5) + 1) * 5)
            group += "w%03i" % ((int(-lon / 30) + 1) * 30)

        tiledir = os.path.join(self._sourcedir, "%s_%s" % (var, group))
        tilefile = os.path.join(tiledir, "%s_%s.tif" % (tile, var))
        tilearch = (
            os.path.join(self._sourcedir, "%s_%s.tar" % (var, group)),
            "%s_%s/%s_%s.tif" % (var, group, tile, var),
            self._sourcedir,
        )
        return (tile, tiledir, tilefile, tilearch)

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

"""EGM 2008 rasters collection."""

# pylint: disable=consider-using-f-string, unused-argument
import os

from .rasters_collection import RastersCollection


class EGM2008RastersCollection(RastersCollection):
    """EGM 2008 rasters collection."""

    def __init__(self, sourcedir, cache_size):
        """Constructor."""
        super().__init__(sourcedir, cache_size)

    def get_file_info(self, lon, lat, *args, **kwargs):
        """Get tile informations from latitude and longitude query."""

        # Compute tile and group names
        if lat >= 100.0:
            tile = "n%03i" % (int(lat / 45) * 45)
        elif lat >= 0.0:
            tile = "n%02i" % (int(lat / 45) * 45)
        elif lat < -100.0:
            tile = "s%03i" % ((int(-lat / 45) + 1) * 45)
        else:
            tile = "s%02i" % ((int(-lat / 45) + 1) * 45)
        if lon >= 100.0:
            tile += "e%03i" % (int(lon / 45) * 45)
        elif lon >= 0.0:
            tile += "e%02i" % (int(lon / 45) * 45)
        elif lon < -100.0:
            tile += "w%03i" % ((int(-lon / 45) + 1) * 45)
        else:
            tile += "w%02i" % ((int(-lon / 45) + 1) * 45)
        tiledir = os.path.join(self._sourcedir, tile)
        tilefile = os.path.join(tiledir, tile, "w001001.adf")
        tilezip = tiledir + ".zip"

        return (tile, tiledir, tilefile, tilezip)

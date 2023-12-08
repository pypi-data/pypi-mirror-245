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

"""Generic RasterCollection class."""

# pylint: disable=consider-using-f-string
import os

from rivers_datasets_aggregation.rasters.rasters_collection import RastersCollection


class GenericRastersCollection(RastersCollection):
    """Generic RasterCollection."""

    def __init__(self, raster_name, raster_path):
        """Constructor."""

        self._raster_name = raster_name
        self._raster_path = raster_path
        self._source_dir = os.path.dirname(self._raster_path)

        super().__init__(sourcedir=self._source_dir, cache_size=5, driver="rasterio")

    def get_tile_info(self, lon, lat, *args, **kwargs):
        """Get tile information from longitude and latitude query."""

        if kwargs["var"] == self._raster_name:
            tile = self._raster_name
            tiledir = self._source_dir
            tilefile = self._raster_path
            tilearch = None

        else:
            raise ValueError("wrong variable: %s" % kwargs["var"])

        return (tile, tiledir, tilefile, tilearch)

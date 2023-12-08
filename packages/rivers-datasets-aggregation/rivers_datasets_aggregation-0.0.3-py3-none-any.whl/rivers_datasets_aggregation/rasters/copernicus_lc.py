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

"""Copernicus Land Cover 100m dataset for rivers_dataset_aggregation tool."""

# pylint: disable=consider-using-f-string, unused-argument, import-error
import os
import time

import numpy as np
import pandas as pd

from rivers_datasets_aggregation.common.progress import Progress

from .rasters_collection import RastersCollection


class CopernicusLandCover(RastersCollection):
    """Copernicus Land Cover rasters collection"""

    def __init__(self, sourcedir):
        """Constructor."""
        super().__init__(sourcedir, cache_size=5, driver="rasterio")

    def get_tile_info(self, lon, lat, *args, **kwargs):
        """Get tile name, file, directory and archive for each data file name."""

        if kwargs["var"] == "bare_fraction":
            tile = "bare_fraction"
            tiledir = self._sourcedir
            tilefile = os.path.join(
                tiledir, "PROBAV_LC100_global_v3.0.1_2019-nrt_Bare-CoverFraction-layer_EPSG-4326.tif"
            )
            tilearch = None
        elif kwargs["var"] == "builtup_fraction":
            tile = "builtup_fraction"
            tiledir = self._sourcedir
            tilefile = os.path.join(
                tiledir, "PROBAV_LC100_global_v3.0.1_2019-nrt_BuiltUp-CoverFraction-layer_EPSG-4326.tif"
            )
            tilearch = None
        elif kwargs["var"] == "crops_fraction":
            tile = "crops_fraction"
            tiledir = self._sourcedir
            tilefile = os.path.join(
                tiledir, "PROBAV_LC100_global_v3.0.1_2019-nrt_Crops-CoverFraction-layer_EPSG-4326.tif"
            )
            tilearch = None
        elif kwargs["var"] == "forest_type":
            tile = "forest_type"
            tiledir = self._sourcedir
            tilefile = os.path.join(tiledir, "PROBAV_LC100_global_v3.0.1_2019-nrt_Forest-Type-layer_EPSG-4326.tif")
            tilearch = None
        elif kwargs["var"] == "grass_fraction":
            tile = "grass_fraction"
            tiledir = self._sourcedir
            tilefile = os.path.join(
                tiledir, "PROBAV_LC100_global_v3.0.1_2019-nrt_Grass-CoverFraction-layer_EPSG-4326.tif"
            )
            tilearch = None
        elif kwargs["var"] == "mosslichen_fraction":
            tile = "mosslichen_fraction"
            tiledir = self._sourcedir
            tilefile = os.path.join(
                tiledir, "PROBAV_LC100_global_v3.0.1_2019-nrt_MossLichen-CoverFraction-layer_EPSG-4326.tif"
            )
            tilearch = None
        elif kwargs["var"] == "permanentwater_fraction":
            tile = "permanentwater_fraction"
            tiledir = self._sourcedir
            tilefile = os.path.join(
                tiledir, "PROBAV_LC100_global_v3.0.1_2019-nrt_PermanentWater-CoverFraction-layer_EPSG-4326.tif"
            )
            tilearch = None
        elif kwargs["var"] == "seasonalwater_fraction":
            tile = "seasonalwater_fraction"
            tiledir = self._sourcedir
            tilefile = os.path.join(
                tiledir, "PROBAV_LC100_global_v3.0.1_2019-nrt_SeasonalWater-CoverFraction-layer_EPSG-4326.tif"
            )
            tilearch = None
        elif kwargs["var"] == "shrub_fraction":
            tile = "shrub_fraction"
            tiledir = self._sourcedir
            tilefile = os.path.join(
                tiledir, "PROBAV_LC100_global_v3.0.1_2019-nrt_Shrub-CoverFraction-layer_EPSG-4326.tif"
            )
            tilearch = None
        elif kwargs["var"] == "snow_fraction":
            tile = "snow_fraction"
            tiledir = self._sourcedir
            tilefile = os.path.join(
                tiledir, "PROBAV_LC100_global_v3.0.1_2019-nrt_Snow-CoverFraction-layer_EPSG-4326.tif"
            )
            tilearch = None
        elif kwargs["var"] == "tree_fraction":
            tile = "tree_fraction"
            tiledir = self._sourcedir
            tilefile = os.path.join(
                tiledir, "PROBAV_LC100_global_v3.0.1_2019-nrt_Tree-CoverFraction-layer_EPSG-4326.tif"
            )
            tilearch = None
        else:
            raise ValueError("wrong variable: %s" % kwargs["var"])

        return (tile, tiledir, tilefile, tilearch)


def extract_stations_on_copernicus_land_cover(copernicus_lc_dir, stations, var, bufsize=0):
    """
    Extract values of a variable in SoilGrids (v2017) for a list of stations

    Parameters
    ----------
        copernicus_lc_dir: str
            Path to the directory of Copernicus Land Cover
        stations: pandas.DataFrame
            Pandas Dataframe that contains the attributes of the stations. This Dataframe must contain at least
            the following columns: name, lon, lat and area. Values of area can be NaN
        var: str
            Soilgrids variable
        bufsize: int
            Size of the buffer for extraction. If size is 0 or 1 the value of the corresponding pixel is used

    Returns
    -------
        updated_stations : Pandas Dataframe which is a copy of the stations Dataframe
            with a new column containing the extracted values
    """

    print("")
    print("=" * 60)
    print("PROCESS : extract_stations_on_soilgrids_2017")
    print(" - Dimensionality : %i stations" % stations.shape[0])
    print(" - Buffer size : %i" % bufsize)
    print("=" * 60)
    process_start_time = time.time()

    # Initalize SoilGrids collection
    copernicus = CopernicusLandCover(copernicus_lc_dir)

    # Copy stations to updated_stations (return of this function)
    updated_stations = stations.copy()
    updated_stations["%s" % var] = pd.Series(np.ones(updated_stations.shape[0]) * np.nan, index=updated_stations.index)

    progress = Progress(prefix="Extracting %s values" % var, start=0, end=stations.shape[0])
    for row in range(0, stations.shape[0]):
        progress.advance()
        lon = stations.loc[row, "lon"]
        lat = stations.loc[row, "lat"]
        if bufsize <= 1:
            updated_stations.loc[row, "%s" % var] = copernicus.get_value(lon, lat, var=var)
        else:
            updated_stations.loc[row, "%s" % var] = copernicus.get_buffer_mean(
                lon, lat, bufsize // 2, bufsize // 2, var=var
            )
    progress.finalize()

    print("=" * 60)
    process_end_time = time.time()
    print("JOB DONE in %.1f seconds" % (process_end_time - process_start_time))
    print("=" * 60)
    print("")

    return updated_stations

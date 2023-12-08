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

"""SoilGrids (2017) rasters collection."""

# pylint: disable=consider-using-f-string, import-error, keyword-arg-before-vararg
import os
import time

import numpy as np
import pandas as pd

from rivers_datasets_aggregation.common.progress import Progress

from .rasters_collection import RastersCollection


class SoilGrids2017(RastersCollection):
    """SoilGrids (2017) rasters collection."""

    def __init__(self, sourcedir):
        """Constructor."""

        super().__init__(sourcedir, cache_size=5, driver="rasterio")

    def get_tile_info(self, lon, lat, level=1, *args, **kwargs):
        """Get tile information from longitude and latitude query."""

        if kwargs["var"] == "clay":
            tile = "clay"
            tiledir = self._sourcedir
            tilefile = os.path.join(tiledir, "CLYPPT_M_sl%i_250m_ll.tif" % level)
            tilearch = None
        elif kwargs["var"] == "sand":
            tile = "sand"
            tiledir = self._sourcedir
            tilefile = os.path.join(tiledir, "SNDPPT_M_sl%i_250m_ll.tif" % level)
            tilearch = None
        elif kwargs["var"] == "silt":
            tile = "silt"
            tiledir = self._sourcedir
            tilefile = os.path.join(tiledir, "SLTPPT_M_sl%i_250m_ll.tif" % level)
            tilearch = None
        else:
            raise ValueError("wrong variable: %s" % kwargs["var"])

        return (tile, tiledir, tilefile, tilearch)


def extract_stations_on_soilgrids_2017(soilgrids_dir, stations, var, bufsize=0):
    """
    Extract values of a variable in SoilGrids (v2017) for a list of stations

    Parameters
    ----------
        soilgrids_dir: str
            Path to the directory of SoilGrids
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
    soilgrids = SoilGrids2017(soilgrids_dir)

    # Copy stations to updated_stations (return of this function)
    updated_stations = stations.copy()
    updated_stations["%s" % var] = pd.Series(np.ones(updated_stations.shape[0]) * np.nan, index=updated_stations.index)

    progress = Progress(prefix="Extracting %s values" % var, start=0, end=stations.shape[0])
    for row in range(0, stations.shape[0]):
        progress.advance()
        lon = stations.loc[row, "lon"]
        lat = stations.loc[row, "lat"]
        if bufsize <= 1:
            updated_stations.loc[row, "%s" % var] = soilgrids.get_value(lon, lat, var=var)
        else:
            updated_stations.loc[row, "%s" % var] = soilgrids.get_buffer_mean(
                lon, lat, bufsize // 2, bufsize // 2, var=var
            )
    progress.finalize()

    print("=" * 60)
    process_end_time = time.time()
    print("JOB DONE in %.1f seconds" % (process_end_time - process_start_time))
    print("=" * 60)
    print("")

    return updated_stations

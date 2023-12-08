#!/usr/bin/env python
# coding: utf8
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

"""Example of GRDC stations relocations on MERIT-Hydro Basins for Africa."""

# pylint: disable=import-error
import argparse

import numpy as np
import pandas as pd

from rivers_datasets_aggregation.common.progress import Progress
from rivers_datasets_aggregation.rasters.merit_hydro_collection import MeritHydroCollection

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Example of relocation of GRDC stations on MERIT Hydro Basins for Africa"
    )
    parser.add_argument(
        "merit_root", metavar="merit_root", type=str, help="Path to the root directory of MERIT Hydro Basins"
    )
    args = parser.parse_args()

    # Load GRDC stations
    stations = pd.read_csv("GRDC_stations_AF.csv", sep=";")
    stations = stations.rename(columns={"long": "lon"})

    # Initalize MERIT Hydro collection
    merit_hydro = MeritHydroCollection(args.merit_root, "EGM96")

    progress = Progress(prefix="Computing elevations", start=0, end=stations.shape[0])
    stations["heights"] = pd.Series(np.ones(stations.shape[0]) * np.nan, index=stations.index)
    for row in range(0, stations.shape[0]):
        progress.advance()
        lon = stations.loc[row, "lon"]
        lat = stations.loc[row, "lat"]
        stations.loc[row, "heights"] = merit_hydro.get_value(lon, lat, "elv", debug=False)
    progress.finalize()

    stations.to_csv("GRDC_stations_AF_heights.csv", sep=";")

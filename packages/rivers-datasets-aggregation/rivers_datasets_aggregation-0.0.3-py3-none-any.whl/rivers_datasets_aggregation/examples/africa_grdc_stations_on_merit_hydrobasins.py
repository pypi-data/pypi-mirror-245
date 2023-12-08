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

"""Example of GRDC stations relocation."""

# pylint: disable=import-error
import argparse
import os

import fiona
import pandas as pd

from rivers_datasets_aggregation.rivers_network.stations_on_rivers_network import relocate_stations_on_rivers_network

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
    stations = stations.rename(columns={"long": "lon", "station": "name"})

    # Open MERIT Hydro layer
    merit_rivers_network_file = os.path.join(
        args.merit_root, "pfaf_1_MERIT_Hydro_v07_Basins_v01", "riv_pfaf_1_MERIT_Hydro_v07_Basins_v01.shp"
    )
    merit_rivers_network = fiona.open(merit_rivers_network_file, "r")

    stations = relocate_stations_on_rivers_network(
        merit_rivers_network, stations, bbox="auto", dx=0.25, dy=0.25, add_reaches_indices=True
    )

    stations = stations.rename(columns={"lon": "long", "name": "stations"})
    stations.to_csv("GRDC_stations_AF_relocated.csv", sep=";")

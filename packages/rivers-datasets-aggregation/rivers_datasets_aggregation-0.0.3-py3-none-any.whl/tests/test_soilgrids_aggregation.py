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
import os
import sys

import pandas as pd

from rivers_datasets_aggregation.rasters.soilgrids_2017 import extract_stations_on_soilgrids_2017


def test_soilgrids_aggregation_on_grdc_stations(bufsize=0):
    """Test clay aggregation on GRDC stations in Africa."""

    # Check that bufsize is an odd number
    if bufsize > 0 and bufsize % 2 == 0:
        raise ValueError("bufsize must be a positive odd number")

    stations = pd.read_csv(os.path.join(os.path.dirname(__file__), "data/GRDC_stations_AF.csv"), sep=";")
    stations = stations.rename(columns={"long": "lon"})

    soilgrids_root = os.path.join(os.path.dirname(__file__), "data/soilgrids")

    updated_stations = extract_stations_on_soilgrids_2017(soilgrids_root, stations, "clay", bufsize)
    ref_stations = pd.read_csv(
        os.path.join(os.path.dirname(__file__), "data/ref/GRDC_stations_AF_clay_percentage.csv"), sep=";"
    )

    assert updated_stations.equals(ref_stations)


if __name__ == "__main__":
    test_soilgrids_aggregation_on_grdc_stations()

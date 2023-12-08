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

# pylint: disable=import-error,
import argparse
import os

from rivers_datasets_aggregation.vectors.vectors_collection import VectorsCollection

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Example of relocation of GRDC stations on MERIT Hydro Basins for Africa"
    )
    parser.add_argument("db_root", metavar="merit_root", type=str, help="Path to the root directory of database")
    parser.add_argument(
        "-continent", metavar="continent", type=str, default="NA", help="Abreviation of the continent to focus on"
    )
    args = parser.parse_args()

    # Initialise VectorsCollection
    collection = VectorsCollection(os.path.join(args.db_root, args.continent), fmt="shp")
    minval, maxval = collection.compute_statistics("catch_area", -9999.0)
    print(minval, maxval)

    # stations = relocate_stations_on_rivers_network(merit_rivers_network, stations,
    # bbox="auto",
    # dx=0.25, dy=0.25,
    # add_reaches_indices=True)

    # stations.to_csv("GRDC_stations_AF_relocated.csv", sep=";")

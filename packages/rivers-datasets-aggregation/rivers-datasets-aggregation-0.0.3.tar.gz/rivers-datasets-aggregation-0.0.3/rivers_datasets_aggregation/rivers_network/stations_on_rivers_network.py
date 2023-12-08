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

"""Relocation of stations on a given river network."""

# pylint: disable= import-error, consider-using-f-string, invalid-name, broad-exception-caught
# pylint: disable=too-many-arguments, too-many-locals, too-many-branches, too-many-statements
import time

import numpy as np
import pandas as pd
import geopandas as gpd
import shapely.wkt
from osgeo import ogr
from shapely.geometry import LineString, MultiLineString, Point

from rivers_datasets_aggregation.common.linestring_query_grid import LinestringQueryGrid
from rivers_datasets_aggregation.common.progress import Progress
from rivers_datasets_aggregation.vectors.vectors_collection import VectorsCollection
from rivers_datasets_aggregation.utils.convert_geo_format import geodataframe_to_fiona_collection


def relocate_stations_on_reaches(  # noqa: C901
    reaches,
    stations,
    bbox,
    dx,
    dy,
    alpha=0.25,
    area_attribute="area",
    index_attribute=None,
    add_reaches_indices=False,
    max_distance=None,
):
    """
    Enforce positions of stations on a rivers network

    Parameters
    ----------
        reaches: iterable
            Iterable that contains shapeply.geometry.LineString objects for the reaches of the network
        stations: pandas.DataFrame
            Pandas Dataframe that contains the attributes of the stations. This Dataframe must contain at least
            the following columns: name, lon, lat and area. Values of area can be NaN
        bbox: tuple
            Tuple (lonmin, lonmax, latmin, latmax) that defines the boundary for the QueryGrid
        dx: float
            Spacing for the QueryGrid
        dy: float
            Spacing for the QueryGrid
        alpha: float
            Parameter for the objective function which is
            normalized(distance^2) + alpha * normalized((reach_area - station_area)^2)
        area_attribute: str
            Attribute in the reaches properties that stores the area
        add_reaches_indices: bool
            True to add reaches indices in the returned DataFrame

    Returns
    -------
        updated_stations : Pandas Dataframe which is a copy of the stations Dataframe but with updated coordinates
    """

    # TODO use attribute for the max distance ?

    print("")
    print("=" * 60)
    print("PROCESS : relocate_stations_on_reaches")
    print(" - Dimensionality : %i reaches and %i stations" % (len(reaches), stations.shape[0]))
    print("=" * 60)
    process_start_time = time.time()

    # Initialise QueryGrid
    queryGrid = LinestringQueryGrid(*bbox, dx=dx, dy=dy)
    if isinstance(reaches, VectorsCollection):
        queryGrid.add_entries(reaches, store_index=False)
    else:
        if index_attribute is None:
            queryGrid.add_entries(reaches, store_index=True)
        else:
            queryGrid.add_entries(reaches, store_index=True, index_attribute=index_attribute)

    # Copy stations to updated_stations (return of this function)
    updated_stations = stations.copy()
    if add_reaches_indices is True:
        updated_stations["reach_index"] = pd.Series(
            np.ones(updated_stations.shape[0], dtype=int) * -9, index=updated_stations.index
        )

    # Loop on stations
    progress = Progress(0, stations.shape[0], 20, prefix="Processing stations")
    errors = []
    for row in range(0, stations.shape[0]):
        progress.advance()

        # Find cells of the QueryGrid that contain the station
        try:
            cells = queryGrid.get_cells(stations["lon"][row], stations["lat"][row])
        except Exception:
            errors.append("Station not found:%s" % stations["name"][row])
            continue

        # Compute distance^2 and (reach_area - station_area)^2 for each reach in the QueryGrid cells
        selected_reaches = []
        if add_reaches_indices is True:
            selected_reaches_indices = []
        dist2 = []
        darea2 = []
        station_point = Point(stations["lon"][row], stations["lat"][row])
        area = stations["area"][row]
        # print("Cells found:", len(cells))
        for cell in cells:
            # print("CELL entries:", len(cell.entries))
            for entry in cell.entries:
                if isinstance(entry, int):
                    # Retrieve reach from index
                    index = entry
                    reach = reaches[index]
                    # print(" - Reach:", reach["properties"]["reach_id"])

                else:
                    reach = entry

                if isinstance(reach, ogr.Feature):
                    # Retrieve Shapely Geometry from an OGR feature
                    geometry = reach.GetGeometryRef()
                    if geometry.GetGeometryName() == "LINESTRING" or geometry.GetGeometryName() == "MULTILINESTRING":
                        wkt = geometry.ExportToWkt()
                        geometry = shapely.wkt.loads(wkt)
                    else:
                        raise RuntimeError("Entry has geometry type %s (must be LineString or MultiLineString)")

                    # Retrieve area
                    reach_area = reach.GetField(area_attribute)
                    if index_attribute is not None:
                        reach_index = reach.GetField(index_attribute)
                    else:
                        if isinstance(entry, int):
                            reach_index = entry
                        else:
                            reach_index = -1

                elif isinstance(reach, dict):
                    # Retrieve Shapely Geometry from a feature dict (Fiona)
                    if reach["geometry"]["type"] == "LineString":
                        geometry = LineString(reach["geometry"]["coordinates"])
                    elif reach["geometry"]["type"] == "MultiLineString":
                        geometry = MultiLineString(reach["geometry"]["coordinates"])
                    else:
                        raise RuntimeError("Entry has geometry type %s (must be LineString or MultiLineString)")

                    # Retrieve area
                    reach_area = reach["properties"][area_attribute]
                    # if reach["properties"]["reach_id"] == "62281200061":
                    #     print("Yes !")
                    #     choice = input()
                    if index_attribute is not None:
                        reach_index = reach["properties"][index_attribute]
                    else:
                        if isinstance(entry, int):
                            reach_index = entry
                        else:
                            reach_index = -1

                else:
                    raise ValueError("wrong reach type: %s" % type(reach))

                if max_distance is not None:
                    if station_point.distance(geometry) > 0.05:
                        continue

                dist2.append(station_point.distance(geometry) ** 2)
                if area >= 0.0 and np.isfinite(area):
                    darea2.append((stations["area"][row] - reach_area) ** 2)
                else:
                    darea2.append(0.0)
                selected_reaches.append(reach)
                if add_reaches_indices is True:
                    selected_reaches_indices.append(reach_index)

        # Check that at least one reach has been found
        if len(dist2) == 0:
            errors.append("No neighbour reach found for station %s" % stations["name"][row])
            continue

        # Normalize distance^2 and (reach_area - station_area)^2
        dist2 = np.array(dist2)
        darea2 = np.array(darea2)
        std_dist2 = np.std(dist2)
        if std_dist2 > 1e-12:
            dist2_normed = dist2 / np.std(dist2)
        else:
            dist2_normed = dist2
        std_darea2 = np.std(darea2)
        if std_darea2 > 1e-12:
            darea2_normed = darea2 / np.std(darea2)
        else:
            darea2_normed = darea2

        # Compute values of the objective function
        objective_function = dist2_normed + alpha * darea2_normed

        # Find the argmin of the objective function and retrieve corresponding reach
        index = np.argmin(objective_function)
        reach = selected_reaches[index]

        # Retrieve Shapely geometry of the selected reach
        if isinstance(reach, ogr.Feature):
            # Retrieve Shapely Geometry from an OGR feature
            geometry = reach.GetGeometryRef()
            if geometry.GetGeometryName() == "LINESTRING" or geometry.GetGeometryName() == "MULTILINESTRING":
                wkt = geometry.ExportToWkt()
                geometry = shapely.wkt.loads(wkt)
            else:
                raise RuntimeError("Entry has geometry type %s (must be LineString or MultiLineString)")

            # Retrieve area
            reach_area = reach.GetField(area_attribute)

        elif isinstance(reach, dict):
            # Retrieve Shapely Geometry from a feature dict (Fiona)
            if reach["geometry"]["type"] == "LineString":
                geometry = LineString(reach["geometry"]["coordinates"])
            elif reach["geometry"]["type"] == "MultiLineString":
                geometry = MultiLineString(reach["geometry"]["coordinates"])
            else:
                raise RuntimeError("Entry has geometry type %s (must be LineString or MultiLineString)")

        # if reach["geometry"]["type"] == "LineString":
        # geometry = LineString(reach["geometry"]["coordinates"])
        # else:
        # geometry = MultiLineString(reach["geometry"]["coordinates"])

        # Project station on selected reach
        new_point = geometry.interpolate(geometry.project(station_point))

        if add_reaches_indices is True:
            reach_index = selected_reaches_indices[index]
            updated_stations.loc[row, ["lon", "lat", "reach_index"]] = [new_point.x, new_point.y, reach_index]
        else:
            updated_stations.loc[row, ["lon", "lat"]] = [new_point.x, new_point.y]

    progress.finalize()

    # Display encountered errors
    if len(errors) > 0:
        # print("\n".join(errors))
        print("( %i errors reported)" % len(errors))

    print("=" * 60)
    process_end_time = time.time()
    print("JOB DONE in %.1f seconds" % (process_end_time - process_start_time))
    print("=" * 60)
    print("")

    return updated_stations


def relocate_stations_on_rivers_network(
    river_network,
    stations,
    bbox,
    dx,
    dy,
    alpha=0.25,
    area_attribute="area",
    index_attribute=None,
    add_reaches_indices=False,
):
    """
    Enforce positions of stations on a rivers network

    Parameters
    ----------
        river_network: fiona.Collection
            fiona Collection that contains reaches (shapeply.geometry.LineString) of the network
        stations: pandas.DataFrame
            Pandas Dataframe that contains the attributes of the stations. This Dataframe must contain at least
            the following columns: name, lon, lat and area. Values of area can be NaN
        bbox: tuple
            Tuple (lonmin, lonmax, latmin, latmax) that defines the boundary for the QueryGrid. Can be None or "auto"
            and then automatically infered from the bounds of the river_network Collection
        dx: float
            Spacing for the QueryGrid
        dy: float
            Spacing for the QueryGrid
        alpha: float
            Parameter for the objective function which is
            normalized(distance^2) + alpha * normalized((reach_area - station_area)^2)
        add_reaches_indices: bool
            True to add reaches indices in the returned DataFrame

    Returns
    -------
            Pandas Dataframe which is a copy of the stations Dataframe but with updated coordinates

    """

    if isinstance(river_network, gpd.GeoDataFrame):
        river_network = geodataframe_to_fiona_collection(river_network)

    if bbox is None or bbox == "auto":
        bounds = river_network.bounds
        bbox = (
            np.floor(bounds[0] / dx) * dx,
            np.ceil(bounds[2] / dx) * dx,
            np.floor(bounds[1] / dy) * dy,
            np.ceil(bounds[3] / dy) * dy,
        )

    updated_stations = relocate_stations_on_reaches(
        river_network, stations, bbox, dx, dy, alpha, area_attribute, index_attribute, add_reaches_indices
    )

    return updated_stations

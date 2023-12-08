#!/usr/bin/env python
# coding: utf8
#
# Copyright 2022-2023 CS GROUP
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

"""Convertion functions for geographic data."""


import geopandas as gpd
import fiona

def geodataframe_to_fiona_collection(gdf, driver='ESRI Shapefile'):
    """
    Converts a GeoPandas GeoDataFrame into a Fiona collection and returns it.

    Parameters
    ----------
        gdf (geopandas.GeoDataFrame): Input GeoDataFrame to be converted.
        driver (str): Fiona driver to be used (default is 'ESRI Shapefile').

    Returns
    -------
        collection (fiona.collection.Collection): A Fiona collection.
    """
    
    # Get the CRS information from the GeoDataFrame
    crs = gdf.crs

    # Create a Fiona schema using the GeoDataFrame's schema
    schema = {
        'geometry': gdf.geometry.type.values[0],
        'properties': gdf.drop('geometry', axis=1).dtypes.to_dict(),
    }

    # Create an in-memory Fiona collection
    collection = fiona.Collection(
        path='memory',
        driver=driver,
        crs=crs,
        schema=schema
    )

    # Iterate over the GeoDataFrame features and add them to the in-memory collection
    for index, row in gdf.iterrows():
        feature = {
            'geometry': mapping(row['geometry']),
            'properties': dict(row.drop('geometry')),
        }
        collection.write(feature)

    return collection

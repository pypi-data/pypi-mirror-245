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

"""VectorsCollection class for memory-optimized vector data handling."""

# pylint: disable=consider-using-f-string, invalid-name, broad-exception-caught, consider-using-with
# pylint: disable=import-error, too-many-branches, too-few-public-methods, unused-variable
# pylint: disable=assignment-from-no-return
import glob
import os
import tarfile
import zipfile

import numpy as np
from osgeo import ogr
import rasterio
from osgeo import gdal


class VectorsCollectionIterator:
    """VectorsCollectionIterator class."""

    def __init__(self, collection):
        """Constructor."""

        self._collection = collection
        self._layer_index = 0
        self._feature_index = 0

    def __next__(self):
        """Iteration method."""

        if self._layer_index < len(self._collection.cache["layers"]):
            # Get current feature
            layer = self._collection.cache["layers"][self._layer_index]
            feature = layer[self._feature_index]

            # Increment
            self._feature_index += 1
            if self._feature_index == layer.GetFeatureCount():
                self._feature_index = 0
                self._layer_index += 1

            return feature

        raise StopIteration


class VectorsCollection:
    """VectorsCollection class."""

    def __init__(self, sourcedir, fmt, cache_size=10, driver="gdal"):
        """Constructor."""

        # Check arguments
        if not isinstance(cache_size, int):
            raise ValueError("cache_size must be of type 'int'")
        if cache_size < 1:
            raise ValueError("cache_size must be greater than zero")
        if driver not in ["gdal", "fiona"]:
            raise ValueError("driver must be 'gdal' or 'fiona'")

        self._sourcedir = sourcedir
        self._fmt = fmt
        self._cache_size = cache_size
        self._driver = driver
        self._cache = {"datafiles": [], "datasets": [], "layers": []}
        self._bounds = None

        # List datafiles
        self._datafiles = self._list_datasets_()

        # Open datasets
        self._open_datasets_()

    def get_tile_info(self, lon, lat, *args, **kwargs):
        """Get specific rasters collection tile information."""

    @property
    def bounds(self):
        """Compute and get bounds attribute."""
        if self._bounds is None:
            # Compute bounds from all extents
            self._bounds = [np.PINF, np.PINF, np.NINF, np.NINF]
            for datafile in self._datafiles:
                basename = os.path.basename(datafile)

                if basename in self._cache["datafiles"]:
                    index = self._cache["datafiles"].index(basename)
                else:
                    # TODO load if not in cache
                    raise NotImplementedError("Automatic update of cache is not implemented yet")

                if self._driver == "gdal":
                    # driver = ogr.GetDriverByName("ESRI Shapefile")
                    # dataset = self._cache["datasets"][index]
                    layer = self._cache["layers"][index]
                    xmin, xmax, ymin, ymax = layer.GetExtent()
                    self._bounds[0] = np.minimum(xmin, self._bounds[0])
                    self._bounds[1] = np.minimum(ymin, self._bounds[1])
                    self._bounds[2] = np.maximum(xmax, self._bounds[2])
                    self._bounds[3] = np.maximum(ymax, self._bounds[3])
                elif self._driver == "fiona":
                    raise NotImplementedError("computing bounds with fiona driver is not implemented yet")

        return self._bounds

    @property
    def cache(self):
        """Get cache attribute."""

        return self._cache

    def __del__(self):
        """Clean cache."""

        self._clean_cache_(last=False)

    def __iter__(self):
        """Iterate."""

        return VectorsCollectionIterator(self)

    def __len__(self):
        """Get features_count attribute."""

        return self._features_count

    def compute_statistics(self, attribute, nodata=None):
        """Compute collection statistics."""

        max_attribute = np.NINF
        min_attribute = np.PINF
        for datafile in self._datafiles:
            if self._driver == "gdal":
                driver = ogr.GetDriverByName("ESRI Shapefile")
                dataset = driver.Open(datafile, 0)
                layer = dataset.GetLayer(0)
                values = [feature.GetField(attribute) for feature in layer]
                if nodata is not None:
                    values = np.array(values)
                    values[np.isclose(values, nodata)] = np.nan
                min_attribute = np.minimum(np.nanmin(values), min_attribute)
                max_attribute = np.maximum(np.nanmax(values), max_attribute)

            elif self._driver == "fiona":
                raise NotImplementedError("computing statistics with fiona driver is not implemented yet")

        return min_attribute, max_attribute

    def _list_datasets_(self):
        """Get data paths list."""

        if self._fmt in ["ESRI Shapefile", "shp"]:
            datafiles = glob.glob(os.path.join(self._sourcedir, "*.shp"))
        else:
            datafiles = []

        return datafiles

    def _open_datasets_(self):
        """Open data files."""

        self._features_count = 0
        for datafile in self._datafiles:
            basename = os.path.basename(datafile)
            if basename not in self._cache["datafiles"]:
                if self._driver == "gdal":
                    driver = ogr.GetDriverByName("ESRI Shapefile")
                    dataset = driver.Open(datafile, 0)
                    layer = dataset.GetLayer(0)
                    # print(basename, layer)
                    # layerDefinition = layer.GetLayerDefn()
                    # for i in range(layerDefinition.GetFieldCount()):
                    # fieldName =  layerDefinition.GetFieldDefn(i).GetName()
                    # fieldTypeCode = layerDefinition.GetFieldDefn(i).GetType()
                    # fieldType = layerDefinition.GetFieldDefn(i).GetFieldTypeName(fieldTypeCode)
                    # fieldWidth = layerDefinition.GetFieldDefn(i).GetWidth()
                    # GetPrecision = layerDefinition.GetFieldDefn(i).GetPrecision()
                    # print(fieldName + " - " + fieldType+ " " + str(fieldWidth) + " " + str(GetPrecision))
                    self._features_count += layer.GetFeatureCount()
                    self._cache["datafiles"].append(basename)
                    self._cache["datasets"].append(dataset)
                    self._cache["layers"].append(layer)
                elif self._driver == "fiona":
                    raise NotImplementedError("opening datasets with fiona driver is not implemented yet")

    def get_value(self, lon, lat, *args, **kwargs):
        """Get vector value from longitude and latitude query."""

        if self._driver == "gdal":
            value = self._get_value_gdal_driver_(lon, lat, *args, **kwargs)
        elif self._driver == "rasterio":
            value = self._get_value_rasterio_driver_(lon, lat, *args, **kwargs)
        return value

    def _clean_cache_(self, last=False):
        """Clean cache."""

        # TODO

        # if last is True:
        # tilename_to_remove = self._cache["tilenames"].pop()
        # tile_to_close = self._cache["tiles"].pop()
        # band_to_close = self._cache["bands"].pop()
        # tmpdir_to_remove = self._cache["tmpdirs"].pop()
        # tile_to_close.close()
        # band_to_close = None
        # if tmpdir_to_remove is not None:
        # if tmpdir_to_remove not in self._cache["tmpdirs"]:
        # tmpdir_to_remove is not used by another tile so we can delete it
        # shutil.rmtree(tmpdir_to_remove)
        # else:
        # while len(self._cache["tiles"]) > 0:
        # tilename_to_remove = self._cache["tilenames"].pop()
        # tile_to_close = self._cache["tiles"].pop()
        # band_to_close = self._cache["bands"].pop()
        # tmpdir_to_remove = self._cache["tmpdirs"].pop()
        # if self._driver == "gdal":
        # tile_to_close = None
        # elif self._driver == "rasterio":
        # tile_to_close.close()
        # band_to_close = None
        # if tmpdir_to_remove is not None:
        # if tmpdir_to_remove not in self._cache["tmpdirs"]:
        # tmpdir_to_remove is not used by another tile so we can delete it
        # shutil.rmtree(tmpdir_to_remove)

    def _get_buffer_gdal_driver_(self, lon, lat, nx, ny, *args, **kwargs):
        """Get buffer data using GDAL."""

        tilename, tile, band = self._load_source_file_(lon, lat, *args, **kwargs)
        transform = tile.GetGeoTransform()
        xorig = transform[0]
        yorig = transform[3]
        dx = transform[1]
        dy = transform[5]
        col = int((lon - xorig) / dx)
        row = int((yorig - lat) / -dy)
        buffer_data = band.ReadAsArray(col - nx, row - ny, 2 * nx + 1, 2 * ny + 1).astype(np.float)
        return buffer_data

    def _get_buffer_rasterio_driver_(self, lon, lat, nx, ny, *args, **kwargs):
        """Get buffer data using rasterio."""

        # Initialize buffer
        buffer_data = np.ones((2 * ny + 1, 2 * nx + 1)) * np.nan

        # Get tile and indices corresponding to the center point
        tilename, tile, band = self._load_source_file_(lon, lat, *args, **kwargs)
        row, col = tile.index(lon, lat)

        # Loop on buffer points
        for bufrow in range(-ny, ny + 1):
            for bufcol in range(nx, nx + 1):
                if row + bufrow > -1 and row + bufrow < band.shape[0]:
                    if col + bufcol > -1 and col + bufcol < band.shape[1]:
                        buffer_data[bufrow, bufcol] = band[row + bufrow, col + bufcol]

        if np.any(np.isnan(buffer_data)):
            print("[ WARNING ] %i NaN values in buffer at (%f,%f)" % (int(np.sum(np.isnan(buffer_data))), lon, lat))

        return buffer_data

    def _get_value_gdal_driver_(self, lon, lat, *args, **kwargs):
        """Get vector value from longitude an dlatitude query using GDAL."""

        tilename, tile, band = self._load_source_file_(lon, lat, *args, **kwargs)
        transform = tile.GetGeoTransform()
        xorig = transform[0]
        yorig = transform[3]
        dx = transform[1]
        dy = transform[5]
        col = int((lon - xorig) / dx)
        row = int((yorig - lat) / -dy)
        value = band.ReadAsArray(col, row, 1, 1).astype(np.float).flatten()[0]
        return value

    def _get_value_rasterio_driver_(self, lon, lat, *args, **kwargs):
        """Get vector value from longitue and latitude query using rasterio."""

        tilename, tile, band = self._load_source_file_(lon, lat, *args, **kwargs)
        row, col = tile.index(lon, lat)
        try:
            value = band[row, col]
        except Exception:
            print(lon, lat, row, col)
            print(tilename)
            print(tile.transform)
            print(tile.crs)
            print(band.shape)
            print("extent:", tile.transform * band.shape)
            print("       ", tile.transform * (0, 0))
            value = np.nan

        return value

    def _load_source_file_(self, lon, lat, *args, **kwargs):  # noqa: C901
        """Load appropriate data file from longitude and lattude query."""

        tilename, tiledir, tilefile, tilearch = self.get_tile_info(lon, lat, *args, **kwargs)

        # Check if tile is in the cache
        tile_in_cache = False
        if tilename in self._cache["tilenames"]:
            tile_in_cache = True

            # Put tile in first place in the cache
            index = self._cache["tilenames"].index(tilename)
            # print(" - index=%i" % index)
            if index > 0:
                self._cache["tilenames"].insert(0, self._cache["tilenames"].pop(index))
                self._cache["tiles"].insert(0, self._cache["tiles"].pop(index))
                self._cache["bands"].insert(0, self._cache["bands"].pop(index))
                self._cache["tmpdirs"].insert(0, self._cache["tmpdirs"].pop(index))

            # Return from cache
            return tilename, self._cache["tiles"][0], self._cache["bands"][0]

        if "debug" in kwargs:
            if kwargs["debug"] is True:
                print("RastersCollection::_load_source_file_:")
                print(" - tiledir=%s" % tiledir)
                print(" - tilefile=%s" % tilefile)
                print(" - tilearch=%s" % repr(tilearch))

        use_archive = False
        if os.path.isdir(tiledir):
            if "debug" in kwargs:
                if kwargs["debug"] is True:
                    print(" - using existing directory:%s" % tiledir)
            if not os.path.isfile(tilefile):
                use_archive = True
            if tiledir in self._cache["tmpdirs"]:
                tmpdir = tiledir
            else:
                tmpdir = None
        else:
            if tilearch is not None:
                tiledir = os.path.join(tilearch[2], os.path.split(tilearch[1])[0])
                tmpdir = tiledir
                use_archive = True
            else:
                raise IOError("File not found %s and no tile archive provided" % tilefile)

        if use_archive:
            if "debug" in kwargs:
                if kwargs["debug"] is True:
                    print(" - extracting from archive")
            if tilearch is None:
                raise IOError("File not found %s and no tile archive provided" % tilefile)
            if "debug" in kwargs:
                if kwargs["debug"] is True:
                    print(" - using archive:%s" % repr(tilearch))
            if os.path.splitext(tilearch[0])[1] == ".zip":
                # TODO same as with MERIT (need another attribute with tilearch ?) for path in tar filef
                tiledir = os.path.join("/tmp", tiledir)
                if not os.path.isdir(tiledir):
                    os.mkdir(tiledir)
                zipIn = zipfile.ZipFile(tilearch, "r")
                zipIn.extractall(tiledir)
                zipIn.close()
                # tilefile = os.path.join(tiledir, tile, tile, "w001001.adf")
                tilefile = os.path.join(tiledir, tilename, tilename, "w001001.adf")
            elif os.path.splitext(tilearch[0])[1] == ".tar":
                tar = tarfile.TarFile(tilearch[0], mode="r", debug=0, errorlevel=2)
                try:
                    tar.extract(tilearch[1], tilearch[2])
                    if "debug" in kwargs:
                        if kwargs["debug"] is True:
                            print(" - extracted %s in %s" % (tilearch[1], tiledir))
                except Exception as err:
                    raise RuntimeError("error extracting tarfile: %s (%s)" % (tilearch[0], repr(err))) from err
                tar.close()
                tilefile = os.path.join(tiledir, tilefile)

        if not os.path.isfile(tilefile):
            raise IOError("File not found: %s" % tilefile)

        if self._driver == "gdal":
            tile = gdal.Open(tilefile)
            band = tile.GetRasterBand(1)
        elif self._driver == "rasterio":
            tile = rasterio.open(tilefile)
            band = tile.read(1)

        if not tile_in_cache:
            # Add tile in the cache
            self._cache["tilenames"].insert(0, tilename)
            self._cache["tiles"].insert(0, tile)
            self._cache["bands"].insert(0, band)
            self._cache["tmpdirs"].insert(0, tmpdir)

            # Clean cache
            if len(self._cache["tilenames"]) > self._cache_size:
                self._clean_cache_(last=True)

        return tilename, tile, band

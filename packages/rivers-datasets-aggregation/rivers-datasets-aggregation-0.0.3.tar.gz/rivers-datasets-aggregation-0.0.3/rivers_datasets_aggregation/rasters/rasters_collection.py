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

"""RastersCollection class for optimized raster data handling."""

# pylint: disable=consider-using-f-string, invalid-name, broad-exception-caught, import-error
# pylint: disable=unused-variable, too-many-branches, consider-using-with, keyword-arg-before-vararg
# pylint: disable=assignment-from-no-return
import os
import shutil
import tarfile
import zipfile

import numpy as np
import rasterio
# from osgeo import gdal


class RastersCollection:
    """Raster data collection class for memory-optimized raster handling."""

    def __init__(self, sourcedir, cache_size, driver="rasterio"):
        """Constructor."""

        # Check arguments
        if not isinstance(cache_size, int):
            raise ValueError("cache_size must be of type 'int'")
        if cache_size < 1:
            raise ValueError("cache_size must be greater than zero")
        # if driver not in ["gdal", "rasterio"]:
        #     raise ValueError("driver must be 'gdal' or 'rasterio'")
        if driver != "rasterio":
            raise ValueError("driver must be 'rasterio'")

        self._sourcedir = sourcedir
        self._cache_size = cache_size
        self._driver = driver
        self._cache = {"tilenames": [], "tiles": [], "bands": [], "tmpdirs": []}

    def __del__(self):
        """Clean cache."""

        self._clean_cache_(last=False)

    def get_tile_info(self, lon, lat, *args, **kwargs):
        """Get specific rasters collection tile information."""

    def get_buffer_mean(self, lon, lat, nx, ny, weights=None, *args, **kwargs):
        """Get buffer mean."""

        buffer_data = self.get_buffer(lon, lat, nx, ny, weights, *args, **kwargs)
        return np.nanmean(buffer_data.flatten())

    def get_buffer(self, lon, lat, nx, ny, weights=None, *args, **kwargs):
        """Get buffer."""

        if self._driver == "gdal":
            buffer_data = self._get_buffer_gdal_driver_(lon, lat, nx, ny, *args, **kwargs)
        elif self._driver == "rasterio":
            buffer_data = self._get_buffer_rasterio_driver_(lon, lat, nx, ny, *args, **kwargs)

        if weights is not None:
            # Check weights
            if weights.shape != (2 * ny + 1, 2 * nx + 1):
                raise ValueError("'weights' must be of shape (%i,%i)" % (2 * ny + 1, 2 * nx + 1))

            buffer_data *= weights

        return buffer_data

    def get_value(self, lon, lat, *args, **kwargs):
        """Get raster value from longitude and latitude query."""

        if self._driver == "gdal":
            value = self._get_value_gdal_driver_(lon, lat, *args, **kwargs)
        elif self._driver == "rasterio":
            value = self._get_value_rasterio_driver_(lon, lat, *args, **kwargs)
        return value

    def _clean_cache_(self, last=False):
        """Clean cache."""

        if last is True:
            # tilename_to_remove = self._cache["tilenames"].pop()
            _ = self._cache["tilenames"].pop()
            tile_to_close = self._cache["tiles"].pop()
            band_to_close = self._cache["bands"].pop()
            # _ = self._cache["bands"].pop()
            tmpdir_to_remove = self._cache["tmpdirs"].pop()
            tile_to_close.close()
            band_to_close = None
            if tmpdir_to_remove is not None:
                if tmpdir_to_remove not in self._cache["tmpdirs"]:
                    # tmpdir_to_remove is not used by another tile so we can delete it
                    shutil.rmtree(tmpdir_to_remove)
        else:
            while len(self._cache["tiles"]) > 0:
                # tilename_to_remove = self._cache["tilenames"].pop()
                _ = self._cache["tilenames"].pop()
                tile_to_close = self._cache["tiles"].pop()
                band_to_close = self._cache["bands"].pop()
                # _ = self._cache["bands"].pop()
                tmpdir_to_remove = self._cache["tmpdirs"].pop()
                if self._driver == "gdal":
                    tile_to_close = None
                elif self._driver == "rasterio":
                    tile_to_close.close()
                band_to_close = None  # noqa: F841
                if tmpdir_to_remove is not None:
                    if tmpdir_to_remove not in self._cache["tmpdirs"]:
                        # tmpdir_to_remove is not used by another tile so we can delete it
                        shutil.rmtree(tmpdir_to_remove)

    def _get_buffer_gdal_driver_(self, lon, lat, nx, ny, *args, **kwargs):
        """Get buffer data with GDAL."""

        tilename, tile, band = self._load_source_file_(lon, lat, *args, **kwargs)
        transform = tile.GetGeoTransform()
        xorig = transform[0]
        yorig = transform[3]
        dx = transform[1]
        dy = transform[5]
        col = int((lon - xorig) / dx)
        row = int((yorig - lat) / -dy)
        buffer_data = band.ReadAsArray(col - nx, row - ny, 2 * nx + 1, 2 * ny + 1).astype(float)
        return buffer_data

    def _get_buffer_rasterio_driver_(self, lon, lat, nx, ny, *args, **kwargs):
        """Get buffer data with rasterio."""

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
        """Get raster value from longitude and latitude query with GDAL."""

        tilename, tile, band = self._load_source_file_(lon, lat, *args, **kwargs)
        transform = tile.GetGeoTransform()
        xorig = transform[0]
        yorig = transform[3]
        dx = transform[1]
        dy = transform[5]
        col = int((lon - xorig) / dx)
        if col >= tile.RasterXSize:
            col = tile.RasterXSize - 1
        row = int((yorig - lat) / -dy)
        if row >= tile.RasterYSize:
            row = tile.RasterYSize - 1
        try:
            value = band.ReadAsArray(col, row, 1, 1).astype(float).flatten()[0]
        except Exception as exception:
            print(tilename, (int(-lon / 5) + 1) * 5)
            print(tilename, (int(-(lon + 0.0001) / 5) + 1) * 5)
            print(tilename, (int(-(lon - 0.0001) / 5) + 1) * 5)
            print(xorig, yorig)
            print(xorig + tile.RasterXSize * dx, yorig + tile.RasterYSize * dy)
            print(lon, lat)
            raise ValueError("Failed to get raster value with GDAL.") from exception

        return value

    def _get_value_rasterio_driver_(self, lon, lat, *args, **kwargs):
        """Get raster value from longitude and latitude query with rasterio."""

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
        """Load appropriate tile data from longitude and latitude query."""

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
                # TODO same as with MERIT (need another attribute with tilearch ?) for path in tar file
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

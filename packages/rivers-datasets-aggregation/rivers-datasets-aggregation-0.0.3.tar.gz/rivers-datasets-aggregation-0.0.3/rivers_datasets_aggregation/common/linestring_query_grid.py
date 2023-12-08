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

"""LineStringQueryGrid class"""

# pylint: disable=invalid-name, too-many-arguments, import-error, too-many-branches
# pylint: disable=consider-using-f-string, no-name-in-module, chained-comparison
import fiona
import numpy as np
from fiona.crs import from_epsg
from osgeo import ogr
from shapely.geometry import Polygon, mapping

from rivers_datasets_aggregation.common.progress import Progress


class LinestringQueryCell:
    """LineStringQueryCell class."""

    def __init__(self, index, bbox):
        """Constructor."""

        self._index = index
        self._bbox = bbox
        self._entries = []

    @property
    def index(self):
        """Get index attribute."""

        return self._index

    @property
    def bbox(self):
        """Get bbox attribute."""

        return self._bbox

    @property
    def entries(self):
        """Get entries attribute."""

        return self._entries

    def add_entry(self, entry, index=None):
        """Add a LineStringQueryCell entry."""
        if index is None:
            self._entries.append(entry)
        else:
            self._entries.append(index)


class LinestringQueryGrid:
    """LinestringQueryGrid class."""

    def __init__(
        self,
        xmin,
        xmax,
        ymin,
        ymax,
        nx=None,
        ny=None,
        dx=None,
        dy=None,
        periodx=None,
        periody=None,
    ):
        """
        Constructor.

        Parameters
        ----------
            xmin : minimum value for x
            ymin : maximum value for y
            xmax : minimum value for x
            ymax : maximum value for y
        """

        # Create Grid
        if nx is None:
            if dx is None:
                raise ValueError("A value for 'dx' or 'nx' must be given")

            nx = int(np.ceil((xmax - xmin) / dx))

        if ny is None:
            if dy is None:
                raise ValueError("A value for 'dy' or 'ny' must be given")

            ny = int(np.ceil((ymax - ymin) / dy))

        self._xmin = xmin
        self._xmax = xmax
        self._nx = nx
        self._ymin = ymin
        self._ymax = ymax
        self._ny = ny
        self._x = np.linspace(xmin, xmax, nx + 1, endpoint=True)
        self._y = np.linspace(ymin, ymax, ny + 1, endpoint=True)
        self.periodx = periodx
        self.periody = periody
        self._cells = []
        for i in range(0, ny):
            for j in range(0, nx):
                index = i * nx + j
                self._cells.append(LinestringQueryCell(index, (self._x[j], self._x[j + 1], self._y[i], self._y[i + 1])))

    def add_entries(self, entries, store_index=True, index_attribute=None):
        """Add entries."""

        count = len(entries)
        progress = Progress(0, count, 20, prefix="Populating LinestringQueryGrid")

        for index, entry in enumerate(entries):
            if store_index is True:
                if index_attribute is not None:
                    if isinstance(entry, ogr.Feature):
                        entry_index = entry.GetField(index_attribute)
                    elif isinstance(entry, dict):
                        entry_index = entry["properties"][index_attribute]
                    else:
                        raise ValueError("wrong entry type: %s" % type(entry))
                else:
                    entry_index = index
                self.add_entry(entry, entry_index=entry_index)
            else:
                self.add_entry(entry)
            progress.advance()
        progress.finalize()

    def add_entry(self, entry, entry_index=None):  # noqa: C901
        """Add entry."""

        indices = []
        if isinstance(entry, ogr.Feature):
            # Retrieve points from an OGR feature
            geometry = entry.GetGeometryRef()
            if geometry.GetGeometryName() == "LINESTRING":
                # Retrieve geometry points
                points = []
                for i in range(0, geometry.GetPointCount()):
                    points.append(geometry.GetPoint(i))
            elif geometry.GetGeometryName() == "MULTILINESTRING":
                # Iterate over geometries to get all points
                points = []
                multiline = geometry
                for geometry in multiline:
                    for i in range(0, geometry.GetPointCount()):
                        points.append(geometry.GetPoint(i))

        elif isinstance(entry, dict):
            # Retrieve points from a feature dict (Fiona)
            geometry = entry["geometry"]
            if geometry["type"] == "LineString":
                points = geometry["coordinates"]
            elif geometry["type"] == "MultiLineString":
                coordinates = geometry["coordinates"]
                points = coordinates[0]
                for linestring in coordinates[1:]:
                    points += linestring
            else:
                raise NotImplementedError("Geometry type not implemented: %s" % geometry["type"])
        else:
            raise ValueError("wrong entry type: %s" % type(entry))

        for point in points:
            # print(point)
            try:
                index = self.get_cell_index(*point)
            except Exception as exception:
                # print(entry)
                # print(point)
                raise ValueError("An error has occured while getting cell index") from exception
            if index == -1:
                index = self.get_cell_index(*point, verbose=True)
                raise RuntimeError("Point %s out of grid" % str(point))
            indices.append(index)
        for index in set(indices):
            self._cells[index].add_entry(entry, index=entry_index)

    def get_cell_index(self, x, y, verbose=False):
        """Get cell index from x and y coordinates."""

        index = self._get_cell_index_(x, y, verbose)
        if index == -1 and self.periodx:
            index_plus_periodx = self._get_cell_index_(x + self.periodx, y, verbose)
            if index_plus_periodx > -1:
                return index_plus_periodx

            index_minus_periodx = self._get_cell_index_(x - self.periodx, y, verbose)
            return index_minus_periodx

        return index

    # def get_cell(self, x, y):
    #     """Get cell from x and y coordinates."""

    #     index = self.get_cell_index(x, y)
    #     if index == -1:
    #         raise RuntimeError("Point (%f,%f) out of grid" % (x, y))
    #     return self._cells[row * self._nx + col]

    def get_cells(self, x, y):
        """Get cells from x and y coordinates."""

        index = self.get_cell_index(x, y)
        if index == -1:
            raise RuntimeError("Point (%f,%f) out of grid" % (x, y))
        row = int(index / self._nx)
        col = index % self._nx
        cells = []
        for row1 in range(row - 1, row + 2):
            for col1 in range(col - 1, col + 2):
                if row1 > -1 and row1 < self._ny and col1 > -1 and col1 < self._nx:
                    cells.append(self._cells[row1 * self._nx + col1])
        return cells

    @property
    def cells(self):
        """Get cells parameter."""

        return self._cells

    def save_cells_tiles(self, fname):
        """Save cells tiles."""

        schema = {"geometry": "Polygon", "properties": {"index": "int"}}
        shpout = fiona.open(fname, "w", crs=from_epsg(4326), driver="ESRI Shapefile", schema=schema)
        for cell in self._cells:
            polygon = Polygon(
                [
                    (cell.bbox[0], cell.bbox[2]),
                    (cell.bbox[1], cell.bbox[2]),
                    (cell.bbox[1], cell.bbox[3]),
                    (cell.bbox[0], cell.bbox[3]),
                    (cell.bbox[0], cell.bbox[2]),
                ]
            )
            properties = {"index": cell.index}
            shpout.write({"geometry": mapping(polygon), "properties": properties})
        shpout.close()

    def save_cells_content(self, fname):
        """Save cells content."""

        schema = {"geometry": "LineString", "properties": {"index": "int"}}
        shpout = fiona.open(fname, "w", crs=from_epsg(4326), driver="ESRI Shapefile", schema=schema)
        for cell in self._cells:
            for entry in cell.entries:
                properties = {"index": cell.index}
                shpout.write({"geometry": entry["geometry"], "properties": properties})
        shpout.close()

    def _get_cell_index_(self, x, y, verbose=False):
        """Get cell index from x and y coordinates."""

        col = int((x - self._xmin) * self._nx / (self._xmax - self._xmin))
        row = int((y - self._ymin) * self._ny / (self._ymax - self._ymin))
        if verbose:
            print("col=%i/%i (x=%f, xmin=%f, xmax=%f)" % (col, self._nx, x, self._xmin, self._xmax))
            print("row=%i/%i (y=%f, ymin=%f, ymax=%f)" % (row, self._ny, y, self._ymin, self._ymax))
        if col >= self._nx or col < 0 or row >= self._ny or row < 0:
            return -1
        return row * self._nx + col

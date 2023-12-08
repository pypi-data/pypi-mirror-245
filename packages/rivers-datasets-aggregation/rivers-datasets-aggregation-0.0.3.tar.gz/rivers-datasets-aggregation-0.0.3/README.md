# rivers-datasets-aggregation
A toolbox for grid and vector data aggregation on river stations.

### Overview

Module features : 

- __Extract__ raster values corresponding to a dataset of points (river stations)
- __Relocate__ a dataset of points (river stations) on a river network

### Getting started

##### Option 1 - Virtual environment

Create a virtual environment with venv:

```
python3 -m venv rda_venv
source rda_venv/bin/activate

pip install -e .
pip install -e .[dev]

pre-commit install
```

##### Option 2 - Conda environment

Create a virtual environment with conda: 

```
conda env create -f environment.yml
conda activate aggregation

pre-commit install
```

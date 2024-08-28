# PathPlanner

## Python Dependencies

Install using `pip` as follows.

```commandline
pip install -r requirements.txt
```

## Directory Structure

* `.venv`: Create python virtual environment in this folder
* `gis_backend`: Python programs related to the download, format conversion,
  storage, query, and visualization of OSM data.
* `gis_data`: Compiled GIS data and OSMNX cache.
* `route_engine`: Python code related to route engine.
* `tests`: Contains unit tests

## Running Unit Tests

In the project directory, use the following command to run all tests.

```commandline
python -m unittest discover .
```

## Quick Start

Retrieve data from OSM

```commandline
python -m gis_backend --fetch-place "Raleigh, NC"
```

## Examples

For an example routing problem, refer to `example.py`.



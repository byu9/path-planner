# PathPlanner

## Python Dependencies

Install the following packages via `pip`:

* `geopandas=1.0.0a1` Install this known-good version.
* `osmnx` for downloading and visualizing street networks from OpenStreetMap
* `pyside6` required by the interactive map viewer using Qt WebEngine
* `folium` GeoPandas plotting dependency
* `matplotlib` GeoPandas plotting dependency
* `mapclassify` GeoPandas plotting dependency

## Directory Structure

* `.venv`: Create python virtual environment in this folder
* `gis_backend`: Python programs related to the download, format conversion,
  storage, query, and visualization of OSM data.
* `osmnx_cache`: Download cache managed by OSMNX
* `gis_database`: Simplified Node and Edge tables in GeoJSON format. This
  represents an abstract topology with junctions/crossings and buildings as
  nodes, roadways as edges. The geometry of roadways is also stored in this
  table as polylines.
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
python -m gis_backend.osm_fetcher
```

Then run `run_map_viewer.py` to see Centennial Parkway being plotted.


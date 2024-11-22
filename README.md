# Path Planner Project

## Python Dependencies

Install using `pip` as follows.

```commandline
pip install -r requirements.txt
```

## Fetching GIS data

Retrieve data from OSM

```commandline
python -m gis_backend --fetch-place "Raleigh, NC"
```

## Files and Directory Structure

* `.venv`: Create python virtual environment in this folder
* `gis_backend`: Python programs related to the download, format conversion,
  storage, query, and visualization of OSM data.
* `gis_data`: Compiled GIS data and OSMNX cache.
* `route_engine`: Python code related to route engine.
* `test_problem`: Contains the provided test problem
* `test_solution`: Contains solution to the provided test problem

Run `solve_test_problem.py` to run the test problem.




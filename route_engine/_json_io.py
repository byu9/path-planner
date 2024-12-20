import json
from collections.abc import Hashable
from collections.abc import Iterable
from typing import Any

from gis_backend.query_provider import get_node_near_address
from gis_backend.query_provider import get_node_near_coord
from ._problem_description import VehicleParams
from ._problem_description import VehicleRoutingProblem
from ._problem_description import WaypointParams


def _load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)


def _reindex_by_primary_key(records: Iterable[dict[Hashable, Any]], key: Hashable):
    keyed_records = {
        item[key]: item
        for item in records
    }
    return keyed_records


class JSONStorageProvider:
    def __init__(self):
        self._depots_filename = 'depots.json'
        self._vehicles_filename = 'vehicles.json'
        self._vehicle_models_filename = 'vehicle_models.json'
        self._stops_filename = 'stops.json'
        self._segments_filename = 'trip_segments.json'

    def load_problem(self, folder) -> VehicleRoutingProblem:
        depot_json = _load_json(f'{folder}/{self._depots_filename}')
        vehicle_json = _load_json(f'{folder}/{self._vehicles_filename}')
        vehicle_model_json = _load_json(f'{folder}/{self._vehicle_models_filename}')
        stop_json = _load_json(f'{folder}/{self._stops_filename}')
        segment_json = _load_json(f'{folder}/{self._segments_filename}')

        depot_data_by_id = _reindex_by_primary_key(depot_json, key='id')
        vehicle_data_by_id = _reindex_by_primary_key(vehicle_json, key='id')
        vehicle_model_data_by_id = _reindex_by_primary_key(vehicle_model_json, key='id')
        stop_data_by_id = _reindex_by_primary_key(stop_json, key='id')

        # Fixup depot data fields
        for depot_id, depot_data in depot_data_by_id.items():
            depot_data['dispatch_osm_node'] = get_node_near_coord(
                lat=depot_data['latitude'],
                long=depot_data['longitude']
            )
            depot_data['recall_osm_node'] = get_node_near_address(
                '303 Ashe Ave Raleigh, NC 27606 United States')

        # Fixup stop data fields
        for stop_id, stop_data in stop_data_by_id.items():
            stop_data['osm_node'] = get_node_near_address(stop_data['address'])

        # Construct problem
        problem = VehicleRoutingProblem()

        for vehicle_id, vehicle_data in vehicle_data_by_id.items():
            depot = depot_data_by_id[vehicle_data['depot_id']]
            vehicle_model = vehicle_model_data_by_id[vehicle_data['vehicle_model']]
            start_activity_after, finish_activity_before = vehicle_data['operation_window']

            vehicle_params = VehicleParams(
                depot=depot['name'],

                dispatch_from_gis_node=depot['dispatch_osm_node'],
                recall_to_gis_node=depot['recall_osm_node'],

                earliest_activity_hour=start_activity_after,
                latest_activity_hour=finish_activity_before,

                fuel_capacity=vehicle_model['battery_capacity'],
                cargo_capacity=vehicle_model['payload_capacity'],
            )

            problem.add_vehicle(f'Vehicle-{vehicle_id}', vehicle_params)

        # Scan the segments file to grab waypoint info
        list_of_stops_in_segment_file = list()
        for segment_data in segment_json:
            list_of_stops_in_segment_file.append(segment_data['origin'])
            list_of_stops_in_segment_file.extend(segment_data['stops'])
            list_of_stops_in_segment_file.append(segment_data['destination'])

        for stop_in_segment_file in list_of_stops_in_segment_file:
            stop_id = stop_in_segment_file['stop_id']
            stop_data = stop_data_by_id[stop_id]
            waypoint_name = f'Waypoint-{stop_id}'

            if waypoint_name not in problem.waypoints:

                waypoint_params = WaypointParams(
                    waypoint=waypoint_name,
                    gis_node=stop_data['osm_node'],

                    earliest_arrival_hour=stop_in_segment_file['arrival_min'],
                    latest_arrival_hour=stop_in_segment_file['arrival_max']
                )
                problem.add_waypoint(waypoint_name, waypoint_params)

            else:
                waypoint_params = problem.waypoint_params(waypoint_name)

            # Accumulate the following quantities found in the segments file
            waypoint_params.cargo_demand += stop_in_segment_file['payload_add']
            waypoint_params.dwell_hours += stop_in_segment_file['stop_duration']

        return problem

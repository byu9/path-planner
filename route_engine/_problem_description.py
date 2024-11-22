from dataclasses import dataclass
from itertools import permutations
from pprint import pformat
from typing import Hashable
from typing import Iterable
from typing import Optional
from typing import Tuple

from gis_backend.query_provider import get_path_metric
from gis_backend.query_provider import get_shortest_path_between


@dataclass
class VehicleInfo:
    dispatch_from_osm_node: Optional[Hashable] = None
    recall_to_osm_node: Optional[Hashable] = None
    fuel_capacity: Optional[float] = None
    cargo_capacity: Optional[float] = None
    earliest_dispatch_time: Optional[float] = None
    latest_recall_time: Optional[float] = None


@dataclass
class WaypointInfo:
    osm_node: Hashable
    cargo_demand: float = 0
    earliest_arrival_time: Optional[float] = None
    latest_arrival_time: Optional[float] = None
    stop_duration: float = 0


class VehicleRoutingProblem:
    def __init__(self, cost_metric='travel_time'):
        self._cost_metric = cost_metric

        self._vehicles = dict()
        self._waypoints = dict()

        self._trips = set()
        self._trip_costs = dict()
        self._trip_geometries = dict()

        self._dispatch_costs = dict()
        self._recall_costs = dict()
        self._dispatch_geometries = dict()
        self._recall_geometries = dict()

    def __str__(self):
        lines = list()
        lines.append('Vehicle Routing Problem')

        pretty_print_data = {
            'Cost metric': self._cost_metric,

            'Vehicles': self._vehicles,
            'Waypoints': self._waypoints,

            'Trips': self._trips,
            'Trip costs': self._trip_costs,

            'Dispatch costs': self._dispatch_costs,
            'Recall costs': self._recall_costs,
        }
        lines.append(pformat(pretty_print_data))

        return '\n'.join(lines)

    def add_vehicle(self, name: Hashable, info: VehicleInfo):
        if name in self._vehicles:
            raise ValueError(f'Cannot add vehicle: Vehicle "{name}" exists.')

        self._vehicles[name] = info

    def add_waypoint(self, name: Hashable, info: WaypointInfo):
        if name in self._waypoints:
            raise ValueError(f'Cannot add waypoint: Waypoint "{name}" exists.')

        self._waypoints[name] = info

    def get_vehicle_info(self, name: Hashable) -> VehicleInfo:
        return self._vehicles[name]

    def get_waypoint_info(self, name: Hashable) -> WaypointInfo:
        return self._waypoints[name]

    def compute_edges(self):
        for trip_start, trip_end in permutations(self._waypoints, r=2):
            path = get_shortest_path_between(
                self._waypoints[trip_start].osm_node,
                self._waypoints[trip_end].osm_node
            )

            trip = trip_start, trip_end

            self._trips.add(trip)
            self._trip_geometries[trip] = path
            self._trip_costs[trip] = get_path_metric(path, metric=self._cost_metric)

        for vehicle in self._vehicles:
            for waypoint in self._waypoints:
                dispatch_path = get_shortest_path_between(
                    self._vehicles[vehicle].dispatch_from_osm_node,
                    self._waypoints[waypoint].osm_node
                )

                recall_path = get_shortest_path_between(
                    self._waypoints[waypoint].osm_node,
                    self._vehicles[vehicle].recall_to_osm_node
                )

                self._dispatch_costs[vehicle, waypoint] = get_path_metric(dispatch_path, metric=self._cost_metric)
                self._recall_costs[vehicle, waypoint] = get_path_metric(recall_path, metric=self._cost_metric)

                self._dispatch_geometries[vehicle, waypoint] = dispatch_path
                self._recall_geometries[vehicle, waypoint] = recall_path

    @property
    def vehicles(self) -> Iterable[Hashable]:
        return self._vehicles

    @property
    def waypoints(self) -> Iterable[Hashable]:
        return self._waypoints

    @property
    def trips(self) -> Iterable[Tuple[Hashable, Hashable]]:
        return self._trips


class VehicleRoutingProblemSolution:
    pass

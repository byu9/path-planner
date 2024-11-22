from dataclasses import dataclass
from itertools import permutations
from pprint import pformat
from typing import Hashable
from typing import Iterable
from typing import Optional

from gis_backend.query_provider import get_path_metric
from gis_backend.query_provider import get_shortest_path_between


@dataclass
class VehicleInfo:
    depot: Hashable
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
    def __init__(self):
        self._cost_metric = None

        self._vehicles = dict()
        self._waypoints = dict()

        self._trips = set()
        self._trip_costs = dict()

        self._dispatch_costs = dict()
        self._recall_costs = dict()

        self._trip_geometries = dict()
        self._dispatch_geometries = dict()
        self._recall_geometries = dict()

    def __str__(self):
        lines = list()
        lines.append('Vehicle Routing Problem')

        pretty_print_data = {
            'Cost metric': self._cost_metric,

            'Vehicles': self._vehicles,
            'Waypoints': self._waypoints,

            'Trip costs': self._trip_costs,

            'Dispatch costs': self._dispatch_costs,
            'Recall costs': self._recall_costs,
        }
        lines.append(pformat(pretty_print_data))

        return '\n'.join(lines)

    def set_vehicle(self, name: Hashable, info: VehicleInfo):
        if name in self._vehicles:
            raise ValueError(f'Cannot set vehicle: Vehicle "{name}" exists.')

        self._vehicles[name] = info

    def set_waypoint(self, name: Hashable, info: WaypointInfo):
        if name in self._waypoints:
            raise ValueError(f'Cannot set waypoint: Waypoint "{name}" exists.')

        self._waypoints[name] = info

    def vehicle(self, name: Hashable) -> VehicleInfo:
        return self._vehicles[name]

    def waypoint(self, name: Hashable) -> WaypointInfo:
        return self._waypoints[name]

    def compute_costs(self, metric):
        self._cost_metric = metric

        for trip_start, trip_end in permutations(self._waypoints, r=2):
            path = get_shortest_path_between(
                self._waypoints[trip_start].osm_node,
                self._waypoints[trip_end].osm_node
            )

            trip = trip_start, trip_end

            self._trips.add(trip)
            self._trip_geometries[trip] = path
            self._trip_costs[trip] = get_path_metric(path, metric=metric)

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

                self._dispatch_costs[vehicle, waypoint] = get_path_metric(dispatch_path, metric=metric)
                self._recall_costs[vehicle, waypoint] = get_path_metric(recall_path, metric=metric)

                self._dispatch_geometries[vehicle, waypoint] = dispatch_path
                self._recall_geometries[vehicle, waypoint] = recall_path

    @property
    def vehicles(self) -> Iterable[Hashable]:
        return self._vehicles

    @property
    def waypoints(self) -> list[Hashable]:
        return list(self._waypoints)

    @property
    def trips(self) -> Iterable[tuple[Hashable, Hashable]]:
        return self._trips

    def trips_to(self, waypoint: Hashable) -> Iterable[tuple[Hashable, Hashable]]:
        for trip_from, trip_to in self.trips:
            if trip_to == waypoint:
                yield trip_from, trip_to

    def trips_from(self, waypoint: Hashable) -> Iterable[tuple[Hashable, Hashable]]:
        for trip_from, trip_to in self.trips:
            if trip_from == waypoint:
                yield trip_from, trip_to

    def trip_cost(self, trip: tuple[Hashable, Hashable]) -> float:
        return self._trip_costs[trip]

    def dispatch_cost(self, vehicle: Hashable, waypoint: Hashable) -> float:
        return self._dispatch_costs[vehicle, waypoint]

    def recall_cost(self, vehicle: Hashable, waypoint: Hashable) -> float:
        return self._recall_costs[vehicle, waypoint]

    def dispatch_geometry(self, vehicle: Hashable, waypoint: Hashable) -> list[Hashable]:
        return self._dispatch_geometries[vehicle, waypoint]

    def recall_geometry(self, vehicle: Hashable, waypoint: Hashable) -> list[Hashable]:
        return self._recall_geometries[vehicle, waypoint]

    def trip_geometry(self, trip: tuple[Hashable, Hashable]) -> list[Hashable]:
        return self._trip_geometries[trip]


@dataclass
class TripActivity:
    trip: tuple[Hashable, Hashable]
    cargo_level: float
    cargo_to_drop_off: float

    # To be filled using information in the problem
    from_osm_node: Optional[Hashable] = None
    to_osm_node: Optional[Hashable] = None
    cost: Optional[float] = None


@dataclass
class DispatchActivity:
    target_waypoint: Hashable
    cargo_level: float
    cargo_to_drop_off: float

    # To be filled using information in the problem
    depot: Optional[Hashable] = None
    from_osm_node: Optional[Hashable] = None
    to_osm_node: Optional[Hashable] = None
    cost: Optional[float] = None


@dataclass
class RecallActivity:
    origin_waypoint: Hashable
    cargo_level: float

    # To be filled using information in the problem
    depot: Optional[Hashable] = None
    from_osm_node: Optional[Hashable] = None
    to_osm_node: Optional[Hashable] = None
    cost: Optional[float] = None


class VehicleRoutingProblemSolution:
    def __init__(self, problem: VehicleRoutingProblem):
        self._problem = problem

        self._vehicle_dispatches: dict[Hashable, DispatchActivity] = dict()
        self._vehicle_recalls: dict[Hashable, RecallActivity] = dict()
        self._vehicle_trips: dict[Hashable, list[TripActivity]] = {
            vehicle: list()
            for vehicle in problem.vehicles
        }

    def __str__(self):
        lines = list()
        lines.append('Vehicle Routing Problem Solution')

        pretty_print_data = {
            'Trips': self._vehicle_trips,
            'Dispatches': self._vehicle_dispatches,
            'Recalls': self._vehicle_recalls,
        }
        lines.append(pformat(pretty_print_data))

        return '\n'.join(lines)

    @property
    def problem(self) -> VehicleRoutingProblem:
        return self._problem

    def add_dispatch(self, vehicle: Hashable, activity: DispatchActivity):
        if vehicle in self._vehicle_dispatches:
            raise ValueError(f'Error setting vehicle dispatch: {vehicle} already set.')

        self._vehicle_dispatches[vehicle] = activity

    def add_recall(self, vehicle: Hashable, activity: RecallActivity):
        if vehicle in self._vehicle_recalls:
            raise ValueError(f'Error setting vehicle recall: {vehicle} already set.')

        self._vehicle_recalls[vehicle] = activity

    def add_trip(self, vehicle: Hashable, activity: TripActivity):
        self._vehicle_trips[vehicle].append(activity)

    def compile(self):
        for vehicle in self._problem.vehicles:
            self._sort_trips(vehicle)

        for vehicle, activity in self._vehicle_dispatches.items():
            activity.from_osm_node = self._problem.vehicle(vehicle).dispatch_from_osm_node
            activity.to_osm_node = self._problem.waypoint(activity.target_waypoint).osm_node
            activity.cost = self._problem.dispatch_cost(vehicle, activity.target_waypoint)
            activity.depot = self._problem.vehicle(vehicle).depot

        for vehicle, activity in self._vehicle_recalls.items():
            activity.from_osm_node = self._problem.waypoint(activity.origin_waypoint).osm_node
            activity.to_osm_node = self._problem.vehicle(vehicle).recall_to_osm_node
            activity.cost = self._problem.recall_cost(vehicle, activity.origin_waypoint)
            activity.depot = self._problem.vehicle(vehicle).depot

        for vehicle, trips in self._vehicle_trips.items():
            for trip_data in trips:
                trip_start, trip_end = trip_data.trip
                trip_data.from_osm_node = self._problem.waypoint(trip_start).osm_node
                trip_data.to_osm_node = self._problem.waypoint(trip_end).osm_node
                trip_data.cost = self._problem.trip_cost((trip_start, trip_end))

    def _sort_trips(self, vehicle):
        if not self._vehicle_trips[vehicle]:
            return

        next_waypoint = dict()  # trip_start: trip_end
        for trip_data in self._vehicle_trips[vehicle]:
            trip_start, trip_end = trip_data.trip
            next_waypoint[trip_start] = trip_end
            next_waypoint[trip_end] = next_waypoint.get(trip_end, None)

        parentless_waypoints = set(next_waypoint.keys()) - set(next_waypoint.values())
        if len(parentless_waypoints) != 1:
            raise ValueError(f'Unable to sort trips: multiple parentless waypoints {parentless_waypoints}.')

        trip_data_by_trip = {
            trip_data.trip: trip_data
            for trip_data in self._vehicle_trips[vehicle]
        }

        first_waypoint, = parentless_waypoints
        waypoint_order = list()

        waypoint = first_waypoint
        while waypoint is not None:
            waypoint_order.append(waypoint)
            waypoint = next_waypoint[waypoint]

        sorted_trips = [
            trip_data_by_trip[trip]
            for trip in zip(waypoint_order[:-1], waypoint_order[1:])
        ]

        self._vehicle_trips[vehicle] = sorted_trips

    def trip_activity(self, vehicle: Hashable) -> list[TripActivity]:
        return self._vehicle_trips[vehicle]

    def dispatch_activity(self, vehicle: Hashable) -> DispatchActivity:
        return self._vehicle_dispatches.get(vehicle, None)

    def recall_activity(self, vehicle: Hashable) -> RecallActivity:
        return self._vehicle_recalls.get(vehicle, None)

    #
    # def add_trip_to_tour(self, vehicle: Hashable, trip: tuple[Hashable, Hashable]):
    #     trip_start, trip_end = trip
    #     next_waypoints = self._next_waypoints[vehicle]
    #
    #     if next_waypoints.get(trip_start, None) is not None:
    #         raise ValueError(f'Error adding {trip}: existing trip with identical trip start.')
    #
    #     next_waypoints[trip_start] = trip_end
    #     if trip_end not in next_waypoints:
    #         next_waypoints[trip_end] = None
    #

    #
    # tour = list()
    # waypoint = first_waypoint
    # while waypoint is not None:
    #     tour.append(waypoint)
    #     waypoint = next_waypoints[waypoint]
    #
    # last_waypoint = tour[-1]
    #
    # if vehicle in self._dispatches:
    #     dispatch_target = self._dispatches[vehicle].target
    #
    #     # If vehicle is dispatched, the first waypoint should be the dispatch target
    #     if dispatch_target != first_waypoint:
    #         raise ValueError(
    #             f'Unable to get tour of {vehicle}: disagreeing dispatch target: '
    #             f'{first_waypoint} vs {dispatch_target}.'
    #         )
    #
    # # If vehicle is recalled, the last waypoint should be the recall origin
    # if vehicle in self._recalls:
    #     recall_origin = self._recalls[vehicle].origin
    #     if last_waypoint != recall_origin:
    #         raise ValueError(
    #             f'Unable to get tour of {vehicle}: disagreeing recall origin: '
    #             f'{last_waypoint} vs {recall_origin}.'
    #         )
    #
    # return tour
    #
    # def get_tour_geometry(self, vehicle: Hashable) -> list[Hashable]:
    #     geometry = list()
    #
    #     if vehicle in self._dispatches:
    #         dispatch_target = self._dispatches[vehicle].target
    #         geometry.extend(self._problem.get_dispatch_geometry(vehicle, dispatch_target))
    #
    #     tour = self.get_tour(vehicle)
    #     for trip_start, trip_end in zip(tour[:-1], tour[1:]):
    #         geometry.extend(self._problem.get_trip_geometry((trip_start, trip_end)))
    #
    #     if vehicle in self._recalls:
    #         recall_origin = self._recalls[vehicle].origin
    #         geometry.extend(self._problem.get_recall_geometry(vehicle, recall_origin))
    #
    #     return geometry

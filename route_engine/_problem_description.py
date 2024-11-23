from collections.abc import Hashable
from collections.abc import Iterable
from dataclasses import dataclass
from itertools import permutations
from pprint import pformat

from gis_backend.query_provider import get_path_metric
from gis_backend.query_provider import get_shortest_path_between

GISNode = Hashable
Depot = Hashable
Vehicle = Hashable
Waypoint = Hashable
Trip = tuple[Waypoint, Waypoint]


@dataclass
class VehicleParams:
    depot: Depot

    dispatch_from_gis_node: GISNode | None = None
    recall_to_gis_node: GISNode | None = None

    earliest_dispatch_time: float | None = None
    latest_recall_time: float | None = None

    fuel_capacity: float | None = None
    cargo_capacity: float | None = None


@dataclass
class WaypointParams:
    waypoint: Waypoint
    gis_node: GISNode

    cargo_demand: float = 0
    stop_duration: float = 0

    earliest_arrival_time: float | None = None
    latest_arrival_time: float | None = None


@dataclass
class DispatchParams:
    depot: Depot
    target: Waypoint

    cost: float = 0
    duration: float = 0
    fuel_consumed: float = 0

    origin_gis_node: GISNode | None = None
    target_gis_node: GISNode | None = None


@dataclass
class RecallParams:
    depot: Depot
    origin: Waypoint

    cost: float = 0
    duration: float = 0
    fuel_consumed: float = 0

    origin_gis_node: GISNode | None = None
    target_gis_node: GISNode | None = None


@dataclass
class TripParams:
    origin: Waypoint
    target: Waypoint

    cost: float = 0
    duration: float = 0
    fuel_consumed: float = 0

    origin_gis_node: GISNode | None = None
    target_gis_node: GISNode | None = None


class VehicleRoutingProblem:
    def __init__(self):
        self._cost_metric = None

        self._vehicles: dict[Vehicle, VehicleParams] = dict()
        self._waypoints: dict[Waypoint, WaypointParams] = dict()
        self._trips: dict[Trip, TripParams] = dict()
        self._dispatches: dict[tuple[Vehicle, Waypoint], DispatchParams] = dict()
        self._recalls: dict[tuple[Vehicle, Waypoint], RecallParams] = dict()

        self._trip_geometries: dict[Trip, list[GISNode]] = dict()
        self._dispatch_geometries: dict[tuple[Vehicle, Waypoint], list[GISNode]] = dict()
        self._recall_geometries: dict[tuple[Vehicle, Waypoint], list[GISNode]] = dict()

    def __str__(self):
        lines = list()
        lines.append('Vehicle Routing Problem')
        pretty_print_data = {
            'Cost metric': self._cost_metric,
            'Vehicles': self._vehicles,
            'Waypoints': self._waypoints,
            'Trips': self._trips,
            'Dispatches': self._dispatches,
            'Recalls': self._recalls,
        }
        lines.append(pformat(pretty_print_data))
        return '\n'.join(lines)

    def add_vehicle(self, vehicle: Vehicle, params: VehicleParams) -> None:
        if vehicle in self._vehicles:
            raise ValueError(f'Cannot add vehicle: Vehicle "{vehicle}" exists.')
        self._vehicles[vehicle] = params

    def add_waypoint(self, waypoint: Waypoint, params: WaypointParams) -> None:
        if waypoint in self._waypoints:
            raise ValueError(f'Cannot add waypoint: Waypoint "{waypoint}" exists.')
        self._waypoints[waypoint] = params

    def vehicle_params(self, vehicle: Vehicle) -> VehicleParams:
        return self._vehicles[vehicle]

    def waypoint_params(self, waypoint: Waypoint) -> WaypointParams:
        return self._waypoints[waypoint]

    def trip_params(self, trip: Trip) -> TripParams:
        return self._trips[trip]

    def dispatch_params(self, vehicle: Vehicle, waypoint: Waypoint) -> DispatchParams:
        return self._dispatches[vehicle, waypoint]

    def recall_params(self, vehicle: Vehicle, waypoint: Waypoint) -> RecallParams:
        return self._recalls[vehicle, waypoint]

    def dispatch_geometry(self, vehicle: Vehicle, waypoint: Waypoint) -> list[GISNode]:
        return self._dispatch_geometries[vehicle, waypoint]

    def recall_geometry(self, vehicle: Vehicle, waypoint: Waypoint) -> list[GISNode]:
        return self._recall_geometries[vehicle, waypoint]

    def trip_geometry(self, trip: Trip) -> list[GISNode]:
        return self._trip_geometries[trip]

    @property
    def vehicles(self) -> Iterable[Vehicle]:
        return self._vehicles

    @property
    def waypoints(self) -> list[Waypoint]:
        return list(self._waypoints)

    @property
    def trips(self) -> Iterable[Trip]:
        return self._trips

    def trips_to(self, waypoint: Waypoint) -> Iterable[Trip]:
        for trip_from, trip_to in self.trips:
            if trip_to == waypoint:
                yield trip_from, trip_to

    def trips_from(self, waypoint: Waypoint) -> Iterable[Trip]:
        for trip_from, trip_to in self.trips:
            if trip_from == waypoint:
                yield trip_from, trip_to

    def run_trip_planning(self, metric):
        self._cost_metric = metric

        for trip in permutations(self._waypoints, r=2):
            trip_start, trip_end = trip

            path = get_shortest_path_between(
                self._waypoints[trip_start].gis_node,
                self._waypoints[trip_end].gis_node,
                metric=metric
            )

            trip_params = TripParams(
                origin=trip_start,
                target=trip_end,
                cost=get_path_metric(path, metric=metric),
                duration=get_path_metric(path, metric='travel_time'),
                origin_gis_node=self._waypoints[trip_start].gis_node,
                target_gis_node=self._waypoints[trip_end].gis_node,
            )

            self._trips[trip] = trip_params
            self._trip_geometries[trip] = path

        for vehicle, vehicle_params in self._vehicles.items():
            for waypoint, waypoint_params in self._waypoints.items():
                dispatch_path = get_shortest_path_between(
                    vehicle_params.dispatch_from_gis_node,
                    waypoint_params.gis_node,
                    metric=metric
                )

                recall_path = get_shortest_path_between(
                    waypoint_params.gis_node,
                    vehicle_params.recall_to_gis_node,
                    metric=metric
                )

                dispatch_params = DispatchParams(
                    depot=vehicle_params.depot,
                    target=waypoint,
                    cost=get_path_metric(dispatch_path, metric=metric),
                    duration=get_path_metric(dispatch_path, metric='travel_time'),
                    origin_gis_node=vehicle_params.dispatch_from_gis_node,
                    target_gis_node=waypoint_params.gis_node
                )

                recall_params = RecallParams(
                    depot=vehicle_params.depot,
                    origin=waypoint,
                    cost=get_path_metric(recall_path, metric=metric),
                    duration=get_path_metric(recall_path, metric='travel_time'),
                    origin_gis_node=waypoint_params.gis_node,
                    target_gis_node=vehicle_params.recall_to_gis_node,
                )

                self._dispatches[vehicle, waypoint] = dispatch_params
                self._recalls[vehicle, waypoint] = recall_params

                self._dispatch_geometries[vehicle, waypoint] = dispatch_path
                self._recall_geometries[vehicle, waypoint] = recall_path


@dataclass
class TripActivity:
    cargo_level: float
    cargo_to_drop_off: float
    fuel_level_at_origin: float = 0

    params: TripParams | None = None


@dataclass
class DispatchActivity:
    cargo_level: float
    cargo_to_drop_off: float
    fuel_level_at_origin: float = 0

    params: DispatchParams | None = None


@dataclass
class RecallActivity:
    cargo_level: float
    fuel_level_at_origin: float = 0

    params: RecallParams | None = None


class VehicleRoutingProblemSolution:
    def __init__(self, problem: VehicleRoutingProblem):
        self._problem = problem

        self._dispatches: dict[Vehicle, DispatchActivity] = dict()
        self._recalls: dict[Vehicle, RecallActivity] = dict()

        self._trips: dict[Vehicle, dict[Trip, TripActivity]] = {
            vehicle: dict()
            for vehicle in problem.vehicles
        }

    def __str__(self):
        lines = list()
        lines.append('Vehicle Routing Problem Solution')
        pretty_print_data = {
            'Trips': {
                vehicle: self.trip_activities(vehicle)
                for vehicle in self.problem.vehicles
            },
            'Dispatches': {
                vehicle: self.dispatch_activity(vehicle)
                for vehicle in self.problem.vehicles
            },
            'Recalls': {
                vehicle: self.recall_activity(vehicle)
                for vehicle in self.problem.vehicles
            },
        }
        lines.append(pformat(pretty_print_data))
        return '\n'.join(lines)

    @property
    def problem(self) -> VehicleRoutingProblem:
        return self._problem

    def add_dispatch(self, vehicle: Vehicle, waypoint: Waypoint, activity: DispatchActivity):
        if vehicle in self._dispatches:
            raise ValueError(f'Error setting vehicle dispatch: {vehicle} already has dispatch.')
        activity.params = self.problem.dispatch_params(vehicle, waypoint)
        self._dispatches[vehicle] = activity

    def add_recall(self, vehicle: Vehicle, waypoint: Waypoint, activity: RecallActivity):
        if vehicle in self._recalls:
            raise ValueError(f'Error setting vehicle recall: {vehicle} already has recall.')
        activity.params = self.problem.recall_params(vehicle, waypoint)
        self._recalls[vehicle] = activity

    def add_trip(self, vehicle: Vehicle, trip: Trip, activity: TripActivity):
        if trip in self._trips[vehicle]:
            raise ValueError(
                f'Error setting trip: {trip} already has exists for vehicle {vehicle}.')
        activity.params = self.problem.trip_params(trip)
        self._trips[vehicle][trip] = activity

    def dispatch_activity(self, vehicle: Vehicle) -> DispatchActivity | None:
        return self._dispatches.get(vehicle, None)

    def recall_activity(self, vehicle: Vehicle) -> RecallActivity | None:
        return self._recalls.get(vehicle, None)

    def trip_activities(self, vehicle: Vehicle) -> list[TripActivity]:
        """
        Returns trips in sorted order
        :param vehicle: vehicle whose trips are to be returned
        :return: trip activities in sorted order
        """
        if not self._trips[vehicle]:
            return list()

        next_waypoint: dict[Waypoint: Waypoint] = dict()
        for trip_start, trip_end in self._trips[vehicle]:
            next_waypoint[trip_start] = trip_end
            next_waypoint[trip_end] = next_waypoint.get(trip_end, None)

        parentless_waypoints = set(next_waypoint.keys()) - set(next_waypoint.values())
        if len(parentless_waypoints) != 1:
            raise ValueError(
                f'Unable to sort trips: multiple parentless waypoints {parentless_waypoints}.')

        first_waypoint, = parentless_waypoints
        waypoint_order = list()

        waypoint = first_waypoint
        while waypoint is not None:
            waypoint_order.append(waypoint)
            waypoint = next_waypoint[waypoint]

        sorted_trips = [
            self._trips[vehicle][trip]
            for trip in zip(waypoint_order[:-1], waypoint_order[1:])
        ]

        return sorted_trips

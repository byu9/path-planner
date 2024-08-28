from itertools import permutations
from typing import Hashable
from typing import Iterable
from typing import Optional
from typing import Tuple
import gis_backend.map_viewer as plt
import gurobipy as gurobi

from gis_backend.query_provider import get_node_at_address
from gis_backend.query_provider import get_path_metric
from gis_backend.query_provider import get_shortest_path_between


class VehicleRoutingProblem:

    def __init__(self):
        self._waypoints = set()
        self._trips = set()
        self._trip_costs = dict()
        self._trip_geometries = dict()
        self._num_vehicles = None

    def __str__(self):
        return (
            f'Vehicle Routing Problem\nwith\n'
            f' num_vehicles {self.num_vehicles}'
            f' waypoints {self._waypoints}\n'
            f' trips {self._trips}\n'
            f' costs {self._trip_costs}'
        )

    @staticmethod
    def from_addresses(waypoint_addresses: Iterable[str]):
        problem = VehicleRoutingProblem()

        problem._waypoints = [
            get_node_at_address(address)
            for address in waypoint_addresses
        ]

        problem._trips = list(permutations(problem._waypoints, 2))

        problem._trip_geometries = dict()
        for trip_start, trip_end in problem._trips:
            path = get_shortest_path_between(trip_start, trip_end)
            if path is not None:
                problem._trip_geometries[trip_start, trip_end] = path

        problem._trip_costs = {
            trip: get_path_metric(path, metric='length')
            for trip, path in problem._trip_geometries.items()
        }

        return problem

    @property
    def waypoints(self) -> Iterable[Hashable]:
        """
        Returns a list of waypoints.
        :return: Waypoints in the form of an iterable.
        """
        return self._waypoints

    @property
    def trips(self) -> Iterable[Tuple[Hashable, Hashable]]:
        """
        Returns a list of trips.
        :return: Trips between a pair of waypoints (if they are connected) in the form of an iterable.
        """
        return self._trips

    @property
    def depot(self) -> Hashable:
        """
        Returns (the name of) the depot.
        :return: The depot, usually a string.
        """
        return 'depot'

    @property
    def num_vehicles(self) -> Optional[int]:
        """
        Returns the number of vehicles in the depot.
        :return: The number of vehicles in the depot, if it is finite. Otherwise, None.
        """
        return self._num_vehicles

    @num_vehicles.setter
    def num_vehicles(self, value):
        self._num_vehicles = value

    def trip_cost(self, trip: Tuple[Hashable, Hashable]) -> float:
        """
        Returns the cost of a trip.
        :param trip: A pair of connected waypoints in the form of a tuple
        :return: The cost of the trip in the form of a real number
        """
        return self._trip_costs[trip]

    @property
    def num_waypoints(self):
        return len(list(self.waypoints))

    @property
    def is_unlimited_number_of_vehicles_kind(self):
        return self.num_vehicles is None

    def plot_solution(self, solution):
        for tour in solution.tours:
            waypoints = tour[1:]
            trip_start = waypoints[:-1]
            trip_end = waypoints[1:]

            trip_paths = [
                self._trip_geometries[trip]
                for trip in zip(trip_start, trip_end)
            ]

            fig = plt.figure()
            for path in trip_paths:
                fig.plot_path(path)

            for node in self.waypoints:
                fig.plot_node(node)

        plt.show()


class _VehicleRoutingProblemSolution:
    def __init__(self):
        self._parents = dict()
        self._leaves = set()

    def __str__(self):
        return (
            f'Vehicle Routing Problem Solution'
            f'with tours\n{self.tours}'
        )

    @property
    def leaves(self):
        return self._leaves

    @property
    def nodes(self):
        return self._parents.keys()

    @property
    def tours(self):
        return [self.path_to(leaf) for leaf in self.leaves]

    def add_node(self, node):
        assert node not in self.nodes
        self._parents[node] = None
        self._leaves.add(node)

    def add_edge(self, node, parent=None):
        assert node in self.nodes
        assert parent in self.nodes

        self._parents[node] = parent

        if parent in self._leaves:
            self._leaves.remove(parent)

    def parent_of(self, node):
        return self._parents[node]

    def path_to(self, node):
        path = list()

        while node is not None:
            path.append(node)
            node = self.parent_of(node)

        path.reverse()
        return path


class MixedIntegerSolver:

    def solve(self, problem: VehicleRoutingProblem):
        model = gurobi.Model()

        # Binary decision variables
        # A value of 1 indicates the trip between two waypoints is included in the tour of a vehicle
        # We also define this variable for edges between the depot and waypoints
        x = {
            trip: model.addVar(vtype=gurobi.GRB.BINARY)
            for trip in problem.trips
        }
        for w in problem.waypoints:
            x[problem.depot, w] = model.addVar(vtype=gurobi.GRB.BINARY)
            x[w, problem.depot] = model.addVar(vtype=gurobi.GRB.BINARY)

        # Continuous decision variables
        # This quantity is used to eliminate isolated tours using the Miller-Tucker-Zemlin formulation.
        # The accumulated demand for waypoints up to and including w
        u = {
            w: model.addVar(lb=1, ub=problem.num_waypoints, vtype=gurobi.GRB.CONTINUOUS)
            for w in problem.waypoints
        }

        # Miller-Tucker-Zemlin constraints
        model.addConstrs(
            u[j] - u[i] >= 1 - problem.num_waypoints * (1 - x[i, j])
            for i, j in problem.trips
        )

        # There should be exactly one vehicle that enters any waypoint (from the depot or from other waypoints)
        model.addConstrs(
            1 == x[problem.depot, w] + sum(x[j, w] for j in problem.waypoints if (j, w) in problem.trips)
            for w in problem.waypoints
        )

        # The number of vehicles entering any waypoint must equal the number of vehicles exiting it
        model.addConstrs(
            x[problem.depot, w] + sum(x[j, w] for j in problem.waypoints if (j, w) in problem.trips) ==
            x[w, problem.depot] + sum(x[w, j] for j in problem.waypoints if (w, j) in problem.trips)
            for w in problem.waypoints
        )

        # The number of vehicles departing from the depot must equal the number of vehicles returning to the depot
        model.addConstr(
            sum(x[problem.depot, j] for j in problem.waypoints) ==
            sum(x[j, problem.depot] for j in problem.waypoints)
        )

        if not problem.is_unlimited_number_of_vehicles_kind:
            self._ensure_valid_number_of_vehicles(problem)

            # The total number of vehicles departing from the depot is at most the number of vehicles in the depot.
            model.addConstr(sum(x[problem.depot, w] for w in problem.waypoints) <= problem.num_vehicles)

        # Minimize the total cost of completing all tours
        model.setObjective(
            sum(x[trip] * problem.trip_cost(trip) for trip in problem.trips),
            sense=gurobi.GRB.MINIMIZE
        )

        model.optimize()

        if model.Status != gurobi.GRB.OPTIMAL:
            raise RuntimeError(f'Model is infeasible.')

        def is_edge_enabled(edge_start, edge_end):
            return x[edge_start, edge_end].X > 0

        solution = _VehicleRoutingProblemSolution()
        solution.add_node(problem.depot)
        for w in problem.waypoints:
            solution.add_node(w)

        for trip_start, trip_end in problem.trips:
            if is_edge_enabled(trip_start, trip_end):
                solution.add_edge(node=trip_end, parent=trip_start)

        for w in problem.waypoints:
            if is_edge_enabled(problem.depot, w):
                solution.add_edge(node=w, parent=problem.depot)

        return solution

    @staticmethod
    def _ensure_valid_number_of_vehicles(problem: VehicleRoutingProblem):
        if not problem.num_vehicles > 0:
            raise ValueError(f'Number of vehicles must be positive. Found {problem.num_vehicles}.')

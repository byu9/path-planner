from abc import ABCMeta
from abc import abstractmethod
from typing import Hashable
from typing import Iterable
from typing import Optional
from typing import Tuple

import gurobipy as gurobi


class VehicleRoutingProblem(metaclass=ABCMeta):

    @property
    @abstractmethod
    def waypoints(self) -> Iterable[Hashable]:
        """
        Returns a list of waypoints.
        :return: Waypoints in the form of an iterable.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def trips(self) -> Iterable[Tuple[Hashable, Hashable]]:
        """
        Returns a list of trips.
        :return: Trips between a pair of waypoints (if they are connected) in the form of an iterable.
        """
        raise NotImplementedError

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
        return None

    @abstractmethod
    def trip_cost(self, trip: Tuple[Hashable, Hashable]) -> float:
        """
        Returns the cost of a trip.
        :param trip: A pair of connected waypoints in the form of a tuple
        :return: The cost of the trip in the form of a real number
        """
        raise NotImplementedError

    @property
    def num_waypoints(self):
        return len(list(self.waypoints))

    @property
    def is_unlimited_number_of_vehicles_kind(self):
        return self.num_vehicles is None


class _VehicleRoutingProblemSolution:
    def __init__(self):
        self._parents = dict()
        self._leaves = set()

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

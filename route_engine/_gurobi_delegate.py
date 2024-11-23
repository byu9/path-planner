from typing import Optional

import gurobipy as gurobi

from . import VehicleRoutingProblemSolution
from ._problem_description import DispatchActivity
from ._problem_description import RecallActivity
from ._problem_description import TripActivity
from ._problem_description import VehicleRoutingProblem


def _is_gurobi_binary_variable_set(gurobi_var):
    return gurobi_var.X > 0.5


def _get_gurobi_variable_value(gurobi_var):
    return gurobi_var.X


class GurobiTourPlanner:
    def __init__(self, gurobi_params: Optional[dict] = None,
                 infeasible_filename: str = 'infeasible.ilp'):
        if gurobi_params is None:
            gurobi_params = dict()

        self._gurobi_params = gurobi_params
        self._infeasible_filename = infeasible_filename

    def solve(self, problem: VehicleRoutingProblem):
        num_waypoints = len(problem.waypoints)
        model = gurobi.Model()

        # Set gurobi parameters on the model
        for param, val in self._gurobi_params.items():
            model.setParam(param, val)

        # Binary decision variables
        # A value of 1 indicates the trip between two waypoints is included in the tour of a vehicle
        x = {
            v: {ij: model.addVar(vtype=gurobi.GRB.BINARY, name=f'x_{ij}') for ij in problem.trips}
            for v in problem.vehicles
        }

        # Binary decision variables
        # A value of 1 indicates the vehicle is dispatched to the waypoint at the beginning of its tour.
        x_dispatch = {
            v: {j: model.addVar(vtype=gurobi.GRB.BINARY, name=f'x_{v, j}') for j in
                problem.waypoints}
            for v in problem.vehicles
        }

        # Binary decision variables
        # A value of 1 indicates the vehicle is recalled from the waypoint at the end of its tour.
        x_recall = {
            v: {j: model.addVar(vtype=gurobi.GRB.BINARY, name=f'x_{j, v}') for j in
                problem.waypoints}
            for v in problem.vehicles
        }

        # Flow control constraint
        # A vehicle that enters a waypoint must exit it.
        # For any vehicle, the total number of enabled edges terminating at any waypoint must be
        # equal to the number of enabled edges originating from it.
        model.addConstrs((
            x_dispatch[v][j] + gurobi.quicksum(x[v][ij] for ij in problem.trips_to(j)) ==
            x_recall[v][j] + gurobi.quicksum(x[v][ji] for ji in problem.trips_from(j))
            for v in problem.vehicles
            for j in problem.waypoints
        ), name='3.2-1')

        # Flow control constraint
        # A waypoint must be visited once.
        # The total number of enabled edges of vehicles terminating at a waypoint must sum to one.
        model.addConstrs((
            gurobi.quicksum(
                x_dispatch[v][j] + gurobi.quicksum(x[v][ij] for ij in problem.trips_to(j))
                for v in problem.vehicles
            ) == 1
            for j in problem.waypoints
        ), name='3.2-2')

        # Flow control constraint
        # A vehicle can be dispatched to and recalled from at most one waypoint.
        model.addConstrs((
            gurobi.quicksum(x_dispatch[v][j] for j in problem.waypoints) <= 1
            for v in problem.vehicles
        ), name='3.2-3a')
        model.addConstrs((
            gurobi.quicksum(x_recall[v][j] for j in problem.waypoints) <= 1
            for v in problem.vehicles
        ), name='3.2-3b')

        # Sub-tour elimination decision variable
        # Accumulated Miller-Tucker-Zemlin demand
        subtour_u = {
            v: {
                j: model.addVar(vtype=gurobi.GRB.CONTINUOUS, lb=1, ub=num_waypoints,
                                name=f'subtour_u_{v, j}')
                for j in problem.waypoints
            }
            for v in problem.vehicles
        }

        # Sub-tour elimination constraint
        # Miller-Tucker-Zemlin formulation
        model.addConstrs((
            subtour_u[v][j] - subtour_u[v][i] >= 1 - num_waypoints * (1 - x[v][i, j])
            for v in problem.vehicles
            for i, j in problem.trips
        ), name='3.3-1')

        def _get_cargo_capacity(_vehicle):
            capacity = problem.vehicle_params(_vehicle).cargo_capacity
            return capacity if capacity is not None else gurobi.GRB.INFINITY

        def _get_cargo_demand(_waypoint):
            demand = problem.waypoint_params(_waypoint).cargo_demand
            return demand

        # Non-negative continuous decision variables
        # The amount of cargo on a vehicle upto and including waypoint
        capacity_u = {
            v: {
                j: model.addVar(lb=0, ub=_get_cargo_capacity(v), name=f'capacity_u{v, j}')
                for j in problem.waypoints
            }
            for v in problem.vehicles
        }

        # Cargo capacity constraints
        # M-value is set to the sum of the absolute value of demands.
        capacity_m = sum(abs(_get_cargo_demand(j)) for j in problem.waypoints)

        # Cargo capacity constraints
        # Conditional equality using Big-M formulation
        model.addConstrs((
            capacity_u[v][i] - capacity_u[v][j] <= _get_cargo_demand(i) + capacity_m * (
                        1 - x[v][i, j])
            for v in problem.vehicles
            for i, j in problem.trips
        ), name='3.3-1a')
        model.addConstrs((
            capacity_u[v][i] - capacity_u[v][j] >= _get_cargo_demand(i) - capacity_m * (
                        1 - x[v][i, j])
            for v in problem.vehicles
            for i, j in problem.trips
        ), name='3.3-1b')

        # Objective
        # The objective is to minimize the cost of tours, dispatching, and returning all vehicles to all depots.
        model.setObjective(
            gurobi.quicksum(
                problem.trip_params(ij).cost * x[v][ij]
                for v in problem.vehicles
                for ij in problem.trips
            ) +
            gurobi.quicksum(
                problem.dispatch_params(v, j).cost * x_dispatch[v][j]
                for v in problem.vehicles
                for j in problem.waypoints
            ) +
            gurobi.quicksum(
                problem.recall_params(v, j).cost * x_recall[v][j]
                for v in problem.vehicles
                for j in problem.waypoints
            ) +

            # Keep initial cargo as low as possible
            gurobi.quicksum(
                capacity_u[v][j]
                for v in problem.vehicles
                for j in problem.waypoints
            )
        )

        model.optimize()
        if model.Status != gurobi.GRB.OPTIMAL:
            model.computeIIS()
            model.write(self._infeasible_filename)
            raise RuntimeError(f'Model is infeasible.')

        solution = VehicleRoutingProblemSolution(problem=problem)

        # Scan for enabled trips
        for vehicle in problem.vehicles:
            for trip_start, trip_end in problem.trips:
                if _is_gurobi_binary_variable_set(x[vehicle][trip_start, trip_end]):
                    activity = TripActivity(
                        cargo_level=_get_gurobi_variable_value(capacity_u[vehicle][trip_end]),
                        cargo_to_drop_off=_get_cargo_demand(trip_end),
                    )
                    solution.add_trip(vehicle, (trip_start, trip_end), activity)

        # Scan for enabled dispatching edges
        for vehicle in problem.vehicles:
            for waypoint in problem.waypoints:
                if _is_gurobi_binary_variable_set(x_dispatch[vehicle][waypoint]):
                    activity = DispatchActivity(
                        cargo_level=_get_gurobi_variable_value(capacity_u[vehicle][waypoint]),
                        cargo_to_drop_off=_get_cargo_demand(waypoint),
                    )
                    solution.add_dispatch(vehicle, waypoint, activity)

        # Scan for enabled recall edges
        for vehicle in problem.vehicles:
            for waypoint in problem.waypoints:
                if _is_gurobi_binary_variable_set(x_recall[vehicle][waypoint]):
                    activity = RecallActivity(
                        cargo_level=(
                                _get_gurobi_variable_value(capacity_u[vehicle][waypoint]) -
                                _get_cargo_demand(waypoint)
                        )
                    )
                    solution.add_recall(vehicle, waypoint, activity)

        return solution

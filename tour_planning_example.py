from route_engine.tour_planning import MixedIntegerSolver
from route_engine.tour_planning import VehicleRoutingProblem

_distances = {
    ('Waypoint 1', 'Waypoint 2'): 25,
    ('Waypoint 1', 'Waypoint 3'): 43,
    ('Waypoint 1', 'Waypoint 4'): 57,
    ('Waypoint 1', 'Waypoint 5'): 43,
    ('Waypoint 1', 'Waypoint 6'): 61,
    ('Waypoint 1', 'Waypoint 7'): 29,
    ('Waypoint 1', 'Waypoint 8'): 41,
    ('Waypoint 1', 'Waypoint 9'): 48,
    ('Waypoint 1', 'Waypoint 10'): 71,

    ('Waypoint 2', 'Waypoint 3'): 29,
    ('Waypoint 2', 'Waypoint 4'): 34,
    ('Waypoint 2', 'Waypoint 5'): 43,
    ('Waypoint 2', 'Waypoint 6'): 68,
    ('Waypoint 2', 'Waypoint 7'): 49,
    ('Waypoint 2', 'Waypoint 8'): 66,
    ('Waypoint 2', 'Waypoint 9'): 72,
    ('Waypoint 2', 'Waypoint 10'): 91,

    ('Waypoint 3', 'Waypoint 4'): 52,
    ('Waypoint 3', 'Waypoint 5'): 72,
    ('Waypoint 3', 'Waypoint 6'): 96,
    ('Waypoint 3', 'Waypoint 7'): 72,
    ('Waypoint 3', 'Waypoint 8'): 81,
    ('Waypoint 3', 'Waypoint 9'): 89,
    ('Waypoint 3', 'Waypoint 10'): 114,

    ('Waypoint 4', 'Waypoint 5'): 45,
    ('Waypoint 4', 'Waypoint 6'): 71,
    ('Waypoint 4', 'Waypoint 7'): 71,
    ('Waypoint 4', 'Waypoint 8'): 95,
    ('Waypoint 4', 'Waypoint 9'): 99,
    ('Waypoint 4', 'Waypoint 10'): 108,

    ('Waypoint 5', 'Waypoint 6'): 27,
    ('Waypoint 5', 'Waypoint 7'): 36,
    ('Waypoint 5', 'Waypoint 8'): 65,
    ('Waypoint 5', 'Waypoint 9'): 65,
    ('Waypoint 5', 'Waypoint 10'): 65,

    ('Waypoint 6', 'Waypoint 7'): 40,
    ('Waypoint 6', 'Waypoint 8'): 66,
    ('Waypoint 6', 'Waypoint 9'): 62,
    ('Waypoint 6', 'Waypoint 10'): 46,

    ('Waypoint 7', 'Waypoint 8'): 31,
    ('Waypoint 7', 'Waypoint 9'): 31,
    ('Waypoint 7', 'Waypoint 10'): 43,

    ('Waypoint 8', 'Waypoint 9'): 11,
    ('Waypoint 8', 'Waypoint 10'): 46,

    ('Waypoint 9', 'Waypoint 10'): 36
}



class ExampleProblem(VehicleRoutingProblem):
    def __init__(self):
        self._distances = _distances
        for (u, v), distance in self._distances.copy().items():
            self._distances[v, u] = distance

        self._waypoints = set()
        for u, v in _distances.keys():
            self._waypoints.add(u)
            self._waypoints.add(v)

    @property
    def waypoints(self):
        return self._waypoints

    @property
    def trips(self):
        return self._distances.keys()

    @property
    def num_vehicles(self):
        return 1

    def trip_cost(self, trip):
        return self._distances[trip]


problem = ExampleProblem()

solver = MixedIntegerSolver()
solution = solver.solve(problem)
print(solution.tours)

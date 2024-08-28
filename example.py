from route_engine.tour_planning import MixedIntegerSolver
from route_engine.tour_planning import VehicleRoutingProblem

waypoint_addresses = [
    '715 Nazareth St, Raleigh, NC 27606',
    '1240 Farmers Market Dr, Raleigh, NC 27606',
    '500 S Salisbury St, Raleigh, NC 27601',
    '2500 Glenwood Ave, Raleigh NC 27608',
    '1315 Oakwood Ave, Raleigh, NC 27610',
    '15 E Peace St, Raleigh, NC 27604'
]

problem = VehicleRoutingProblem.from_addresses(waypoint_addresses)
problem.num_vehicles = 1

solver = MixedIntegerSolver()
solution = solver.solve(problem)

print(problem)
print(solution)

problem.plot_solution(solution)

# from gis_backend._pickling import save_object
# from route_engine import JSONStorageProvider
#
# json_provider = JSONStorageProvider()
# problem = json_provider.load_problem(folder='test_problem')
# problem.compute_costs(metric='travel_time')
#
# save_object(problem, 'problem.pickle')

from route_engine import GurobiTourPlanner
from gis_backend._pickling import load_object
from route_engine import RoutePlotter

problem = load_object('problem.pickle')

gurobi_solver = GurobiTourPlanner(gurobi_params={
    'LogToConsole': 1,
    'MIPFocus': 2,  # Focus on optimality
    'TimeLimit': 600
})
solution = gurobi_solver.solve(problem)

with open('test_solution/debug_problem.txt', 'w') as file:
    print(problem, file=file)

with open('test_solution/debug_solution.txt', 'w') as file:
    print(solution, file=file)

plotter = RoutePlotter()
plotter.plot_solution_to_file(solution, filename='test_solution/plot_solution.html')

plotter = RoutePlotter()
# plotter.plot_solution_to_file(solution, filename='test_solution/plot_solution.html')

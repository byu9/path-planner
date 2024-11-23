import pickle
from pathlib import Path

from route_engine import GurobiTourPlanner
from route_engine import JSONStorageProvider
from route_engine import plot_solution_to_file

cached_problem_filename = Path('test_solution/cached_problem.pickle')

if cached_problem_filename.exists():
    with open(cached_problem_filename, 'rb') as file:
        problem = pickle.load(file)

else:
    json_provider = JSONStorageProvider()
    problem = json_provider.load_problem(folder='test_problem')
    problem.run_trip_planning(metric='travel_time')

    with open(cached_problem_filename, 'wb') as file:
        pickle.dump(problem, file=file)

with open('test_solution/debug_problem.txt', 'w') as file:
    print(problem, file=file)

gurobi_solver = GurobiTourPlanner({
    'LogToConsole': 1,
    'MIPFocus': 2,  # Focus on optimality
})
solution = gurobi_solver.solve(problem)

with open('test_solution/debug_solution.txt', 'w') as file:
    print(solution, file=file)

plot_solution_to_file(solution, filename='test_solution/plot_solution.html')

from desdeo_emo.EAs.NSGAIII import NSGAIII
import numpy as np
from desdeo_problem.problem import MOProblem, ScalarObjective, variable_builder

import numpy as np


"""The example problem utilized in
Eskelinen, P., Miettinen, K. Trade-off analysis approach for interactive nonlinear multiobjective optimization. 
OR Spectrum 34, 803–816 (2012). https://doi.org/10.1007/s00291-011-0266-z
"""


def phi(x):
    return fi(x) - np.exp(-50 * fi(x))


def fi(x):
    return x[:, 0] ** 2 + x[:, 1] ** 2


def f_1(x):
    return phi(x)


def f_2(x):
    aux = np.copy(x)
    aux[:, 1] = aux[:, 1] - 1
    return phi(aux)


def f_3(x):
    aux = np.copy(x)
    aux[:, 0] = aux[:, 0] - 1
    return phi(aux)


def objective_function(x):
    return np.array([f1(x), f2(x), f3(x)])


list_vars = variable_builder(
    ["x", "y"], initial_values=[0, 0], lower_bounds=[0, 0], upper_bounds=[1, 1]
)

f1 = ScalarObjective(name="f1", evaluator=f_1)
f2 = ScalarObjective(name="f2", evaluator=f_2)
f3 = ScalarObjective(name="f3", evaluator=f_3)
list_objs = [f1, f2, f3]

problem = MOProblem(variables=list_vars, objectives=list_objs)
evolver = NSGAIII(
    problem,
    interact=False,
    n_iterations=1,
    n_gen_per_iter=200,
    population_size=500,
)

evolver.start()
while evolver.continue_evolution():
    evolver.iterate()

individuals, solutions, _ = evolver.end()

np.savetxt("paper_front.csv", solutions, delimiter=",")

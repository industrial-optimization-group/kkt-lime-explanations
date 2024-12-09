from desdeo_problem import Variable
from desdeo_emo.EAs.NSGAIII import NSGAIII
import numpy as np
from desdeo_problem.problem import MOProblem, ScalarObjective, variable_builder


# create the problem
def f_1(x):
    return 4.07 + 2.27 * x[:, 0]

def f_2(x):
    return 2.60 + 0.03*x[:, 0] + 0.02*x[:, 1] + 0.01 / (1.39 - x[:, 0]**2) + 0.30 / (1.39 - x[:, 1]**2)

def f_3(x):
    return 8.21 - 0.71 / (1.09 - x[:, 0]**2)

def f_4(x):
    return 0.96 - 0.96 / (1.09 - x[:, 1]**2)


objective_1 = ScalarObjective(name="the DO level in the city", evaluator=f_1, maximize=[True])
objective_2 = ScalarObjective(name="the DO level at the municipality border", evaluator=f_2, maximize=[True])
objective_3 = ScalarObjective(name="the percent return on investment at the fishery", evaluator=f_3, maximize=[True])
objective_4 = ScalarObjective(name="the addition to the tax rate of city", evaluator=f_4, maximize=[True])

objectives = [objective_1, objective_2, objective_3, objective_4]

var_iv = np.array([0.5, 0.5])

x_1 = Variable("the proportionate amount of BOD removed from water at the fishery", var_iv[0], 0.3, 1.0)
x_2 = Variable("the proportionate amount of BOD removed from water at the city", var_iv[1], 0.3, 1.0)

variables = [x_1, x_2]

problem = MOProblem(variables=variables, objectives=objectives)

evolver = NSGAIII(
    problem,
    interact=False,
    n_iterations=10,
    n_gen_per_iter=200,
    population_size=500,
)

evolver.start()
while evolver.continue_evolution():
    evolver.iterate()

individuals, solutions, _ = evolver.end()

np.savetxt("data.csv", solutions, delimiter=",")

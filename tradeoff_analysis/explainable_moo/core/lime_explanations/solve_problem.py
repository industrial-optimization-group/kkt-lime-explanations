from explainable_moo.problems.problems import river_pollution_problem
from explainable_moo.problems.problems import car_crash_problem
from explainable_moo.core.lime_explanations.kkt_multipliers import compute_multipliers
from explainable_moo.core.lime_explanations.compute_tradeoffs import (
    compute_tradeoffs_objectives,
)
import numpy as np
from explainable_moo.utils.utils import normalize_objectives


def compute_approximate_pareto_optimal_objective_vector(
    dot_z, lambdas, z_value, weights
):
    """
    Compute the approximate Pareto optimal objective vector.

    Args:
    dot_z (numpy.ndarray): Current objective vector.
    lambdas (list): List of Lagrange multipliers.
    z_values (numpy.ndarray): Array containing points in the neighborhood of dot_z.
    weights (list): List of weights for the objectives.

    Returns:
    numpy.ndarray: Array of approximate Pareto optimal objective vectors.
    """
    k = len(dot_z)  # Number of objectives
    w_inv = 1 / np.array(weights)
    n = -np.array([lambdas[i] * weights[i] for i in range(k)])
    d = np.array(z_value) - dot_z  # Direction vector from dot_z to z_value
    w_inv = np.array(w_inv)
    n = np.array(n)

    t = -np.dot(n.T, d) / np.dot(n.T, w_inv)

    print("t", t)

    approximate_z = dot_z + d + t * w_inv

    return approximate_z


def get_MOP(id):
    problem = river_pollution_problem()
    if id == 2:
        problem = river_pollution_problem()
    elif id == 3:
        problem = car_crash_problem()
    elif id == 4:
        problem = river_pollution_problem(True)
    else:
        problem = river_pollution_problem()
    return problem


def solve_MOP(id, z_dot, ideal, nadir):
    problem = get_MOP(id)
    objectives = problem.objectives
    num_objectives = problem.n_of_objectives
    base_weight = 1 / num_objectives
    w = [base_weight] * num_objectives
    problem.get_objective_names()

    x, lagrange_multipliers = compute_multipliers(problem, w, z_dot, ideal, nadir)

    fx = problem.evaluate(np.array(x))

    partial_tradeoffs = compute_tradeoffs_objectives(
        lagrange_multipliers, w, objectives
    )

    # print("obj", fx.objectives[0])

    return lagrange_multipliers, partial_tradeoffs, fx


if __name__ == "__main__":
    solve_MOP(1, [1, 2, 3, 4], [0, 0, 0, 0], [1, 1, 1, 1])

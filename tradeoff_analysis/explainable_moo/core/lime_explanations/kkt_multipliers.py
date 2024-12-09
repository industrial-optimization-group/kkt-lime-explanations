from typing import Union
from gekko import GEKKO
import numpy as np
from explainable_moo.utils.utils import (
    normalize_objectives,
    normalize_reference_point,
    parse_objectives,
)

from desdeo_problem import MOProblem


def normalize(value, min_val, max_val):
    # Normalize values to be between 0 and 1
    normalized_values = (value - min_val) / (max_val - min_val)
    return normalized_values


def get_scalar_value(value: Union[float, np.ndarray]) -> float:
    if isinstance(value, float):
        return value
    elif isinstance(value, np.ndarray):
        if value.size == 1:
            return float(value.item())  # Convert single element ndarray to float
        else:
            raise ValueError(
                "Expected a scalar ndarray, but the array has more than one element."
            )
    else:
        raise TypeError("Expected a float or ndarray, but got something else.")


def compute_multipliers(problem: MOProblem, w, z_dot, ideal, nadir):
    num_variables = problem.n_of_variables
    lower_bounds = problem.get_variable_lower_bounds()
    upper_bounds = problem.get_variable_upper_bounds()
    # Initial guess for alpha and variables
    m = GEKKO(remote=False)

    alpha = m.Var(value=0)  # Variable alpha
    x = m.Array(m.Var, num_variables)

    for i in range(num_variables):
        x[i].lower = lower_bounds[i]
        x[i].upper = upper_bounds[i]

    m.Obj(alpha)  # Objective function to minimize
    num_objectives = problem.n_of_objectives

    # Normalize objectives and z_dot using ideal and nadir points
    # normalized_objectives = normalize_objectives(problem, ideal, nadir)
    normalized_z_dot = normalize_reference_point(z_dot, ideal, nadir)
    parsed_objectives = parse_objectives(problem, ideal, nadir)
    # Define Constraints
    for i in range(num_objectives):
        # print(parsed_objectives[i]([0, 0])[0, 0])
        m.Equation(
            w[i] * (parsed_objectives[i](x)[0, 0] - normalized_z_dot[i]) <= alpha
        )

    m.options.DIAGLEVEL = 2

    # Minimize alpha subject to the constraints
    m.solve(disp=False)
    # print(f"Optimal value of alpha: {alpha.value[0]}")
    # print("Lagrange multipliers")
    lam = np.loadtxt(m.path + "/apm_lam.txt")
    lam *= -1
    # print(lam)
    # print("Value of x")
    flattened_x = [item for sublist in x for item in sublist]
    # print(flattened_x)
    # Calculate Lagrange multipliers
    # lagrange_multipliers = np.array([item for sublist in result.v for item in sublist])
    # lagrange_multipliers[0:num_objectives] *= -1
    # lagrange_multipliers = result.grad[:-1]
    return np.array(flattened_x), lam

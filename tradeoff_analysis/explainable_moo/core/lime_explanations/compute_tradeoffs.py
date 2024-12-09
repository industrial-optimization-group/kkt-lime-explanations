import numpy as np
from scipy.stats import qmc
from scipy.optimize import approx_fprime
from explainable_moo.utils.utils import get_min_max

from scipy import stats


def asf(fx, w, z_dot):
    values = []
    for i in range(len(fx)):
        values.append(w[i] * (fx[i] - z_dot[i]))
    return np.max(values)


def compute_tradeoffs_slope(z_values):

    n_objectives = len(z_values[0])
    partial_trade_offs = np.ones((n_objectives, n_objectives))

    for i in range(n_objectives):
        for j in range(n_objectives):
            if i != j:
                slope, intercept, r_value, p_value, std_err = stats.linregress(
                    z_values[:, i], z_values[:, j]
                )
                partial_trade_offs[i][j] = slope

    return partial_trade_offs


def compute_tradeoffs_objectives(lambdas, w, objectives):
    n_objectives = len(objectives)
    partial_trade_offs = np.ones((n_objectives, n_objectives))
    # trade_off_with_original_values = np.ones((n_objectives, n_objectives))
    # norm_objectives = (np.array(fx) - np.min(fx)) / (np.max(fx) - np.min(fx))
    # normalized_multipliers = (lambdas - np.min(lambdas)) / (np.max(lambdas) - np.min(lambdas))
    # min_value, max_value = get_min_max(ideal, nadir)

    w_inv = 1 / np.array(w)
    w_inv = np.array(w_inv)
    # print (norm_objectives)
    for i in range(n_objectives):
        # lambda_i = lambdas[i] * (max_value[i] - min_value[i]) + min_value[i]
        lambda_i = lambdas[i]
        for j in range(n_objectives):
            if i != j:
                # lambda_j = lambdas[j] * (max_value[j] - min_value[j]) + min_value[j]
                lambda_j = lambdas[j]
                # print(np.array(x))
                # tradeoff = (np.linalg.norm(lambdas[i] * gradient_i)) / (
                #    np.linalg.norm(lambdas[j] * gradient_j)
                # )
                # Gaining one unit in i impairs j in tradeoff units
                tradeoff = -(lambda_j) / (lambda_i)
                partial_trade_offs[i][j] = tradeoff

                # trade_off_with_original_values[i][j] = tradeoff * (fx[j] / fx[i])
                # print(f"Trade-off between x{i+1} and x{j+1}: {trade_off_with_original_values}")
                # print(lambdas)
                # print(tradeoff)
    return partial_trade_offs

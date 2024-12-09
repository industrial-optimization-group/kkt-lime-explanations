import numpy as np
from scipy.stats import qmc
from scipy.linalg import lstsq
from numpy.linalg import matrix_rank
from numpy.linalg import pinv
from scipy import stats

from numpy.linalg import cond, svd


def generate_dominated_neighborhood_points(dot_z, num_points, radius):
    """
    Generate non-dominated points in the neighborhood of dot_z.

    Args:
    dot_z (numpy.ndarray): Current objective vector.
    num_points (int): Number of points to generate.
    radius (float): Radius of the neighborhood.

    Returns:
    numpy.ndarray: Array of points in the neighborhood of dot_z.
    """
    k = len(dot_z)  # Number of objectives
    points = np.random.normal(size=(num_points, k))  # Generate random points
    points = (
        radius * points / np.linalg.norm(points, axis=1)[:, np.newaxis]
    )  # Scale to radius
    points += dot_z  # Translate to dot_z

    # Function to check if a point is dominated by another point
    def is_dominated(point, other_points):
        return any(
            np.all(other_points <= point, axis=1) & np.any(other_points < point, axis=1)
        )

    # Filter non-dominated points
    non_dominated_points = []
    for i in range(len(points)):
        if not is_dominated(points[i], points[:i]) and not is_dominated(
            points[i], points[i + 1 :]
        ):
            non_dominated_points.append(points[i])

    return np.array(non_dominated_points)


def generate_neighborhood_points(dot_z, num_points, radius):
    """
    Generate points in the neighborhood of dot_z.

    Args:
    dot_z (numpy.ndarray): Current objective vector.
    num_points (int): Number of points to generate.
    radius (float): Radius of the neighborhood.

    Returns:
    numpy.ndarray: Array of points in the neighborhood of dot_z.
    """
    k = len(dot_z)  # Number of objectives
    points = np.random.normal(size=(num_points, k))  # Generate random points
    points = (
        radius * points / np.linalg.norm(points, axis=1)[:, np.newaxis]
    )  # Scale to radius
    points += dot_z  # Translate to dot_z
    return points


def generate_neighborhood_lhs_points(dot_z, num_points, radius):
    """
    Generate points in the neighborhood of dot_z using LHS sampling.

    Args:
    dot_z (numpy.ndarray): Current objective vector.
    num_points (int): Number of points to generate.
    radius (float): Radius of the neighborhood.

    Returns:
    numpy.ndarray: Array of points in the neighborhood of dot_z.
    """
    k = len(dot_z)  # Number of objectives

    # Generate LHS samples in the range [-1, 1] for each dimension
    sampler = qmc.LatinHypercube(d=k)
    lhs_points = sampler.random(num_points) * 2 - 1  # Scale to [-1, 1]

    # Normalize the points to ensure they lie within the radius
    norm = np.linalg.norm(lhs_points, axis=1)
    lhs_points = lhs_points / norm[:, np.newaxis]  # Normalize to unit sphere
    lhs_points = lhs_points * radius  # Scale to the given radius

    # Translate points to be centered around dot_z
    points = lhs_points + dot_z

    return points


def generate_neighborhood_scaled_points(dot_z, num_points, radius, min_vals, max_vals):
    """
    Generate points in the neighborhood of dot_z with consideration for max and min values of each dimension.

    Args:
    dot_z (numpy.ndarray): Current objective vector.
    num_points (int): Number of points to generate.
    radius (float): Radius of the neighborhood.
    min_vals (numpy.ndarray): Minimum values for each dimension.
    max_vals (numpy.ndarray): Maximum values for each dimension.

    Returns:
    numpy.ndarray: Array of points in the neighborhood of dot_z.
    """
    k = len(dot_z)  # Number of objectives

    # Generate LHS samples in the range [-1, 1] for each dimension
    sampler = qmc.LatinHypercube(d=k)
    lhs_points = sampler.random(num_points) * 2 - 1  # Scale to [-1, 1]

    # Scale the points to fit within the ranges of each dimension
    for i in range(k):
        range_size = max_vals[i] - min_vals[i]
        lhs_points[:, i] = lhs_points[:, i] * (range_size / 2)

    # Normalize the points to lie within the unit sphere
    norm = np.linalg.norm(lhs_points, axis=1)
    lhs_points = lhs_points / norm[:, np.newaxis]  # Normalize to unit sphere

    # Scale points to lie within the specified radius
    lhs_points = lhs_points * radius  # Scale to the given radius

    # Translate points to be centered around dot_z
    points = lhs_points + dot_z

    return points


def compute_approximate_pareto_optimal_objective_vectors(
    dot_z, lambdas, z_values, weights
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
    d = np.array(z_values) - dot_z  # Direction vectors from dot_z to z_values
    w_inv = np.array(w_inv)
    n = np.array(n)

    # Compute the trade-off vectors for each point z
    t_values = []
    for d_vector in d:
        t = -np.dot(n.T, d_vector) / np.dot(n.T, w_inv)
        t_values.append(t)

    # Compute approximate z for each point z
    approximate_z_values = []
    for i in range(len(z_values)):
        approximate_z = dot_z + d[i] + t_values[i] * w_inv
        approximate_z_values.append(approximate_z)

    approximate_z_values = np.array(approximate_z_values)

    slope, intercept, r_value, p_value, std_err = stats.linregress(
        approximate_z_values[:, 1], approximate_z_values[:, 3]
    )
    slope2, intercept, r_value, p_value, std_err = stats.linregress(
        approximate_z_values[:, 3], approximate_z_values[:, 1]
    )

    print("slope 01", slope)
    print("slope 10", slope2)

    return approximate_z_values


def compute_approximate_pareto_optimal_objective_vector(
    dot_z, lambdas, new_reference_point, weights
):
    """
    Compute the approximate Pareto optimal objective vector.

    Args:
    dot_z (numpy.ndarray): Current objective vector.
    d (numpy.ndarray): Direction vector.
    n (numpy.ndarray): Normal vector.
    w_inv (numpy.ndarray): Inverse of the weight vector.

    Returns:
    numpy.ndarray: Approximate Pareto optimal objective vector.
    """
    k = len(dot_z)  # Number of objectives
    w_inv = 1 / np.array(weights)
    n = -np.array([lambdas[i] * weights[i] for i in range(k)])
    local_trade_off = -(lambdas[1] * weights[1]) / (lambdas[0] * weights[0])
    print("Local trade off", local_trade_off)
    # d = np.zeros(len(new_reference_point))
    d = np.array(new_reference_point) - np.array(dot_z)

    for i in range(0, len(new_reference_point)):
        if new_reference_point[i] > dot_z[i]:
            print("improve objective ", i)

        elif new_reference_point[i] < dot_z[i]:
            print("impair", i)

        else:
            print("keep the same", i)

    print("dot_z", dot_z)
    print("potential", new_reference_point)
    print("new ref_point", np.array(dot_z) + d)

    d = np.array(d)
    n = np.array(n)
    w_inv = np.array(w_inv)
    t = -np.dot(n.T, d) / np.dot(n.T, w_inv)
    approximate_z = dot_z + d + t * w_inv
    print("d", d)
    print("Approximated z", approximate_z)
    return approximate_z


# Function to compute slope using SVD
def compute_slope_svd(difference_matrix):
    # Check the rank of the difference matrix
    rank = matrix_rank(difference_matrix)
    print(f"Rank of the Difference Matrix: {rank}")

    # Perform SVD
    U, s, Vt = svd(difference_matrix, full_matrices=False)

    # Tolerance to determine numerical stability
    tolerance = 1e-10
    s_inv = np.array([1 / si if si > tolerance else 0 for si in s])

    # Create the diagonal matrix for singular values
    S_inv = np.diag(s_inv)

    # Compute the pseudo-inverse
    A_pseudo_inv = Vt.T @ S_inv @ U.T

    # Solve for slope (assuming b = 0)
    b = np.zeros(difference_matrix.shape[0])
    slope = A_pseudo_inv @ b

    # Check for rank deficiency
    tolerance = 1e-10
    effective_rank = np.sum(s > tolerance)
    print(f"Effective Rank (considering tolerance): {effective_rank}")

    if effective_rank < difference_matrix.shape[1]:
        print("The difference matrix is rank deficient.")
    else:
        print("The difference matrix is not rank deficient.")

    return slope


# Compute difference matrix
def compute_difference_matrix(solutions):
    num_solutions = solutions.shape[0]
    diff_matrix = np.zeros((num_solutions - 1, solutions.shape[1]))

    for i in range(num_solutions - 1):
        diff_matrix[i] = (
            solutions[i + 1] - solutions[0]
        )  # Difference from the first solution

    return diff_matrix


def construct_tangent_hyperplane(target_solution, neighbors):

    # Compute difference matrix A (each row is the difference between a neighbor and the target)
    A = compute_difference_matrix(neighbors)

    slope = compute_slope_svd(A)
    print("Slope svd", slope)
    return slope

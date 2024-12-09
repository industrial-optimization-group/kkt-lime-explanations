from desdeo_tools.scalarization import StomASF
from flask import Flask, request, jsonify
from explainable_moo.problems import problems
from explainable_moo.core.lime_explanations.kkt_multipliers import compute_multipliers
from explainable_moo.core.lime_explanations.compute_tradeoffs import (
    compute_tradeoffs_objectives,
)
from explainable_moo.core.lime_explanations.approximate_solutions import (
    compute_approximate_pareto_optimal_objective_vector,
)
from flask_cors import CORS

import numpy as np

app = Flask(__name__, static_url_path="", static_folder="data")
CORS(app)  # This will enable CORS for all routes

decimal_places = 5
# Global values
optimization_problems = {
    1: {
        "name": "RPP",
        "definition": problems.river_pollution_problem(),
        "ideal": np.array([-6.34, -3.44487179, -7.5, 0.0]),
        "nadir": np.array([-4.751, -2.85346154, -0.32111111, 9.70666667]),
        "multipliers": np.array([-1, -1, -1, -1]),
        "shortnames": np.array(["f_1", "f_2", "f_3", "f_4"]),
    },
    2: {
        "name": "CCW",
        "definition": problems.car_crash_problem(),
        "ideal": [0, 0, 0, 0],
        "nadir": [1, 1, 1, 1],
        "multipliers": [-1, -1, -1, -1],
        "shortnames": np.array(["f_1", "f_2", "f_3", "f_4"]),
    },
    3: {
        "name": "RPP",
        "definition": problems.discrete_river_pollution(),
        "multipliers": np.array([-1, -1, -1, -1, -1]),
        "explainer": None,
        "missing_data": [],
        "bb": [],
    },
}


@app.route("/get_details_problem", methods=["POST"])
def get_details_problem():
    problem_id = 1
    problem = optimization_problems[problem_id]["definition"]
    multipiers = np.array(optimization_problems[problem_id]["multipliers"])
    ideal = np.array(optimization_problems[problem_id]["ideal"]) * multipiers
    nadir = np.array(optimization_problems[problem_id]["nadir"]) * multipiers
    shortnames = np.array(optimization_problems[problem_id]["shortnames"])

    return jsonify(
        {
            "ideal": ideal.tolist(),
            "nadir": nadir.tolist(),
            "num_objectives": problem.n_of_objectives,
            "objective_names": problem.get_objective_names(),
            "short_names": shortnames.tolist(),
            "decimal_places": decimal_places,
        }
    )


@app.route("/get_solution", methods=["POST"])
def get_solution():
    data = request.get_json()
    problem_id = 1
    reference_point = data.get("reference_point")

    problem = optimization_problems[problem_id]["definition"]
    ideal = optimization_problems[problem_id]["ideal"]
    nadir = optimization_problems[problem_id]["nadir"]
    multipliers = optimization_problems[problem_id]["multipliers"]
    objectives = problem.objectives
    num_objectives = problem.n_of_objectives
    base_weight = 1 / num_objectives
    w = [base_weight] * num_objectives
    # uncomment this when switching to maximizatiom
    # new_reference_point = -1 * np.array(reference_point)
    new_reference_point = np.array(reference_point) * multipliers
    x, lagrange_multipliers = compute_multipliers(
        problem, w, new_reference_point, ideal, nadir
    )

    fx = problem.evaluate(np.array(x))
    fx = fx.objectives[0] * multipliers
    # z_values = generate_neighborhood_scaled_points(fx, 50,5,default_problem.get_nadir(), default_problem.get_ideal())
    # approx_solutions = compute_approximate_pareto_optimal_objective_vectors(fx, lagrange_multipliers,z_values,w)

    # partial_tradeoffs = compute_tradeoffs_slope(approx_solutions)

    print("reference point", reference_point)
    print("computed fx", fx)
    partial_tradeoffs = compute_tradeoffs_objectives(
        lagrange_multipliers, w, objectives
    )

    return jsonify(
        {
            "lagrange_multipliers": lagrange_multipliers.tolist(),
            "partial_tradeoffs": partial_tradeoffs.tolist(),
            "fx": fx.tolist(),
        }
    )


@app.route("/get_kkt_multipliers", methods=["POST"])
def get_kkt_multipliers():
    data = request.get_json()
    problem_id = data.get("problem_id")
    reference_point = data.get("reference_point")
    weights = data.get("weights")
    # Dummy KKT multipliers calculation
    kkt_multipliers = [rp * w for rp, w in zip(reference_point, weights)]
    return jsonify(kkt_multipliers)


@app.route("/approximate_solution", methods=["POST"])
def compute_point():
    data = request.get_json()
    reference_point = data.get("reference_point")
    new_reference_point = data.get("new_reference_point")
    lagrange_multipliers = data.get("multipliers")
    num_objectives = data.get("num_objectives")
    base_weight = 1 / num_objectives
    w = [base_weight] * num_objectives

    computed_point = compute_approximate_pareto_optimal_objective_vector(
        reference_point, lagrange_multipliers, new_reference_point, w
    )
    return jsonify(
        {
            "approximated_solution": computed_point.tolist(),
        }
    )


if __name__ == "__main__":
    app.run(debug=True)

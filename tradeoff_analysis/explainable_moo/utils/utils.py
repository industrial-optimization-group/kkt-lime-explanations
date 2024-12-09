import numpy as np
from desdeo_problem import MOProblem, ScalarObjective


def get_min_max(ideal, nadir):
    num_objectives = len(ideal)
    min_value = np.zeros(num_objectives)
    max_value = np.zeros(num_objectives)

    for i in range(num_objectives):
        if ideal[i] >= nadir[i]:
            min_value[i] = nadir[i]
            max_value[i] = ideal[i]
        else:
            min_value[i] = ideal[i]
            max_value[i] = nadir[i]

    return min_value, max_value


def normalize_front(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))


def normalize_reference_point(rp, ideal, nadir):
    min_value, max_value = get_min_max(ideal, nadir)
    return (rp - min_value) / (max_value - min_value)


def normalize_objectives(problem: MOProblem, ideal, nadir):
    objectives = problem.objectives
    num_objectives = problem.n_of_objectives

    min_value, max_value = get_min_max(ideal, nadir)
    normalized_objectives = []
    for i in range(num_objectives):

        def normalized_obj(
            x, obj=objectives[i], ideal=min_value[i], nadir=max_value[i]
        ):
            return (obj.evaluate(x) - ideal) / (nadir - ideal)

        normalized_objectives.append(normalized_obj)

    return normalized_objectives


def parse_objectives(problem: MOProblem, ideal, nadir):
    objectives = problem.objectives
    num_objectives = problem.n_of_objectives
    min_value, max_value = get_min_max(ideal, nadir)
    parsed_objectives = []
    for i in range(num_objectives):

        def parsed_obj(
            x, obj=objectives[i]._func_evaluate, ideal=min_value[i], nadir=max_value[i]
        ):
            return (obj(x) - ideal) / (nadir - ideal)

        parsed_objectives.append(parsed_obj)

    return parsed_objectives

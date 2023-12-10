""" Here come methods that use mopeds as import.
Separated from utilities to avoid dependency hell"""
from __future__ import annotations

import copy

import numpy as np

from mopeds import Model, Simulator, SimulatorNLE, VariableList, VariableParameter, VariableControl


def create_grid(bounds: list[list[float]]) -> list[list[float]]:
    """Create a grid in a given bounds. Bounds is dictionary, with variable names as keys(),
    and values() as a list with 3 elements: [lower_bound, upper_bound, num_points]
    """
    linspace_list = []
    for bound in bounds:
        linspace_list.append(np.linspace(start=bound[0], stop=bound[1], num=bound[2]))
    meshgrid = np.meshgrid(*linspace_list)

    grid = [n_grid.ravel() for n_grid in meshgrid]
    grid = np.array(grid).transpose().tolist()
    return grid, meshgrid


def generate_varlist_with_data(
    variable_list: VariableList,
    model: Model,
    time_grid: np.ndarray,
    algebraic: bool = False,
    perturbate: bool = False,
    rng: np.random.Generator | None = None
) -> VariableList:
    if rng is None:
        rng = np.random.default_rng()
    # Simulated ODE/DAE and replaces StateVariable values with simulated data
    var_list_fixed = copy.deepcopy(variable_list)
    for var in var_list_fixed.values():
        var.fixed = True
    sim = Simulator(model, time_grid, var_list_fixed)
    var_list_exp = sim.generate_exp_data(algebraic)

    # Replace empty state variables with results from simulation
    variable_list_with_data = copy.deepcopy(variable_list)
    for key, var in var_list_exp.items():
        if not isinstance(var, VariableControl):
            df = var.dataframe
            if perturbate:
                std = var_list_fixed[key].variance ** 0.5
                value = rng.normal(var.dataframe, std)
                df[key] = value

            variable_list_with_data[key].dataframe = df

    return variable_list_with_data


def generate_varlist_with_data_NLE(
    model,
    variable_list,
    control_bounds,
    perturbate: bool = True,
    rng: np.random.Generator = None,
    measurement_names: list[str] = None,
) -> tuple[list[VariableList], dict[str, float]]:
    """Generate artificial data that can immediately be used by Parameter Estimator.
    Returns list of varlists and a dictionary with parameter values that were used
    to generate data.

    Parameter values that are used are taken from variable list.
    control_bounds is dictionary, with variable names as keys(),
    and values() as a list with 3 elements: [lower_bound, upper_bound, num_points]
    perturbate: if True, generated data is perturbated based on variance in variable_list
    rng: is a rng object, user can use it to predefine the randomization of the noise
    measurement_names: list with variable names, for which artificial data should be generated
    """
    if rng is None:
        rng = np.random.default_rng()

    if measurement_names is None:
        measurement_names = model.varlist_algebraic.keys()

    variable_list_original = copy.deepcopy(variable_list)
    true_parameters = {}

    for var in variable_list.values():
        var.fixed = True

    for var in model.varlist_independent.values():
        if isinstance(var, VariableParameter):
            var_varlist = variable_list_original[var.name]
            true_parameters[var_varlist.name] = var_varlist.value[0]

    grid, meshgrid = create_grid(list(control_bounds.values()))
    sim_fixed = SimulatorNLE(model, variable_list)

    varlist_list = []
    for grid_point in grid:
        variable_list_optimizer = copy.deepcopy(variable_list_original)
        sim_fixed.change_independent_variables(
            dict(zip(control_bounds.keys(), grid_point))
        )
        varlist_results = sim_fixed.generate_exp_data()

        # Set startings values
        for variable_name, variable in varlist_results.items():
            if variable_name in measurement_names:
                value = variable.value[0]
                if perturbate:
                    value = rng.normal(value, np.sqrt(variable.variance))
                variable_list_optimizer[variable_name].guess = value
                variable_list_optimizer[variable_name].value = value
        for index, var_name in enumerate(control_bounds.keys()):
            variable_list_optimizer[var_name].value = grid_point[index]
        varlist_list.append(variable_list_optimizer)

    return varlist_list, true_parameters

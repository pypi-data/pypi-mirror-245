from __future__ import annotations

from collections.abc import Callable

import casadi as ca
import numpy as np

from mopeds import (
    Model,
    Optimizer,
    Simulator,
    VariableAlgebraic,
    VariableControl,
    VariableControlPiecewiseConstant,
    VariableList,
    VariableParameter,
    VariableState,
)


class ModelPredictiveControl(Optimizer):
    def __init__(
        self,
        model: Model,
        variable_list: list[VariableList],
        number_of_time_horizonts: int,
        simulator_name="idas",
        simulator_settings=None,
        *,
        reinitialize_algebraic=False,
        use_idas_constraints=False,
        use_algebraic_vars=False,
    ):
        raise NotImplementedError
        super().__init__(
            model,
            variable_list,
            simulator_name,
            simulator_settings,
        )

        if use_algebraic_vars:
            objective = self._objective_alg
        else:
            objective = self._objective_state
        self._objective: Callable[[], tuple[ca.MX | ca.DM, ca.MX | ca.DM]] = objective

        self.number_of_time_horizonts = number_of_time_horizonts
        self.array_data: None | np.ndarray = None
        self.array_data_mask: None | np.ndarray = None
        self.inverted_variances: None | np.ndarray = None

        self._setup_simulator(
            use_idas_constraints=use_idas_constraints,
            use_algebraic_vars=use_algebraic_vars,
        )
        self._setup_initialization()
        self.logger.debug(
            "Created Optimizer object: \n Data Shape {} \n Desicion Variables {}".format(
                self.array_data.shape, self.varlist_decision.get_variable_name()  # type: ignore
            )
        )

        self.solver_name = "ipopt"
        self.solver_settings = {
            "verbose": False,
            "ipopt": {"hessian_approximation": "limited-memory", "max_iter": 300},
        }

        if reinitialize_algebraic:
            for sim in self.list_simulators:
                sim.calculate_algebraic_initials(apply_intials=True)

    def _setup_simulator(self, *, use_idas_constraints, use_algebraic_vars):
        self.list_simulators: list[Simulator] = []
        varlist_input = self.list_input_varlist[0]
        # Create a time_grid, that "stops" at every experimental data, for every state variable
        time_grid = np.ndarray((1, 0))
        for var in varlist_input.values():
            if isinstance(var, VariableState) or (
                isinstance(var, VariableAlgebraic) and use_algebraic_vars
            ):
                time_grid = np.append(time_grid, var.time_relative)
            elif isinstance(var, VariableParameter):
                var.fixed = True
            elif isinstance(var, VariableControl):
                if isinstance(var, VariableControlPiecewiseConstant):
                    time_grid = np.append(time_grid, var.time_relative)

        time_grid = np.unique(time_grid)

        # Last time_stamp is not used, because no simulation is done after last point
        time_grid_controls = np.linspace(
            time_grid[0], time_grid[-2], num=self.number_of_time_horizonts
        )[1:]
        time_grid = np.append(time_grid, time_grid_controls)
        time_grid = np.unique(time_grid)

        self.time_grid = time_grid
        self.time_grid_controls = time_grid_controls

        for var in varlist_input.values():
            if isinstance(var, VariableState):
                self.varlist_state.add_variable(var)
            elif isinstance(var, VariableParameter):
                self.varlist_parameter.add_variable(var)
            elif isinstance(var, VariableControl):
                self.varlist_control.add_variable(var)
                if var.fixed is False:
                    if isinstance(var, VariableControlPiecewiseConstant):
                        if len(var.variable_list) > 1:
                            raise ValueError(
                                f"Variable should have only first horizon at time=0. You supplied:\n{var} with {var.variable_list}"
                            )
                        else:
                            # New horizons are created with same guess as at time 0
                            # All horizons are unfixed and are decision variables
                            values = [var.get_variable_at_time_relative(0).guess] * (
                                self.number_of_time_horizonts - 1
                            )
                            var.expand_horizon(time_grid_controls, values)
                            for var_control in var.variable_list.values():
                                var_control.fixed = False
                                self.varlist_decision.add_variable(var_control)
                    else:
                        self.varlist_decision.add_variable(var)

        self.list_simulators.append(
            Simulator(
                self.model,
                time_grid,
                varlist_input,
                self.simulator_name,
                self.simulator_settings,
                use_idas_constraints=use_idas_constraints,
            )
        )

        # Generate an array (experiment_data_varlist) with Experimental data with the same dimensions as simulation results.
        experiment_data_varlist = []
        experiment_data_mask_varlist = []

        if use_algebraic_vars:
            variable_name_list = list(
                [*self.model.varlist_state.keys(), *self.model.varlist_algebraic.keys()]
            )
        else:
            variable_name_list = list(self.model.varlist_state.keys())

        for var_name in variable_name_list:
            var = varlist_input[var_name]
            time_grid_var = np.array(var.time_relative)
            # if simulated point has data - set element to True
            experiment_data_mask_var = 1.0 * np.isin(time_grid, time_grid_var)[1:]
            experiment_data_var_real = np.array(var.value)[1:]
            # array that would be filled with Experimental data where data_mask is 1
            experiment_data_var_extended = experiment_data_mask_var.copy()

            # data_var is being redimensioned to the output of simulation
            counter = 0
            for timegrid_index, trigger in enumerate(experiment_data_mask_var):
                if trigger == 1:
                    experiment_data_var_extended[
                        timegrid_index
                    ] = experiment_data_var_real[counter]
                    counter = counter + 1
            experiment_data_varlist.append(experiment_data_var_extended)
            experiment_data_mask_varlist.append(experiment_data_mask_var)

        # Stack data from separate variables and flatten columnwise
        experiment_data_varlist = np.column_stack(experiment_data_varlist).flatten()
        experiment_data_mask_varlist = np.column_stack(
            experiment_data_mask_varlist
        ).flatten()
        self.array_data = experiment_data_varlist
        self.array_data_mask = experiment_data_mask_varlist

        """ Generate arrays with inverted variances and experiments weightning.
        Varainces are used for generation of weighted least squares optimization
        problem. Experiments weightning is used in order to give same weight to
        separate experiments: if one experiment has twice as many experimental
        points, their error is multiplied by 0.5.
        """
        inverted_variances_varlist = []
        for var_name in variable_name_list:
            var = varlist_input[var_name]
            inverted_variances_varlist.append(
                1.0 / (np.full(len(time_grid) - 1, var.variance))
            )
        inverted_variances_varlist = np.column_stack(
            inverted_variances_varlist
        ).flatten()
        self.inverted_variances = inverted_variances_varlist

    def _objective_state(self):
        array_simulation = None

        for simulator in self.list_simulators:
            res_simulation = simulator.simulate()
            if array_simulation is None:
                array_simulation = res_simulation["xf"][:]
            else:
                array_simulation = ca.vertcat(array_simulation, res_simulation["xf"][:])

        # multiply by self.array_data_mask needed to ignore elements were error experimental data is zero
        error = (array_simulation - self.array_data) * self.array_data_mask
        objective = ca.sum1(self.inverted_variances * (error**2))

        return objective

    def _objective_alg(self):
        array_simulation = None

        for simulator in self.list_simulators:
            res_simulation = simulator.simulate()
            if array_simulation is None:
                res_all = ca.vertcat(res_simulation["xf"], res_simulation["zf"])
                array_simulation = res_all[:]
            else:
                res_all = ca.vertcat(res_simulation["xf"], res_simulation["zf"])
                array_simulation = ca.vertcat(array_simulation, res_all[:])

        # multiply by self.array_data_mask needed to ignore elements were error experimental data is zero
        error = (array_simulation - self.array_data) * self.array_data_mask
        objective = ca.sum1(self.inverted_variances * (error**2))

        return objective

    def optimize(self, scale=True):
        """Solves optimization problem. Scaling decreases amount of iterations,
        and should be used as a first option.
        """

        return self._optimize(scale)

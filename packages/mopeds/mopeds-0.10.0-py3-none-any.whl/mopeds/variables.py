from __future__ import annotations

import sys
from collections.abc import Generator, Iterable
from datetime import datetime, timedelta
from typing import Any, Union

if sys.version_info[1] == 8:
    from typing import OrderedDict
elif sys.version_info[1] >= 9:
    from collections import OrderedDict

import casadi as ca
import numpy as np
import pandas as pd

import mopeds

ORIGIN_TS: pd.Timestamp = pd.Timestamp(year=1970, month=1, day=1)
""" Indicats a default zero timestamp for data, if date is irrelevant.
Chosen DateTime is the same, that is used by pd.to_datetime() by default.
"""

def _check_mx_conversion_compitablity(mx: ca.MX):
    if "time_sp" not in str(mx):
        raise NotImplementedError

def convert_mx_to_number(mx: ca.MX):
    if mx.is_symbolic():
        _check_mx_conversion_compitablity(mx)
        return int(str(mx).strip("time_sp")) + 1
    else:
        if mx == 0:
            return 0
        else:
            raise NotImplementedError

# Ignored type errors come from mypy issue https://github.com/python/mypy/issues/3004


class Variable(object):
    def __init__(
        self,
        name: str,
        lb: float | None = None,
        ub: float | None = None,
    ) -> None:
        self.name: str = name
        if not isinstance(self, VariableConstant):
            self.casadi_var: ca.MX = ca.MX.sym(self.name)
        # fixed is property in order to deal with VariableControlPiecewiseConstant properly
        self._fixed: bool = True
        self.opc_ua_id: None | int = None
        if not isinstance(self, VariableControlPiecewiseConstant):
            self.dataframe: pd.DataFrame = None
            self.guess: float = np.nan
            self.lower_bound: float = lb  # type: ignore
            self.upper_bound: float = ub  # type: ignore
        self.variance: float = 1.0
        # attibute used to decide if variable should be plotted
        self.ignore_plotting: bool = True
        self.variable_list: VariableList

    @classmethod
    def get_subclasses(cls) -> Generator[type[Variable], None, None]:
        for subclass in cls.__subclasses__():
            yield from subclass.get_subclasses()
            yield subclass

    def plot(self, ax: None | Axes = None) -> Axes:
        axis = self.dataframe.plot(ax=ax)
        from matplotlib import pyplot as plt
        from matplotlib.axes import Axes

        plt.show()
        return axis

    def __repr__(self) -> str:
        return f"{self.name}\n{type(self)}\n{self.value}\n"

    def get_value_or_casadi(self) -> float | ca.MX:
        """Return either value at time=0 or casadi_variable.
        Used in Simulator for readability and less if statements.
        """
        if self.fixed:
            return self.value[0]
        else:
            return self.casadi_var

    def get_value_or_guess(self) -> float:
        """Return guess or value at time zero. Used further for
        readability"""
        if self.fixed:
            return self.value[0]
        else:
            return self.guess

    @property
    def value(self) -> list[float]:
        """Returns a list with values of variables"""
        return self.dataframe[self.name].tolist()

    @value.setter
    def value(self, value: int | float) -> None:
        """Returns a list with values of variables"""
        if isinstance(value, Iterable):
            raise NotImplementedError(
                "Method can only be used to with scalars. Use variable.dataframe[variable.name] for arrays"
            )
        self.dataframe.iloc[0] = value

    @property
    def time_absolute(self) -> pd.Series:
        """Returns a list which contains time_stamps with date and time"""
        return self.dataframe.index

    @property
    def time_relative(self) -> list[float]:
        """Returns a list which contains timestamps in seconds.
        First time is considered to be zero second"""
        return (self.dataframe.index - self.dataframe.index[0]).total_seconds().tolist()

    def is_value_consistent(self) -> bool | None:
        """Returns True if self.value is consistent or raise Error.

        Checks if index of self.value is increasing and unique,
        ensuring that first element in index is always time=0.
        Checks if any element in Data is Nan.

        Raises:
            BadVariableError: with descriptive text.
        """
        if isinstance(self.dataframe, pd.DataFrame):
            if not self.dataframe.index._is_strictly_monotonic_increasing:
                raise BadVariableError(self, "Value index is not unique or not sorted")
            if self.name not in self.dataframe.columns:
                raise BadVariableError(
                    self, "Column name in Variable.value dosn't equal Variable.name"
                )
            if not isinstance(
                self, (VariableAlgebraic, VariableControlPiecewiseConstant)
            ):
                if self.dataframe[self.name].hasnans:
                    raise BadVariableError(self, "Variable value has Nan")
        else:
            raise BadVariableError(self, "Value of Variable is of wrong type")

        return True

    @property
    def origin_ts(self) -> pd.Timestamp:
        """Propoerty that return the first Timestamp in self.value.

        Can be used to compare if Variables have same origin in .value.
        Does check self.value for consistensy.
        Returns:
            Union[None, pd.Timestamp]:
            None is self.value is None or Timestamp that corresponds to time=0
        """
        self.is_value_consistent()

        if isinstance(self, VariableControlPiecewiseConstant):
            return self.time_absolute[0]
        else:
            return self.dataframe.index[0]

    @property
    def fixed(self) -> bool:
        # VariableControlPiecewiseConstant is fixed only if all variables inside are fixed
        if isinstance(self, VariableControlPiecewiseConstant):
            fixed_list = []
            for variable in self.variable_list.values():
                fixed_list.append(variable.fixed)
            self._fixed = all(fixed_list)
        return self._fixed

    @fixed.setter
    def fixed(self, state: bool) -> None:
        if isinstance(self, VariableControlPiecewiseConstant):
            for var in self.variable_list.values():
                var.fixed = state
        self._fixed = state

    @property
    def get_constraint_idas(self) -> int:
        """Constrain the solution y=[x,z].  0 (default): no constraint on yi,
        1: yi >= 0.0, -1: yi <= 0.0, 2: yi > 0.0, -2: yi < 0.0."}},"""

        if self.lower_bound == 0:
            constraint = 1
        elif self.lower_bound > 0:
            constraint = 2
        elif self.upper_bound == 0:
            constraint = -1
        elif self.upper_bound < 0:
            constraint = -2
        else:
            constraint = 0

        return constraint

    @property
    def lower_bound(self) -> float:
        return self._lower_bound

    @lower_bound.setter
    def lower_bound(self, lower_bound: float | None) -> None:
        if lower_bound is None or lower_bound == -1e9:
            self._lower_bound = -ca.inf
        else:
            self._lower_bound = lower_bound

    @property
    def guess(self) -> float:
        return self._guess

    @guess.setter
    def guess(self, guess: float | None) -> None:
        if guess is None:
            self._guess = np.nan
        else:
            self._guess = guess

    @property
    def upper_bound(self) -> float:
        return self._upper_bound

    @upper_bound.setter
    def upper_bound(self, upper_bound: float | None) -> None:
        if upper_bound is None or upper_bound == 1e9:
            self._upper_bound = ca.inf
        else:
            self._upper_bound = upper_bound

    def _dataframe_from_value(
        self, value: None | float, origin: pd.Timestamp = ORIGIN_TS
    ) -> pd.DataFrame:
        df = pd.DataFrame(
            [value],
            index=[origin],
            columns=[self.name],
            dtype="float64",
        )
        return df

    def set_dataframe_from_value_and_time(
        self,
        value: list[float | int],
        time_relative: list[float | int] | np.ndarray,
        origin: Any = "unix",
    ) -> None:
        if not len(value) == len(time_relative):
            raise ValueError(
                f"Value and time must have same length. Supplied Value:\n{value}\nTime:\n{time_relative}"
            )
        if not time_relative[0] == 0:
            raise ValueError("Time vector should start with 0, you supplied:\n{time}")

        time_series = pd.to_datetime(time_relative, unit="s", origin=origin)
        if isinstance(self, VariableControlPiecewiseConstant):
            raise NotImplementedError
        else:
            dataframe = pd.DataFrame(
                value, index=time_series, columns=[self.name], dtype="float64"
            )
            self.dataframe = dataframe

    def show(self) -> None:
        mopeds.show_html_from_dataframe(self.dataframe)


class VariableState(Variable):
    def __init__(
        self,
        name: str,
        starting_value: float | None = None,
        lb: float | None = None,
        ub: float | None = None,
        opc_ua_id: int | None = None,
    ) -> None:
        super().__init__(name, lb, ub)
        # Assuming that State Variables are always to be plotted
        self.ignore_plotting = False
        self.dataframe = self._dataframe_from_value(starting_value)
        self.opc_ua_id = opc_ua_id


class VariableAlgebraic(Variable):
    def __init__(
        self,
        name: str,
        guess: float | None = None,
        lb: float | None = None,
        ub: float | None = None,
        opc_ua_id: int | None = None,
    ) -> None:
        super().__init__(name, lb, ub)
        self.guess = guess  # type: ignore
        self.opc_ua_id = opc_ua_id
        self.dataframe = self._dataframe_from_value(None)


class VariableParameter(Variable):
    def __init__(
        self,
        name: str,
        value: float | None = None,
        lb: float | None = None,
        ub: float | None = None,
    ) -> None:
        super().__init__(name, lb, ub)
        self.guess = value  # type: ignore
        self.dataframe = self._dataframe_from_value(value)


class VariableControl(Variable):
    def __init__(
        self,
        name: str,
        value: float | None = None,
        lb: float | None = None,
        ub: float | None = None,
        opc_ua_id: int | None = None,
    ) -> None:
        super().__init__(name, lb, ub)
        if not isinstance(self, VariableControlPiecewiseConstant):
            self.dataframe = self._dataframe_from_value(value)
            self.guess = value  # type: ignore
        self.opc_ua_id = opc_ua_id
        self.piecewise_control_name = None


class VariableControlPiecewiseConstant(VariableControl):
    """self.time - [time_stamps] list with time points of all variables in self.variables_list."""

    def __init__(
        self,
        name: str,
        value: float | None = None,
        lb: float | None = None,
        ub: float | None = None,
        opc_ua_id: int | None = None,
    ):
        super().__init__(name)
        self.variable_list = VariableList()
        var_t0 = VariableControl(name + "_t0", value, lb, ub, opc_ua_id)
        var_t0.fixed = True
        var_t0.piecewise_control_name = name
        self.variable_list.add_variable(var_t0)

    @property
    def value(self) -> list[float]:
        values = []
        for var in self.variable_list.values():
            values.extend(var.value)
        return values

    @value.setter
    def value(self, value: int | float) -> None:
        if isinstance(value, Iterable):
            raise NotImplementedError("Method can only be used with scalars.")
        self.variable_list.index(0).value = value

    @property
    def time_absolute(self) -> pd.Series:
        time_list = []
        for variable in self.variable_list.values():
            time_list.append(variable.time_absolute[0])
        time_series = pd.Series(time_list)
        return time_series

    @property
    def lower_bound(self) -> np.ndarray:
        values = []
        for var in self.variable_list.values():
            values.append(var.lower_bound)
        return values

    @lower_bound.setter
    def lower_bound(self, lower_bound: float | None) -> None:
        for var in self.variable_list.values():
            var.lower_bound = lower_bound

    @property
    def upper_bound(self) -> np.ndarray:
        values = []
        for var in self.variable_list.values():
            values.append(var.upper_bound)
        return values

    @upper_bound.setter
    def upper_bound(self, upper_bound: float | None) -> None:
        for var in self.variable_list.values():
            var.upper_bound = upper_bound

    @property
    def guess(self) -> np.ndarray:
        values = []
        for var in self.variable_list.values():
            values.append(var.guess)
        return values

    @guess.setter
    def guess(self, guess: float | None) -> None:
        for var in self.variable_list.values():
            var.guess = guess

    @property
    def time_relative(self) -> list[float]:
        time_series = self.time_absolute
        return (time_series - time_series.iloc[0]).dt.total_seconds().tolist()

    def to_dictionary(self) -> dict[float, Variable]:
        time_var_dict = dict(zip(self.time_relative, list(self.variable_list.values())))
        return time_var_dict

    def get_variable_at_time_absolute(
        self, time_stamp_absolute: pd.Timestamp
    ) -> VariableControl:
        index = pd.Index(self.time_absolute).get_indexer(
            [time_stamp_absolute], method="ffill"
        )[0]
        return list(self.variable_list.values())[index]

    def get_variable_at_time_relative(
        self, time_stamp_relative: float
    ) -> VariableControl:
        if isinstance(time_stamp_relative, ca.MX):
            time_stamp_relative = convert_mx_to_number(time_stamp_relative)
        index = pd.Index(self.time_relative).get_indexer(
            [time_stamp_relative], method="ffill"
        )[0]
        return list(self.variable_list.values())[index]

    def get_value_or_casadi(  # type: ignore
        self, time_grid_relative: list[float] | np.ndarray
    ) -> list[float | ca.MX]:
        """This method is used to avoid following problem: if current Control is fixed at given time_stamp, simulator
        should use either - a fixed value, provided with Variable, or a value of a Control Variable from previous timestamp.
        Input:
                        t0      t1      t2      t3
        Value / Var     20      var_t1  var_t2  20
        Fixed / Unfixed Fixed   Unfixed Unfixed Fixed
        Result:
        Simulate with   20      var_t1  var_t2  var_t2
        """
        independent_variable = []
        last_unfixed_variable = None

        for time_index in range(time_grid_relative.shape[0]):
            time_stamp = time_grid_relative[time_index]
            var_at_timestamp = self.get_variable_at_time_relative(time_stamp)
            # This if statement is required for OED in order to use casadi_var from previous step, if it was already used. Without it, control variable will be fixed to some value for given timestep
            if var_at_timestamp.fixed:
                if last_unfixed_variable is None:
                    independent_variable.append(var_at_timestamp.get_value_or_casadi())
                else:
                    independent_variable.append(
                        last_unfixed_variable.get_value_or_casadi()
                    )
            else:
                last_unfixed_variable = var_at_timestamp
                independent_variable.append(last_unfixed_variable.get_value_or_casadi())

        return independent_variable

    def expand_horizon(self, times: list[float], values: list[float | None]) -> None:
        if not len(times) == len(values):
            raise ValueError(
                "Length of times and values vector should be same. You supplied:\ntimes\n{times}\nvalues\n{values}"
            )
        if not len(self.time_relative) == 1:
            raise NotImplementedError(
                "Cannot be used to expand already expanded variable"
            )
        for index, (time, value) in enumerate(zip(times, values), 1):
            var = VariableControl(
                f"{self.name}_t{index}",
                value,
                self.variable_list.index(0).lower_bound,
                self.variable_list.index(0).upper_bound,
                self.opc_ua_id,
            )
            var.fixed = True
            var.piecewise_control_name = self.name

            if isinstance(time, ca.MX):
                time = convert_mx_to_number(time)

            var.dataframe = var._dataframe_from_value(
                value, self.time_absolute[0] + timedelta(seconds=time)
            )
            self.variable_list.add_variable(var)

    def set_horizon(self, times: Any, values: Any) -> None:
        """Used when control at time 0 should also be rewritten"""
        raise NotImplementedError

    @property
    # WIP, not tested
    def dataframe(self) -> pd.DataFrame:
        values = []
        times = []
        for var in self.variable_list.values():
            values.append(var.value[0])
            times.append(var.time_absolute[0])

        dataframe = pd.DataFrame(
            values, index=times, columns=[self.name], dtype="float64"
        )

        return dataframe


class VariableConstant(Variable):
    def __init__(
        self,
        name: str,
        value: float | None = None,
        opc_ua_id: int | None = None,
    ):
        super().__init__(name)
        self.dataframe = self._dataframe_from_value(value)
        self.opc_ua_id = opc_ua_id
        self.fixed = True

    @property
    def casadi_var(self):
        """Variable Constant doesn't have a a symbolic variable, so casadi_var is replaced
        by a value of the constant in the equations directly"""
        return self.value[0]


class VariableList(OrderedDict[str, Union[Variable, VariableControlPiecewiseConstant]]):
    def __init__(self) -> None:
        super().__init__()

    def __repr__(self) -> str:
        if bool(self):
            types = [type(item) for item in list(self.values())]
            counter_types = {x: types.count(x) for x in types}
            list_names: dict = {var_type: [] for var_type in counter_types.keys()}
            message = f"Var list has {sum(counter_types.values())} variables:\n"
            for var in self.values():
                list_names[type(var)].extend([var.name])
            for var_type in counter_types.keys():
                if "VariableConstant" in str(var_type) or "VariableAlgebraic" in str(
                    var_type
                ):
                    print_list_names = str()
                else:
                    print_list_names = f":\n{list_names[var_type]}"
                message = (
                    message
                    + f"{var_type} of length {counter_types[var_type]}{print_list_names}\n"
                )
        else:
            message = f"Empty {type(self)}"
        return message

    def get_common_origin(
        self, strict: bool = False, variable_type: type[Variable] = Variable
    ) -> pd.Timestamp | bool:
        """Returns a common Timestamp of State, Algebraic, and Control variables. If no common origin exists - return ORIGIN_TS, strict is False

        Args:
            strict: if no common origin is found, return False instead of ORIGIN_TS
        """
        list_of_origins = []
        for variable in self.values():
            if isinstance(variable, variable_type):
                list_of_origins.append(variable.time_absolute[0])

        if len(set(list_of_origins)) < 2:
            return list_of_origins[0]
        else:
            if strict:
                return False
            else:
                return ORIGIN_TS

    @property
    def dataframe(self) -> pd.DataFrame:
        list_df = []
        for var in self.values():
            list_df.append(var.dataframe)
        data_frame = pd.concat(list_df, axis=1, join="outer")
        return data_frame

    def index(self, var_index: int) -> Variable:
        """Return variable at given index (if VariableList was a List).

        Primary way to index Variables in VariableList is name of the variable.
        This method is used for debugging, and should not be used by inexperienced users.
        Args:
            var_index (int): var_index

        Returns:
            Variable: Variable that correspons to given index.
        """
        var: Variable = list(self.values())[var_index]
        return var

    def add_variable(self, variable: Variable) -> None:
        if variable.name in self:
            raise SameVariableNameError(variable.name)
        else:
            self.update({variable.name: variable})

    def get_variable_name(self) -> list[str]:
        names = []
        for var in self.values():
            names.append(var.name)
        return names

    def get_casadi_variables(self) -> ca.MX:
        """Returns a concatanated vector of all variables in a variable_list."""
        casadi_vars = []
        for var in self.values():
            casadi_vars.append(var.casadi_var)
        return ca.vcat(casadi_vars)

    def get_data_opcua(self, time_start: Any, time_stop: Any) -> None:
        # Older implementation doesn't work anymore, removed on 06-15-2022
        raise NotImplementedError

    def set_variable_list_fixed(self, fix_list: list[str] | None = None) -> None:
        self._list_fixation(fix_list, True)

    def set_variable_list_unfixed(self, unfix_list: list[str] | None = None) -> None:
        self._list_fixation(unfix_list, False)

    def _list_fixation(self, fixation_list: list[str] | None, val: bool) -> None:
        if fixation_list is None:
            for var in self.values():
                var.fixed = val
        else:
            for var in self.values():
                if var.name in fixation_list:
                    var.fixed = val

    def set_bounds(
        self, val: int | float = 0.25, emerg_val: int | float | None = None
    ) -> None:
        for var in self.values():
            if (
                isinstance(var, (VariableParameter, VariableControl))
                and var.fixed is False
            ):
                value = var.value[0]
                if value > 0:
                    var.lower_bound = value * (1 - val)
                    var.upper_bound = value * (1 + val)
                elif value < 0:
                    var.lower_bound = value * (1 + val)
                    var.upper_bound = value * (1 - val)
                elif value == 0:
                    if emerg_val is None:
                        # Setting bounds for val == 0 without emerg_val is not implemented
                        raise (NotImplementedError)
                    else:
                        var.lower_bound = -emerg_val
                        var.upper_bound = emerg_val
                else:
                    # Setting bounds for arrays is not implemented
                    raise (NotImplementedError)
                var.guess = var.lower_bound

    def write_data_opcua(self, time_start: datetime) -> None:
        # Older implementation doesn't work anymore, removed on 06-16-2022
        raise NotImplementedError

    def plot(
        self,
        as_one_plot: bool = False,
        algebraic: bool = False,
        prefix: str | None = None,
        show: bool = True,
        **kwargs,
    ) -> Axes | np.ndarray:
        """Plots variables that are not ignored via var.ignore_plotting
        If as_one_plot is True, plot every variable on separate plot
        If algebraic is True, plot als algebraic variables

        prefix is used to append name to a variable name
        **kwargs are matplotlib options, for example marker='o'
        supply ax argument to provide axis and plot multiple varlists
        Use show=True to reuse axis before showing plot"""
        plot_varlist = self._get_varlist_to_plot(algebraic)

        if "subplots" not in kwargs:
            kwargs["subplots"] = True

        if as_one_plot is True:
            axes_list = []
            for var in plot_varlist.values():
                axes_list.append(var.plot())
            axes = np.array(axes_list)

        else:
            dataframe = plot_varlist.dataframe
            if prefix is not None:
                dataframe = dataframe.add_prefix(prefix)
            axes = dataframe.ffill().plot(**kwargs)

        from matplotlib import pyplot as plt

        if show:
            plt.show()

        return axes

    def _get_varlist_to_plot(self, algebraic: bool = False) -> VariableList:
        """Return varlist that has only "plottable" variables"""
        plot_varlist = VariableList()
        for var in self.values():
            if not var.ignore_plotting:
                if isinstance(var, VariableState):
                    plot_varlist.add_variable(var)
                elif isinstance(var, VariableAlgebraic):
                    if algebraic is True:
                        plot_varlist.add_variable(var)
                elif isinstance(var, VariableControlPiecewiseConstant):
                    plot_varlist.add_variable(var)

        return plot_varlist

    def show(self) -> None:
        mopeds.show_html_from_dataframe(self.dataframe)


class SameVariableNameError(Exception):
    def __init__(self, name) -> None:
        message = f"There is already an existing variable with the same name! Wrong variable with name: {name}"
        super().__init__(message)


class BadVariableError(Exception):
    def __init__(self, variable, message=None) -> None:
        if message is None:
            message = "Failed while using this variable:"
        message = message + f"\n{variable}"
        super().__init__(message)


class PlottingError(BadVariableError):
    pass

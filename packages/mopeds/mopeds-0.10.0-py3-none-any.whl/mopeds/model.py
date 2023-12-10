from __future__ import annotations

import casadi as ca

from mopeds import (
    Variable,
    VariableAlgebraic,
    VariableConstant,
    VariableControl,
    VariableList,
    VariableParameter,
    VariableState,
)


class Model(object):
    """Model class is used to get lists of variables used in this model,
    create equations and determine if model is DAE or ODE.
    """

    def __init__(self, variable_list: VariableList, name: str = "default") -> None:
        self.varlist_state: VariableList = VariableList()
        self.varlist_algebraic: VariableList = VariableList()
        # Includes Parameters and Controls
        self.varlist_independent: VariableList = VariableList()
        self._varlist_constant: VariableList = VariableList()

        # This varlist should be used to consistently iterate over all variables in Simulation and Optimization
        self.varlist_all: VariableList = VariableList()
        self.equations_differential: ca.MX = None
        self.equations_algebraic: ca.MX = None
        self.DAE: bool = False

        for var in variable_list.values():
            if isinstance(var, Variable):
                if isinstance(var, VariableState):
                    self.varlist_state.add_variable(VariableState(var.name))
                elif isinstance(var, VariableAlgebraic):
                    self.varlist_algebraic.add_variable(
                        VariableAlgebraic(var.name, var.guess)
                    )
                elif isinstance(var, VariableParameter) or isinstance(
                    var, VariableControl
                ):
                    self.varlist_independent.add_variable(type(var)(var.name))
                elif isinstance(var, VariableConstant):
                    self._varlist_constant.add_variable(
                        VariableConstant(var.name, var.value[0])
                    )
                else:
                    raise VariableTypeError(var.name)
            else:
                raise VariableTypeError(var.name)

        self.varlist_all.update(self.varlist_state)
        self.varlist_all.update(self.varlist_algebraic)
        self.varlist_all.update(self.varlist_independent)
        self.varlist_all.update(self._varlist_constant)

        self.name = name

    def add_equations_differential(self, equations: list[ca.MX]) -> None:
        if self.equations_differential is None:
            self.equations_differential = ca.vcat(equations)
        else:
            # Adding additional equations is not implemented
            raise (NotImplementedError)

    def add_equations_algebraic(self, equations: list[ca.MX]) -> None:
        if self.equations_algebraic is None:
            self.equations_algebraic = ca.vcat(equations)
            self.DAE = True
        else:
            # Adding additional equations is not implemented
            raise (NotImplementedError)


class VariableTypeError(Exception):
    def __init__(self, name) -> None:
        message = f"Not a supported mopeds variable class! Wrong variable with name: {name}"
        super().__init__(message)

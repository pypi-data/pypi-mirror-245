from __future__ import annotations

import copy

import casadi as ca

import mopeds


def empy_dae(
    piecewise_control: bool = False,
) -> tuple[mopeds.VariableList, mopeds.Model]:
    variable_list = mopeds.VariableList()

    variable_list.add_variable(mopeds.VariableState("X1", 0))
    variable_list.add_variable(mopeds.VariableState("X2", 0))
    variable_list.add_variable(mopeds.VariableAlgebraic("Z1", 0.0))

    if piecewise_control:
        variable_list.add_variable(
            mopeds.VariableControlPiecewiseConstant("C", 0.0, -1, 1)
        )
    else:
        variable_list.add_variable(mopeds.VariableControl("C", 0.0, -1, 1))
    variable_list.add_variable(mopeds.VariableParameter("P", 0.0, -1, 1))

    m = mopeds.Model(variable_list)

    dydx1 = m.varlist_all["C"].casadi_var * 0
    dydx2 = m.varlist_all["P"].casadi_var * 0
    alg1 = (
        m.varlist_all["X1"].casadi_var
        + m.varlist_all["X2"].casadi_var
        + m.varlist_all["Z1"].casadi_var
    )

    m.add_equations_differential(
        [
            dydx1,
            dydx2,
        ]
    )
    m.add_equations_algebraic(
        [
            alg1,
        ]
    )

    return variable_list, m


def pendulum_dae_1(
    piecewise_control: bool = False, variable_list: None | mopeds.VariableList = None
) -> tuple[mopeds.VariableList, mopeds.Model]:
    if variable_list is None:
        variable_list = mopeds.VariableList()

        variable_list.add_variable(mopeds.VariableState("x", 3.0))
        variable_list.add_variable(mopeds.VariableState("u", -1.0 / 3))

        variable_list.add_variable(mopeds.VariableAlgebraic("y", 4.0))
        variable_list.add_variable(mopeds.VariableAlgebraic("v", 1.0 / 4))
        variable_list.add_variable(mopeds.VariableAlgebraic("lambda", 1147.0 / 720))

        if piecewise_control:
            variable_list.add_variable(
                mopeds.VariableControlPiecewiseConstant("L", 5.0)
            )
        else:
            variable_list.add_variable(mopeds.VariableControl("L", 5.0))
        variable_list.add_variable(mopeds.VariableParameter("g", 10.0))

    m = mopeds.Model(variable_list)

    # fmt: off
    dydx1 = m.varlist_all["u"].casadi_var
    dydx2 = m.varlist_all["lambda"].casadi_var * m.varlist_all["x"].casadi_var

    alg1 = m.varlist_all["x"].casadi_var ** 2 + m.varlist_all["y"].casadi_var ** 2 - m.varlist_all["L"].casadi_var ** 2
    alg2 = m.varlist_all["u"].casadi_var * m.varlist_all["x"].casadi_var + m.varlist_all["v"].casadi_var * m.varlist_all["y"].casadi_var
    alg3 = m.varlist_all["u"].casadi_var ** 2 - m.varlist_all["g"].casadi_var * m.varlist_all["y"].casadi_var + m.varlist_all["v"].casadi_var ** 2 + m.varlist_all["L"].casadi_var ** 2 * m.varlist_all["lambda"].casadi_var

    m.add_equations_differential([dydx1, dydx2, ])
    m.add_equations_algebraic([alg1, alg2, alg3, ])
    # fmt: on

    return variable_list, m


def cstr_ode(
    piecewise_control: bool = False,
) -> tuple[mopeds.VariableList, mopeds.Model]:
    e0_greek_nu_i1_r1 = -1.0
    e0_greek_nu_i1_r2 = 1.0
    e0_greek_nu_i2_r2 = -1.0
    e0_greek_nu_i3_r1 = 1.0
    e0_greek_nu_i1_r3 = -1.0
    e0_greek_nu_i4_r3 = 1.0
    e0_greek_rho = 800.0
    e0_A = 1.0
    e0_R = 8.314
    e0_V = 1.0

    variable_list = mopeds.VariableList()

    variable_list.add_variable(mopeds.VariableState("e0_T", 273.0))
    variable_list.add_variable(mopeds.VariableState("e0_c_i1", 3.0))
    variable_list.add_variable(mopeds.VariableState("e0_c_i2", 10.0))
    variable_list.add_variable(mopeds.VariableState("e0_c_i3", 0.0))
    variable_list.add_variable(mopeds.VariableState("e0_c_i4", 0.0))

    # fmt: off
    variable_list.add_variable(mopeds.VariableParameter("e0_E_r1", 9.6e4, 9.0e4, 10.0e4))
    variable_list.add_variable(mopeds.VariableParameter("e0_E_r2", 7.2e4, 6.8e4, 7.6e4))
    variable_list.add_variable(mopeds.VariableParameter("e0_E_r3", 6.9e4, 6.5e4, 7.3e4))
    variable_list.add_variable(mopeds.VariableParameter("e0_k_pre_r1", 5.0e6, 4.5e6, 5.5e6))
    variable_list.add_variable(mopeds.VariableParameter("e0_k_pre_r2", 1.0e7, 0.5e7, 1.5e7))
    variable_list.add_variable(mopeds.VariableParameter("e0_k_pre_r3", 5.0e5, 4.5e5, 5.5e5))
    variable_list.add_variable(mopeds.VariableParameter("e0_U", 1.4, 1.0, 1.8))
    variable_list.add_variable(mopeds.VariableParameter("e0_c_p", 3.5, 3.0, 4.0))
    variable_list.add_variable(mopeds.VariableParameter("e0_greek_Deltah_r1", 4.5e-3, 4.0e-3, 5.0e-3))
    variable_list.add_variable(mopeds.VariableParameter("e0_greek_Deltah_r2", -5.5e-3, -6.0e-3, -5.0e-3))
    variable_list.add_variable(mopeds.VariableParameter("e0_greek_Deltah_r3", 4.5e-3, 4.0e-3, 5.0e-3))

    if piecewise_control:
        variable_list.add_variable(mopeds.VariableControlPiecewiseConstant("e0_c_in_i1", 5.0, 4.0, 6.0))
    else:
        variable_list.add_variable(mopeds.VariableControl("e0_c_in_i1", 5.0, 4.0, 6.0))
    variable_list.add_variable(mopeds.VariableControl("e0_c_in_i2", 10.0, 9.0, 11.0))
    variable_list.add_variable(mopeds.VariableControl("e0_c_in_i3", 0.0, 0.0, 1.0))
    variable_list.add_variable(mopeds.VariableControl("e0_c_in_i4", 0.0, 0.0, 1.0))
    if piecewise_control:
        variable_list.add_variable(mopeds.VariableControlPiecewiseConstant("e0_T_in", 373.0, 353.0, 393.0))
    else:
        variable_list.add_variable(mopeds.VariableControl("e0_T_in", 373.0, 353.0, 393.0))
    variable_list.add_variable(mopeds.VariableControl("e0_T_j", 373.0, 353.0, 393.0))
    variable_list.add_variable(mopeds.VariableControl("e0_F", 6.5e-4, 6.0e-4, 7.0e-4))
    # fmt: on

    for var in variable_list.values():
        if isinstance(var, (mopeds.VariableParameter, mopeds.VariableControl)):
            var.guess = var.lower_bound

    if piecewise_control:
        var = variable_list["e0_T_in"].variable_list.index(0)
        var.guess = var.lower_bound
        var = variable_list["e0_c_in_i1"].variable_list.index(0)
        var.guess = var.lower_bound

    m = mopeds.Model(variable_list)

    # fmt: off
    tdot = (((((m.varlist_all["e0_F"].casadi_var / e0_V) * ((m.varlist_all["e0_T_in"].casadi_var - m.varlist_all["e0_T"].casadi_var))) + (((m.varlist_all["e0_U"].casadi_var * e0_A) / (e0_greek_rho * (m.varlist_all["e0_c_p"].casadi_var * e0_V))) * ((m.varlist_all["e0_T_j"].casadi_var - m.varlist_all["e0_T"].casadi_var)))) + (((-m.varlist_all["e0_greek_Deltah_r1"].casadi_var) / (e0_greek_rho * m.varlist_all["e0_c_p"].casadi_var)) * (m.varlist_all["e0_k_pre_r1"].casadi_var * (m.varlist_all["e0_c_i1"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r1"].casadi_var) / (e0_R * m.varlist_all["e0_T"].casadi_var))))))) + (((-m.varlist_all["e0_greek_Deltah_r2"].casadi_var) / (e0_greek_rho * m.varlist_all["e0_c_p"].casadi_var)) * (m.varlist_all["e0_k_pre_r2"].casadi_var * (m.varlist_all["e0_c_i2"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r2"].casadi_var) / (e0_R * m.varlist_all["e0_T"].casadi_var))))))) + (((-m.varlist_all["e0_greek_Deltah_r3"].casadi_var) / (e0_greek_rho * m.varlist_all["e0_c_p"].casadi_var)) * (m.varlist_all["e0_k_pre_r3"].casadi_var * (m.varlist_all["e0_c_i1"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r3"].casadi_var) / (e0_R * m.varlist_all["e0_T"].casadi_var))))))
    c1dot = ((((m.varlist_all["e0_F"].casadi_var / e0_V) * ((m.varlist_all["e0_c_in_i1"].casadi_var - m.varlist_all["e0_c_i1"].casadi_var))) + (e0_greek_nu_i1_r1 * (m.varlist_all["e0_k_pre_r1"].casadi_var * (m.varlist_all["e0_c_i1"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r1"].casadi_var) / (e0_R * m.varlist_all["e0_T"].casadi_var))))))) + (e0_greek_nu_i1_r2 * (m.varlist_all["e0_k_pre_r2"].casadi_var * (m.varlist_all["e0_c_i2"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r2"].casadi_var) / (e0_R * m.varlist_all["e0_T"].casadi_var))))))) + (e0_greek_nu_i1_r3 * (m.varlist_all["e0_k_pre_r3"].casadi_var * (m.varlist_all["e0_c_i1"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r3"].casadi_var) / (e0_R * m.varlist_all["e0_T"].casadi_var))))))
    c2dot = ((m.varlist_all["e0_F"].casadi_var / e0_V) * ((m.varlist_all["e0_c_in_i2"].casadi_var - m.varlist_all["e0_c_i2"].casadi_var))) + (e0_greek_nu_i2_r2 * (m.varlist_all["e0_k_pre_r2"].casadi_var * (m.varlist_all["e0_c_i2"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r2"].casadi_var) / (e0_R * m.varlist_all["e0_T"].casadi_var))))))
    c3dot = ((m.varlist_all["e0_F"].casadi_var / e0_V) * ((m.varlist_all["e0_c_in_i3"].casadi_var - m.varlist_all["e0_c_i3"].casadi_var))) + (e0_greek_nu_i3_r1 * (m.varlist_all["e0_k_pre_r1"].casadi_var * (m.varlist_all["e0_c_i1"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r1"].casadi_var) / (e0_R * m.varlist_all["e0_T"].casadi_var))))))
    c4dot = ((m.varlist_all["e0_F"].casadi_var / e0_V) * ((m.varlist_all["e0_c_in_i4"].casadi_var - m.varlist_all["e0_c_i4"].casadi_var))) + (e0_greek_nu_i4_r3 * (m.varlist_all["e0_k_pre_r3"].casadi_var * (m.varlist_all["e0_c_i1"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r3"].casadi_var) / (e0_R * m.varlist_all["e0_T"].casadi_var))))))
    # fmt: on

    m.add_equations_differential([tdot, c1dot, c2dot, c3dot, c4dot])

    return variable_list, m


def cstr_dae(
    piecewise_control: bool = False,
) -> tuple[mopeds.VariableList, mopeds.Model]:
    e0_greek_nu_i1_r1 = -1.0
    e0_greek_nu_i1_r2 = 1.0
    e0_greek_nu_i2_r2 = -1.0
    e0_greek_nu_i3_r1 = 1.0
    e0_greek_nu_i1_r3 = -1.0
    e0_greek_nu_i4_r3 = 1.0
    e0_greek_rho = 800.0
    e0_A = 1.0
    e0_R = 8.314
    e0_V = 1.0

    variable_list = mopeds.VariableList()

    # fmt: off
    variable_list.add_variable(mopeds.VariableState("e0_T", 273.0))
    variable_list.add_variable(mopeds.VariableState("e0_c_i1", 3.0))
    variable_list.add_variable(mopeds.VariableState("e0_c_i2", 10.0))
    variable_list.add_variable(mopeds.VariableState("e0_c_i3", 0.0))
    variable_list.add_variable(mopeds.VariableState("e0_c_i4", 0.0))
    variable_list.add_variable(mopeds.VariableAlgebraic("e0_c_tot", 13.0))

    variable_list.add_variable(mopeds.VariableParameter("e0_E_r1", 9.6e4, 9.0e4, 10.0e4))
    variable_list.add_variable(mopeds.VariableParameter("e0_E_r2", 7.2e4, 6.8e4, 7.6e4))
    variable_list.add_variable(mopeds.VariableParameter("e0_E_r3", 6.9e4, 6.5e4, 7.3e4))
    variable_list.add_variable(mopeds.VariableParameter("e0_k_pre_r1", 5.0e6, 4.5e6, 5.5e6))
    variable_list.add_variable(mopeds.VariableParameter("e0_k_pre_r2", 1.0e7, 0.5e7, 1.5e7))
    variable_list.add_variable(mopeds.VariableParameter("e0_k_pre_r3", 5.0e5, 4.5e5, 5.5e5))
    variable_list.add_variable(mopeds.VariableParameter("e0_U", 1.4, 1.0, 1.8))
    variable_list.add_variable(mopeds.VariableParameter("e0_c_p", 3.5, 3.0, 4.0))
    variable_list.add_variable(mopeds.VariableParameter("e0_greek_Deltah_r1", 4.5e-3, 4.0e-3, 5.0e-3))
    variable_list.add_variable(mopeds.VariableParameter("e0_greek_Deltah_r2", -5.5e-3, -6.0e-3, -5.0e-3))
    variable_list.add_variable(mopeds.VariableParameter("e0_greek_Deltah_r3", 4.5e-3, 4.0e-3, 5.0e-3))

    if piecewise_control:
        variable_list.add_variable(mopeds.VariableControlPiecewiseConstant("e0_c_in_i1", 5.0, 4.0, 6.0))
    else:
        variable_list.add_variable(mopeds.VariableControl("e0_c_in_i1", 5.0, 4.0, 6.0))
    variable_list.add_variable(mopeds.VariableControl("e0_c_in_i2", 10.0, 9.0, 11.0))
    variable_list.add_variable(mopeds.VariableControl("e0_c_in_i3", 0.0, 0.0, 1.0))
    variable_list.add_variable(mopeds.VariableControl("e0_c_in_i4", 0.0, 0.0, 1.0))
    if piecewise_control:
        variable_list.add_variable(mopeds.VariableControlPiecewiseConstant("e0_T_in", 373.0, 353.0, 393.0))
    else:
        variable_list.add_variable(mopeds.VariableControl("e0_T_in", 373.0, 353.0, 393.0))
    variable_list.add_variable(mopeds.VariableControl("e0_T_j", 373.0, 353.0, 393.0))
    variable_list.add_variable(mopeds.VariableControl("e0_F", 6.5e-4, 6.0e-4, 7.0e-4))
    # fmt: on

    for var in variable_list.values():
        if isinstance(var, (mopeds.VariableParameter, mopeds.VariableControl)):
            var.guess = var.lower_bound

    if piecewise_control:
        var = variable_list["e0_T_in"].variable_list.index(0)
        var.guess = var.lower_bound
        var = variable_list["e0_c_in_i1"].variable_list.index(0)
        var.guess = var.lower_bound

    m = mopeds.Model(variable_list)

    # fmt: off
    tdot = (((((m.varlist_all["e0_F"].casadi_var / e0_V) * ((m.varlist_all["e0_T_in"].casadi_var - m.varlist_all["e0_T"].casadi_var))) + (((m.varlist_all["e0_U"].casadi_var * e0_A) / (e0_greek_rho * (m.varlist_all["e0_c_p"].casadi_var * e0_V))) * ((m.varlist_all["e0_T_j"].casadi_var - m.varlist_all["e0_T"].casadi_var)))) + (((-m.varlist_all["e0_greek_Deltah_r1"].casadi_var) / (e0_greek_rho * m.varlist_all["e0_c_p"].casadi_var)) * (m.varlist_all["e0_k_pre_r1"].casadi_var * (m.varlist_all["e0_c_i1"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r1"].casadi_var) / (e0_R * m.varlist_all["e0_T"].casadi_var))))))) + (((-m.varlist_all["e0_greek_Deltah_r2"].casadi_var) / (e0_greek_rho * m.varlist_all["e0_c_p"].casadi_var)) * (m.varlist_all["e0_k_pre_r2"].casadi_var * (m.varlist_all["e0_c_i2"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r2"].casadi_var) / (e0_R * m.varlist_all["e0_T"].casadi_var))))))) + (((-m.varlist_all["e0_greek_Deltah_r3"].casadi_var) / (e0_greek_rho * m.varlist_all["e0_c_p"].casadi_var)) * (m.varlist_all["e0_k_pre_r3"].casadi_var * (m.varlist_all["e0_c_i1"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r3"].casadi_var) / (e0_R * m.varlist_all["e0_T"].casadi_var))))))
    c1dot = ((((m.varlist_all["e0_F"].casadi_var / e0_V) * ((m.varlist_all["e0_c_in_i1"].casadi_var - m.varlist_all["e0_c_i1"].casadi_var))) + (e0_greek_nu_i1_r1 * (m.varlist_all["e0_k_pre_r1"].casadi_var * (m.varlist_all["e0_c_i1"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r1"].casadi_var) / (e0_R * m.varlist_all["e0_T"].casadi_var))))))) + (e0_greek_nu_i1_r2 * (m.varlist_all["e0_k_pre_r2"].casadi_var * (m.varlist_all["e0_c_i2"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r2"].casadi_var) / (e0_R * m.varlist_all["e0_T"].casadi_var))))))) + (e0_greek_nu_i1_r3 * (m.varlist_all["e0_k_pre_r3"].casadi_var * (m.varlist_all["e0_c_i1"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r3"].casadi_var) / (e0_R * m.varlist_all["e0_T"].casadi_var))))))
    c2dot = ((m.varlist_all["e0_F"].casadi_var / e0_V) * ((m.varlist_all["e0_c_in_i2"].casadi_var - m.varlist_all["e0_c_i2"].casadi_var))) + (e0_greek_nu_i2_r2 * (m.varlist_all["e0_k_pre_r2"].casadi_var * (m.varlist_all["e0_c_i2"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r2"].casadi_var) / (e0_R * m.varlist_all["e0_T"].casadi_var))))))
    c3dot = ((m.varlist_all["e0_F"].casadi_var / e0_V) * ((m.varlist_all["e0_c_in_i3"].casadi_var - m.varlist_all["e0_c_i3"].casadi_var))) + (e0_greek_nu_i3_r1 * (m.varlist_all["e0_k_pre_r1"].casadi_var * (m.varlist_all["e0_c_i1"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r1"].casadi_var) / (e0_R * m.varlist_all["e0_T"].casadi_var))))))
    c4dot = ((m.varlist_all["e0_F"].casadi_var / e0_V) * ((m.varlist_all["e0_c_in_i4"].casadi_var - m.varlist_all["e0_c_i4"].casadi_var))) + (e0_greek_nu_i4_r3 * (m.varlist_all["e0_k_pre_r3"].casadi_var * (m.varlist_all["e0_c_i1"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r3"].casadi_var) / (e0_R * m.varlist_all["e0_T"].casadi_var))))))

    ctot = m.varlist_all["e0_c_tot"].casadi_var - m.varlist_all["e0_c_i1"].casadi_var - m.varlist_all["e0_c_i2"].casadi_var - m.varlist_all["e0_c_i3"].casadi_var - m.varlist_all["e0_c_i4"].casadi_var
    # fmt: on

    m.add_equations_differential([tdot, c1dot, c2dot, c3dot, c4dot])
    m.add_equations_algebraic([ctot])

    return variable_list, m


def cstr_ode_constant(
    piecewise_control: bool = False,
) -> tuple[mopeds.VariableList, mopeds.Model]:

    variable_list = mopeds.VariableList()

    # fmt: off
    variable_list.add_variable(mopeds.VariableState("e0_T", 273.0))
    variable_list.add_variable(mopeds.VariableState("e0_c_i1", 3.0))
    variable_list.add_variable(mopeds.VariableState("e0_c_i2", 10.0))
    variable_list.add_variable(mopeds.VariableState("e0_c_i3", 0.0))
    variable_list.add_variable(mopeds.VariableState("e0_c_i4", 0.0))

    variable_list.add_variable(mopeds.VariableParameter("e0_E_r1", 9.6e4, 9.0e4, 10.0e4))
    variable_list.add_variable(mopeds.VariableParameter("e0_E_r2", 7.2e4, 6.8e4, 7.6e4))
    variable_list.add_variable(mopeds.VariableParameter("e0_E_r3", 6.9e4, 6.5e4, 7.3e4))
    variable_list.add_variable(mopeds.VariableParameter("e0_k_pre_r1", 5.0e6, 4.5e6, 5.5e6))
    variable_list.add_variable(mopeds.VariableParameter("e0_k_pre_r2", 1.0e7, 0.5e7, 1.5e7))
    variable_list.add_variable(mopeds.VariableParameter("e0_k_pre_r3", 5.0e5, 4.5e5, 5.5e5))
    variable_list.add_variable(mopeds.VariableParameter("e0_U", 1.4, 1.0, 1.8))
    variable_list.add_variable(mopeds.VariableParameter("e0_c_p", 3.5, 3.0, 4.0))
    variable_list.add_variable(mopeds.VariableParameter("e0_greek_Deltah_r1", 4.5e-3, 4.0e-3, 5.0e-3))
    variable_list.add_variable(mopeds.VariableParameter("e0_greek_Deltah_r2", -5.5e-3, -6.0e-3, -5.0e-3))
    variable_list.add_variable(mopeds.VariableParameter("e0_greek_Deltah_r3", 4.5e-3, 4.0e-3, 5.0e-3))

    if piecewise_control:
        variable_list.add_variable(mopeds.VariableControlPiecewiseConstant("e0_c_in_i1", 5.0, 4.0, 6.0))
    else:
        variable_list.add_variable(mopeds.VariableControl("e0_c_in_i1", 5.0, 4.0, 6.0))
    variable_list.add_variable(mopeds.VariableControl("e0_c_in_i2", 10.0, 9.0, 11.0))
    variable_list.add_variable(mopeds.VariableControl("e0_c_in_i3", 0.0, 0.0, 1.0))
    variable_list.add_variable(mopeds.VariableControl("e0_c_in_i4", 0.0, 0.0, 1.0))
    if piecewise_control:
        variable_list.add_variable(mopeds.VariableControlPiecewiseConstant("e0_T_in", 373.0, 353.0, 393.0))
    else:
        variable_list.add_variable(mopeds.VariableControl("e0_T_in", 373.0, 353.0, 393.0))
    variable_list.add_variable(mopeds.VariableControl("e0_T_j", 373.0, 353.0, 393.0))
    variable_list.add_variable(mopeds.VariableControl("e0_F", 6.5e-4, 6.0e-4, 7.0e-4))

    variable_list.add_variable(mopeds.VariableConstant("e0_greek_nu_i1_r1", -1.0))
    variable_list.add_variable(mopeds.VariableConstant("e0_greek_nu_i1_r2", 1.0))
    variable_list.add_variable(mopeds.VariableConstant("e0_greek_nu_i2_r2", -1.0))
    variable_list.add_variable(mopeds.VariableConstant("e0_greek_nu_i3_r1", 1.0))
    variable_list.add_variable(mopeds.VariableConstant("e0_greek_nu_i1_r3", -1.0))
    variable_list.add_variable(mopeds.VariableConstant("e0_greek_nu_i4_r3", 1.0))
    variable_list.add_variable(mopeds.VariableConstant("e0_greek_rho", 800.0))
    variable_list.add_variable(mopeds.VariableConstant("e0_A", 1.0))
    variable_list.add_variable(mopeds.VariableConstant("e0_R", 8.314))
    variable_list.add_variable(mopeds.VariableConstant("e0_V", 1.0))
    # fmt: on

    for var in variable_list.values():
        var.guess = var.lower_bound

    if piecewise_control:
        var = variable_list["e0_T_in"].variable_list.index(0)
        var.guess = var.lower_bound
        var = variable_list["e0_c_in_i1"].variable_list.index(0)
        var.guess = var.lower_bound

    m = mopeds.Model(variable_list)

    # fmt: off
    tdot = (((((m.varlist_all["e0_F"].casadi_var / m.varlist_all["e0_V"].casadi_var) * ((m.varlist_all["e0_T_in"].casadi_var - m.varlist_all["e0_T"].casadi_var))) + (((m.varlist_all["e0_U"].casadi_var * m.varlist_all["e0_A"].casadi_var) / (m.varlist_all["e0_greek_rho"].casadi_var * (m.varlist_all["e0_c_p"].casadi_var * m.varlist_all["e0_V"].casadi_var))) * ((m.varlist_all["e0_T_j"].casadi_var - m.varlist_all["e0_T"].casadi_var)))) + (((-m.varlist_all["e0_greek_Deltah_r1"].casadi_var) / (m.varlist_all["e0_greek_rho"].casadi_var * m.varlist_all["e0_c_p"].casadi_var)) * (m.varlist_all["e0_k_pre_r1"].casadi_var * (m.varlist_all["e0_c_i1"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r1"].casadi_var) / (m.varlist_all["e0_R"].casadi_var * m.varlist_all["e0_T"].casadi_var))))))) + (((-m.varlist_all["e0_greek_Deltah_r2"].casadi_var) / (m.varlist_all["e0_greek_rho"].casadi_var * m.varlist_all["e0_c_p"].casadi_var)) * (m.varlist_all["e0_k_pre_r2"].casadi_var * (m.varlist_all["e0_c_i2"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r2"].casadi_var) / (m.varlist_all["e0_R"].casadi_var * m.varlist_all["e0_T"].casadi_var))))))) + (((-m.varlist_all["e0_greek_Deltah_r3"].casadi_var) / (m.varlist_all["e0_greek_rho"].casadi_var * m.varlist_all["e0_c_p"].casadi_var)) * (m.varlist_all["e0_k_pre_r3"].casadi_var * (m.varlist_all["e0_c_i1"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r3"].casadi_var) / (m.varlist_all["e0_R"].casadi_var * m.varlist_all["e0_T"].casadi_var))))))
    c1dot = ((((m.varlist_all["e0_F"].casadi_var / m.varlist_all["e0_V"].casadi_var) * ((m.varlist_all["e0_c_in_i1"].casadi_var - m.varlist_all["e0_c_i1"].casadi_var))) + (m.varlist_all["e0_greek_nu_i1_r1"].casadi_var * (m.varlist_all["e0_k_pre_r1"].casadi_var * (m.varlist_all["e0_c_i1"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r1"].casadi_var) / (m.varlist_all["e0_R"].casadi_var * m.varlist_all["e0_T"].casadi_var))))))) + (m.varlist_all["e0_greek_nu_i1_r2"].casadi_var * (m.varlist_all["e0_k_pre_r2"].casadi_var * (m.varlist_all["e0_c_i2"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r2"].casadi_var) / (m.varlist_all["e0_R"].casadi_var * m.varlist_all["e0_T"].casadi_var))))))) + (m.varlist_all["e0_greek_nu_i1_r3"].casadi_var * (m.varlist_all["e0_k_pre_r3"].casadi_var * (m.varlist_all["e0_c_i1"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r3"].casadi_var) / (m.varlist_all["e0_R"].casadi_var * m.varlist_all["e0_T"].casadi_var))))))
    c2dot = ((m.varlist_all["e0_F"].casadi_var / m.varlist_all["e0_V"].casadi_var) * ((m.varlist_all["e0_c_in_i2"].casadi_var - m.varlist_all["e0_c_i2"].casadi_var))) + (m.varlist_all["e0_greek_nu_i2_r2"].casadi_var * (m.varlist_all["e0_k_pre_r2"].casadi_var * (m.varlist_all["e0_c_i2"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r2"].casadi_var) / (m.varlist_all["e0_R"].casadi_var * m.varlist_all["e0_T"].casadi_var))))))
    c3dot = ((m.varlist_all["e0_F"].casadi_var / m.varlist_all["e0_V"].casadi_var) * ((m.varlist_all["e0_c_in_i3"].casadi_var - m.varlist_all["e0_c_i3"].casadi_var))) + (m.varlist_all["e0_greek_nu_i3_r1"].casadi_var * (m.varlist_all["e0_k_pre_r1"].casadi_var * (m.varlist_all["e0_c_i1"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r1"].casadi_var) / (m.varlist_all["e0_R"].casadi_var * m.varlist_all["e0_T"].casadi_var))))))
    c4dot = ((m.varlist_all["e0_F"].casadi_var / m.varlist_all["e0_V"].casadi_var) * ((m.varlist_all["e0_c_in_i4"].casadi_var - m.varlist_all["e0_c_i4"].casadi_var))) + (m.varlist_all["e0_greek_nu_i4_r3"].casadi_var * (m.varlist_all["e0_k_pre_r3"].casadi_var * (m.varlist_all["e0_c_i1"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r3"].casadi_var) / (m.varlist_all["e0_R"].casadi_var * m.varlist_all["e0_T"].casadi_var))))))
    # fmt: on

    m.add_equations_differential([tdot, c1dot, c2dot, c3dot, c4dot])

    return variable_list, m


def cstr_dae_constant(
    piecewise_control: bool = False,
) -> tuple[mopeds.VariableList, mopeds.Model]:
    variable_list = mopeds.VariableList()

    # fmt: off
    variable_list.add_variable(mopeds.VariableState("e0_T", 273.0))
    variable_list.add_variable(mopeds.VariableState("e0_c_i1", 3.0))
    variable_list.add_variable(mopeds.VariableState("e0_c_i2", 10.0))
    variable_list.add_variable(mopeds.VariableState("e0_c_i3", 0.0))
    variable_list.add_variable(mopeds.VariableState("e0_c_i4", 0.0))
    variable_list.add_variable(mopeds.VariableAlgebraic("e0_c_tot", 13.0))

    variable_list.add_variable(mopeds.VariableParameter("e0_E_r1", 9.6e4, 9.0e4, 10.0e4))
    variable_list.add_variable(mopeds.VariableParameter("e0_E_r2", 7.2e4, 6.8e4, 7.6e4))
    variable_list.add_variable(mopeds.VariableParameter("e0_E_r3", 6.9e4, 6.5e4, 7.3e4))
    variable_list.add_variable(mopeds.VariableParameter("e0_k_pre_r1", 5.0e6, 4.5e6, 5.5e6))
    variable_list.add_variable(mopeds.VariableParameter("e0_k_pre_r2", 1.0e7, 0.5e7, 1.5e7))
    variable_list.add_variable(mopeds.VariableParameter("e0_k_pre_r3", 5.0e5, 4.5e5, 5.5e5))
    variable_list.add_variable(mopeds.VariableParameter("e0_U", 1.4, 1.0, 1.8))
    variable_list.add_variable(mopeds.VariableParameter("e0_c_p", 3.5, 3.0, 4.0))
    variable_list.add_variable(mopeds.VariableParameter("e0_greek_Deltah_r1", 4.5e-3, 4.0e-3, 5.0e-3))
    variable_list.add_variable(mopeds.VariableParameter("e0_greek_Deltah_r2", -5.5e-3, -6.0e-3, -5.0e-3))
    variable_list.add_variable(mopeds.VariableParameter("e0_greek_Deltah_r3", 4.5e-3, 4.0e-3, 5.0e-3))

    if piecewise_control:
        variable_list.add_variable(mopeds.VariableControlPiecewiseConstant("e0_c_in_i1", 5.0, 4.0, 6.0))
    else:
        variable_list.add_variable(mopeds.VariableControl("e0_c_in_i1", 5.0, 4.0, 6.0))
    variable_list.add_variable(mopeds.VariableControl("e0_c_in_i2", 10.0, 9.0, 11.0))
    variable_list.add_variable(mopeds.VariableControl("e0_c_in_i3", 0.0, 0.0, 1.0))
    variable_list.add_variable(mopeds.VariableControl("e0_c_in_i4", 0.0, 0.0, 1.0))
    if piecewise_control:
        variable_list.add_variable(mopeds.VariableControlPiecewiseConstant("e0_T_in", 373.0, 353.0, 393.0))
    else:
        variable_list.add_variable(mopeds.VariableControl("e0_T_in", 373.0, 353.0, 393.0))
    variable_list.add_variable(mopeds.VariableControl("e0_T_j", 373.0, 353.0, 393.0))
    variable_list.add_variable(mopeds.VariableControl("e0_F", 6.5e-4, 6.0e-4, 7.0e-4))

    variable_list.add_variable(mopeds.VariableConstant("e0_greek_nu_i1_r1", -1.0))
    variable_list.add_variable(mopeds.VariableConstant("e0_greek_nu_i1_r2", 1.0))
    variable_list.add_variable(mopeds.VariableConstant("e0_greek_nu_i2_r2", -1.0))
    variable_list.add_variable(mopeds.VariableConstant("e0_greek_nu_i3_r1", 1.0))
    variable_list.add_variable(mopeds.VariableConstant("e0_greek_nu_i1_r3", -1.0))
    variable_list.add_variable(mopeds.VariableConstant("e0_greek_nu_i4_r3", 1.0))
    variable_list.add_variable(mopeds.VariableConstant("e0_greek_rho", 800.0))
    variable_list.add_variable(mopeds.VariableConstant("e0_A", 1.0))
    variable_list.add_variable(mopeds.VariableConstant("e0_R", 8.314))
    variable_list.add_variable(mopeds.VariableConstant("e0_V", 1.0))
    # fmt: on

    for var in variable_list.values():
        if not var.name == "e0_c_tot":
            var.guess = var.lower_bound

    if piecewise_control:
        var = variable_list["e0_T_in"].variable_list.index(0)
        var.guess = var.lower_bound
        var = variable_list["e0_c_in_i1"].variable_list.index(0)
        var.guess = var.lower_bound

    m = mopeds.Model(variable_list)

    # fmt: off
    tdot = (((((m.varlist_all["e0_F"].casadi_var / m.varlist_all["e0_V"].casadi_var) * ((m.varlist_all["e0_T_in"].casadi_var - m.varlist_all["e0_T"].casadi_var))) + (((m.varlist_all["e0_U"].casadi_var * m.varlist_all["e0_A"].casadi_var) / (m.varlist_all["e0_greek_rho"].casadi_var * (m.varlist_all["e0_c_p"].casadi_var * m.varlist_all["e0_V"].casadi_var))) * ((m.varlist_all["e0_T_j"].casadi_var - m.varlist_all["e0_T"].casadi_var)))) + (((-m.varlist_all["e0_greek_Deltah_r1"].casadi_var) / (m.varlist_all["e0_greek_rho"].casadi_var * m.varlist_all["e0_c_p"].casadi_var)) * (m.varlist_all["e0_k_pre_r1"].casadi_var * (m.varlist_all["e0_c_i1"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r1"].casadi_var) / (m.varlist_all["e0_R"].casadi_var * m.varlist_all["e0_T"].casadi_var))))))) + (((-m.varlist_all["e0_greek_Deltah_r2"].casadi_var) / (m.varlist_all["e0_greek_rho"].casadi_var * m.varlist_all["e0_c_p"].casadi_var)) * (m.varlist_all["e0_k_pre_r2"].casadi_var * (m.varlist_all["e0_c_i2"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r2"].casadi_var) / (m.varlist_all["e0_R"].casadi_var * m.varlist_all["e0_T"].casadi_var))))))) + (((-m.varlist_all["e0_greek_Deltah_r3"].casadi_var) / (m.varlist_all["e0_greek_rho"].casadi_var * m.varlist_all["e0_c_p"].casadi_var)) * (m.varlist_all["e0_k_pre_r3"].casadi_var * (m.varlist_all["e0_c_i1"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r3"].casadi_var) / (m.varlist_all["e0_R"].casadi_var * m.varlist_all["e0_T"].casadi_var))))))
    c1dot = ((((m.varlist_all["e0_F"].casadi_var / m.varlist_all["e0_V"].casadi_var) * ((m.varlist_all["e0_c_in_i1"].casadi_var - m.varlist_all["e0_c_i1"].casadi_var))) + (m.varlist_all["e0_greek_nu_i1_r1"].casadi_var * (m.varlist_all["e0_k_pre_r1"].casadi_var * (m.varlist_all["e0_c_i1"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r1"].casadi_var) / (m.varlist_all["e0_R"].casadi_var * m.varlist_all["e0_T"].casadi_var))))))) + (m.varlist_all["e0_greek_nu_i1_r2"].casadi_var * (m.varlist_all["e0_k_pre_r2"].casadi_var * (m.varlist_all["e0_c_i2"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r2"].casadi_var) / (m.varlist_all["e0_R"].casadi_var * m.varlist_all["e0_T"].casadi_var))))))) + (m.varlist_all["e0_greek_nu_i1_r3"].casadi_var * (m.varlist_all["e0_k_pre_r3"].casadi_var * (m.varlist_all["e0_c_i1"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r3"].casadi_var) / (m.varlist_all["e0_R"].casadi_var * m.varlist_all["e0_T"].casadi_var))))))
    c2dot = ((m.varlist_all["e0_F"].casadi_var / m.varlist_all["e0_V"].casadi_var) * ((m.varlist_all["e0_c_in_i2"].casadi_var - m.varlist_all["e0_c_i2"].casadi_var))) + (m.varlist_all["e0_greek_nu_i2_r2"].casadi_var * (m.varlist_all["e0_k_pre_r2"].casadi_var * (m.varlist_all["e0_c_i2"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r2"].casadi_var) / (m.varlist_all["e0_R"].casadi_var * m.varlist_all["e0_T"].casadi_var))))))
    c3dot = ((m.varlist_all["e0_F"].casadi_var / m.varlist_all["e0_V"].casadi_var) * ((m.varlist_all["e0_c_in_i3"].casadi_var - m.varlist_all["e0_c_i3"].casadi_var))) + (m.varlist_all["e0_greek_nu_i3_r1"].casadi_var * (m.varlist_all["e0_k_pre_r1"].casadi_var * (m.varlist_all["e0_c_i1"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r1"].casadi_var) / (m.varlist_all["e0_R"].casadi_var * m.varlist_all["e0_T"].casadi_var))))))
    c4dot = ((m.varlist_all["e0_F"].casadi_var / m.varlist_all["e0_V"].casadi_var) * ((m.varlist_all["e0_c_in_i4"].casadi_var - m.varlist_all["e0_c_i4"].casadi_var))) + (m.varlist_all["e0_greek_nu_i4_r3"].casadi_var * (m.varlist_all["e0_k_pre_r3"].casadi_var * (m.varlist_all["e0_c_i1"].casadi_var * ca.exp(((-m.varlist_all["e0_E_r3"].casadi_var) / (m.varlist_all["e0_R"].casadi_var * m.varlist_all["e0_T"].casadi_var))))))

    ctot = m.varlist_all["e0_c_tot"].casadi_var - m.varlist_all["e0_c_i1"].casadi_var - m.varlist_all["e0_c_i2"].casadi_var - m.varlist_all["e0_c_i3"].casadi_var - m.varlist_all["e0_c_i4"].casadi_var
    # fmt: on

    m.add_equations_differential([tdot, c1dot, c2dot, c3dot, c4dot])
    m.add_equations_algebraic([ctot])

    return variable_list, m


def vle_nle_problem() -> tuple[mopeds.VariableList, mopeds.Model]:
    # Id. VLE of EtOH and Water

    # Variables
    variable_list = mopeds.variables.VariableList()  # Preallocate variable_list

    # Define variables
    #     T in K
    #     x in 1
    #     P in Pa
    #     # EtOH = 1,      H2O = 2
    #     a = [5.24125,    5.19625] # a in 1
    #     b = [1592.864,   1730.630]# b in K
    #     c = [-46.9659,   -39.7239] # c in K

    variable_list.add_variable(mopeds.VariableAlgebraic("T", 373))
    variable_list.add_variable(mopeds.VariableControl("x", 0.5))
    variable_list.add_variable(mopeds.VariableControl("P", 1e5))
    variable_list.add_variable(mopeds.VariableParameter("a1", 5.24125))
    variable_list.add_variable(mopeds.VariableParameter("a2", 5.19625))
    variable_list.add_variable(mopeds.VariableParameter("b1", 1592.864))
    variable_list.add_variable(mopeds.VariableParameter("b2", 1730.630))
    variable_list.add_variable(mopeds.VariableParameter("c1", -46.9659))
    variable_list.add_variable(mopeds.VariableParameter("c2", -39.7239))

    model = mopeds.Model(variable_list)  # adding all variables to the model

    # Equations
    RES = model.varlist_all["P"].casadi_var - (
        model.varlist_all["x"].casadi_var
        * 10
        ** (
            model.varlist_all["a1"].casadi_var
            - model.varlist_all["b1"].casadi_var
            / (model.varlist_all["c1"].casadi_var + model.varlist_all["T"].casadi_var)
        )
        * 1e5
        + (1 - model.varlist_all["x"].casadi_var)
        * 10
        ** (
            model.varlist_all["a2"].casadi_var
            - model.varlist_all["b2"].casadi_var
            / (model.varlist_all["c2"].casadi_var + model.varlist_all["T"].casadi_var)
        )
        * 1e5
    )
    model.add_equations_algebraic([RES])  # adding the equations to model

    return variable_list, model


def bod_model() -> tuple[
    mopeds.VariableList, mopeds.Model, list[mopeds.VariableList]
]:
    # BOD data as used in Bates, Watts, Nonlinear regression analysis: Its applications
    variable_list = mopeds.variables.VariableList()  # Preallocate variable_list

    variable_list.add_variable(mopeds.VariableAlgebraic("f", 8.3))
    variable_list.add_variable(mopeds.VariableControl("x", 1))
    variable_list.add_variable(mopeds.VariableParameter("theta1", 20))
    variable_list.add_variable(mopeds.VariableParameter("theta2", 0.24))

    m = mopeds.Model(variable_list)  # adding all variables to the model

    f = m.varlist_all["f"].casadi_var  # noqa: E501
    x = m.varlist_all["x"].casadi_var  # noqa: E501
    theta1 = m.varlist_all["theta1"].casadi_var  # noqa: E501
    theta2 = m.varlist_all["theta2"].casadi_var  # noqa: E501

    equation = f - (theta1 * (1 - ca.exp(-theta2 * x)))
    # Equations
    m.add_equations_algebraic([equation])  # adding the equations to model

    data = [
        [1, 8.3],
        [2, 10.3],
        [3, 19.0],
        [4, 16.0],
        [5, 15.6],
        [7, 19.8],
    ]

    exp_data = []

    for x_i, f_i in data:
        var_list = copy.deepcopy(variable_list)
        var_list["f"].value = f_i
        var_list["x"].value = x_i
        var_list["theta1"].fixed = False
        var_list["theta1"].lower_bound = 0
        var_list["theta1"].upper_bound = 40
        var_list["theta2"].fixed = False
        var_list["theta2"].lower_bound = 0
        var_list["theta2"].upper_bound = 1
        exp_data.append(var_list)

    return variable_list, m, exp_data


def puromycin_model() -> tuple[
    mopeds.VariableList, mopeds.Model, dict(list[mopeds.VariableList])
]:
    # Puromycin data as used in Bates, Watts, Nonlinear regression analysis: Its applications
    variable_list = mopeds.variables.VariableList()  # Preallocate variable_list

    variable_list.add_variable(mopeds.VariableAlgebraic("f", 8.3))
    variable_list.add_variable(mopeds.VariableControl("x", 1))
    variable_list.add_variable(mopeds.VariableParameter("theta1", 212.7))
    variable_list.add_variable(mopeds.VariableParameter("theta2", 0.0641))

    m = mopeds.Model(variable_list)  # adding all variables to the model

    f = m.varlist_all["f"].casadi_var  # noqa: E501
    x = m.varlist_all["x"].casadi_var  # noqa: E501
    theta1 = m.varlist_all["theta1"].casadi_var  # noqa: E501
    theta2 = m.varlist_all["theta2"].casadi_var  # noqa: E501

    equation = f - ((theta1 * x) / (theta2 + x))
    # Equations
    m.add_equations_algebraic([equation])  # adding the equations to model

    data_dict = {
        "Treated": [
            [0.02, 76],
            [0.02, 47],
            [0.06, 97],
            [0.06, 107],
            [0.11, 123],
            [0.11, 139],
            [0.22, 159],
            [0.22, 152],
            [0.56, 191],
            [0.56, 201],
            [1.10, 207],
            [1.10, 200],
        ],
        "Untreated": [
            [0.02, 67],
            [0.02, 51],
            [0.06, 84],
            [0.06, 86],
            [0.11, 98],
            [0.11, 115],
            [0.22, 131],
            [0.22, 124],
            [0.56, 144],
            [0.56, 158],
            [1.10, 160],
            [1.10, 160],
        ],
    }

    exp_data = {}

    for name in list(["Treated", "Untreated"]):
        data = data_dict[name]
        exp_data_list = []

        for x_i, f_i in data:
            var_list = copy.deepcopy(variable_list)
            var_list["f"].value = f_i
            var_list["x"].value = x_i
            var_list["theta1"].fixed = False
            var_list["theta1"].lower_bound = 0
            var_list["theta1"].upper_bound = 300
            var_list["theta2"].fixed = False
            var_list["theta2"].lower_bound = 0
            var_list["theta2"].upper_bound = 1
            exp_data_list.append(var_list)
        exp_data[name] = exp_data_list

    return variable_list, m, exp_data


def simple_mixer() -> tuple[mopeds.VariableList, mopeds.Model]:
    variable_list = mopeds.VariableList()
    variable_list.add_variable(mopeds.VariableAlgebraic("e0_F_s2", 20.0))  # noqa: E501
    variable_list.add_variable(mopeds.VariableAlgebraic("e0_F_s4", 7.0))  # noqa: E501
    variable_list.add_variable(mopeds.VariableControl("e0_F_s1", 21.0))  # noqa: E501
    variable_list.add_variable(mopeds.VariableParameter("e0_F_s3", 13.0))  # noqa: E501
    variable_list.add_variable(mopeds.VariableAlgebraic("e0_F_s5", 20.0))  # noqa: E501

    m = mopeds.Model(variable_list)

    e0_F_s1 = m.varlist_all["e0_F_s1"].casadi_var  # noqa: E501
    e0_F_s3 = m.varlist_all["e0_F_s3"].casadi_var  # noqa: E501
    e0_F_s2 = m.varlist_all["e0_F_s2"].casadi_var  # noqa: E501
    e0_F_s4 = m.varlist_all["e0_F_s4"].casadi_var  # noqa: E501
    e0_F_s5 = m.varlist_all["e0_F_s5"].casadi_var  # noqa: E501

    EQ_alg1 = 0.0 - ((e0_F_s1 - e0_F_s2))  # noqa: E501,E226
    EQ_alg2 = 0.0 - (((e0_F_s2 - e0_F_s3) - e0_F_s4))  # noqa: E501,E226
    EQ_alg3 = 0.0 - (((e0_F_s2 - e0_F_s5)))  # noqa: E501,E226

    list_algebraic_equations = [EQ_alg1, EQ_alg2, EQ_alg3]  # noqa: E501

    m.add_equations_algebraic(list_algebraic_equations)

    return variable_list, m


def isomerization_model() -> tuple[
    mopeds.VariableList, mopeds.Model, list[mopeds.VariableList]
]:
    # Isomerization data as used in Bates, Watts, Nonlinear regression analysis: Its applications
    variable_list = mopeds.variables.VariableList()  # Preallocate variable_list

    variable_list.add_variable(mopeds.VariableAlgebraic("f", 8.3))
    variable_list.add_variable(mopeds.VariableControl("x1", 1))
    variable_list.add_variable(mopeds.VariableControl("x2", 1))
    variable_list.add_variable(mopeds.VariableControl("x3", 1))
    variable_list.add_variable(mopeds.VariableParameter("theta1", 35.92))
    variable_list.add_variable(mopeds.VariableParameter("theta2", 0.0708))
    variable_list.add_variable(mopeds.VariableParameter("theta3", 0.0377))
    variable_list.add_variable(mopeds.VariableParameter("theta4", 0.167))

    m = mopeds.Model(variable_list)  # adding all variables to the model

    f = m.varlist_all["f"].casadi_var  # noqa: E501
    x1 = m.varlist_all["x1"].casadi_var  # noqa: E501
    x2 = m.varlist_all["x2"].casadi_var  # noqa: E501
    x3 = m.varlist_all["x3"].casadi_var  # noqa: E501
    theta1 = m.varlist_all["theta1"].casadi_var  # noqa: E501
    theta2 = m.varlist_all["theta2"].casadi_var  # noqa: E501
    theta3 = m.varlist_all["theta3"].casadi_var  # noqa: E501
    theta4 = m.varlist_all["theta4"].casadi_var  # noqa: E501

    equation = f - (theta1 * theta3 * (x2 - x3 / 1.632)) / (
        1 + theta2 * x1 + theta3 * x2 + theta4 * x3
    )
    # Equations
    m.add_equations_algebraic([equation])  # adding the equations to model

    data = [
        [205.8, 90.9, 37.1, 3.541],
        [404.8, 92.9, 36.3, 2.397],
        [209.7, 174.9, 49.4, 6.694],
        [401.6, 187.2, 44.9, 4.722],
        [224.9, 92.7, 116.3, 0.593],
        [402.6, 102.2, 128.9, 0.268],
        [212.7, 186.9, 134.4, 2.797],
        [406.2, 192.6, 134.9, 2.451],
        [133.3, 140.8, 87.6, 3.196],
        [470.9, 144.2, 86.9, 2.021],
        [300.0, 68.3, 81.7, 0.896],
        [301.6, 214.6, 101.7, 5.084],
        [297.3, 142.2, 10.5, 5.686],
        [314.0, 146.7, 157.1, 1.193],
        [305.7, 142.0, 86.0, 2.648],
        [300.1, 143.7, 90.2, 3.303],
        [305.4, 141.1, 87.4, 3.054],
        [305.2, 141.5, 87.0, 3.302],
        [300.1, 83.0, 66.4, 1.271],
        [106.6, 209.6, 33.0, 11.648],
        [417.2, 83.9, 32.9, 2.002],
        [251.0, 294.4, 41.5, 9.604],
        [250.3, 148.0, 14.7, 7.754],
        [145.1, 291.0, 50.2, 11.590],
    ]

    exp_data = []

    for x1_i, x2_i, x3_i, f_i in data:
        var_list = copy.deepcopy(variable_list)
        var_list["f"].value = f_i
        var_list["x1"].value = x1_i
        var_list["x2"].value = x2_i
        var_list["x3"].value = x3_i
        var_list["theta1"].fixed = False
        var_list["theta2"].fixed = False
        var_list["theta3"].fixed = False
        var_list["theta4"].fixed = False
        var_list.set_bounds()
        exp_data.append(var_list)

    return variable_list, m, exp_data


def free_fall_example() -> tuple[
    mopeds.VariableList, mopeds.Model, list[mopeds.VariableList]
]:
    # Isomerization data as used in Bates, Watts, Nonlinear regression analysis: Its applications
    variable_list = mopeds.variables.VariableList()  # Preallocate variable_list

    variable_list.add_variable(mopeds.VariableState("s", 0))
    variable_list.add_variable(mopeds.VariableState("v", 0))

    variable_list.add_variable(mopeds.VariableAlgebraic("a", 8.8))
    variable_list.add_variable(mopeds.VariableAlgebraic("d", 1))
    variable_list.add_variable(mopeds.VariableAlgebraic("a_i", 0))

    variable_list.add_variable(mopeds.VariableParameter("g", 9.8))
    variable_list.add_variable(mopeds.VariableParameter("k1", 1))
    variable_list.add_variable(mopeds.VariableParameter("k2", 1.1))
    variable_list.add_variable(mopeds.VariableParameter("k3", 1.0))

    m = mopeds.Model(variable_list)  # adding all variables to the model

    s = m.varlist_all["s"].casadi_var  # noqa: E501
    v = m.varlist_all["v"].casadi_var  # noqa: E501
    a = m.varlist_all["a"].casadi_var  # noqa: E501
    d = m.varlist_all["d"].casadi_var  # noqa: E501
    a_i = m.varlist_all["a_i"].casadi_var  # noqa: E501
    g = m.varlist_all["g"].casadi_var  # noqa: E501
    k1 = m.varlist_all["k1"].casadi_var  # noqa: E501
    k2 = m.varlist_all["k2"].casadi_var  # noqa: E501
    k3 = m.varlist_all["k3"].casadi_var  # noqa: E501

    eq1 = v
    eq2 = a

    eq3 = a - (g - d - a_i)
    eq4 = d - k1
    eq5 = a_i - s * (k2 - k3)

    m.add_equations_differential([eq1, eq2])  # adding the equations to model
    m.add_equations_algebraic([eq3, eq4, eq5])  # adding the equations to model
    variable_list["a"].ignore_plotting = False
    variable_list["a_i"].ignore_plotting = False

    time = [0.0, 7.5, 15.0, 22.5, 30.0]
    data = [
        [0.0, 151.1831578, 85.26994645, 28.73744369, 175.83004085],
    ]

    exp_data = []
    for s_v in data:
        var_list = copy.deepcopy(variable_list)
        var_list["s"].set_dataframe_from_value_and_time(s_v, time)
        var_list["s"].variance = 0.1
        var_list["g"].lower_bound = 1
        var_list["g"].upper_bound = 100
        var_list["g"].guess = 39
        var_list["g"].fixed = False
        exp_data.append(var_list)

    return variable_list, m, exp_data

def spmma() -> tuple[
    mopeds.VariableList, mopeds.Model, list[mopeds.VariableList]
]:
    # s-PMMA data as used in Bates, Watts, Nonlinear regression analysis: Its applications
    variable_list = mopeds.variables.VariableList()  # Preallocate variable_list

    variable_list.add_variable(mopeds.VariableAlgebraic("e1", 4.22))
    variable_list.add_variable(mopeds.VariableAlgebraic("e2", 0.136))

    variable_list.add_variable(mopeds.VariableControl("f", 30))

    variable_list.add_variable(mopeds.VariableParameter("eps0", 4.32))
    variable_list.add_variable(mopeds.VariableParameter("epsinf", 2.522))
    variable_list.add_variable(mopeds.VariableParameter("lnf0", 7.956))
    variable_list.add_variable(mopeds.VariableParameter("alpha", 0.531))
    variable_list.add_variable(mopeds.VariableParameter("beta", 0.554))

    m = mopeds.Model(variable_list)  # adding all variables to the model

    e1 = m.varlist_all["e1"].casadi_var  # noqa: E501
    e2 = m.varlist_all["e2"].casadi_var  # noqa: E501
    f = m.varlist_all["f"].casadi_var  # noqa: E501
    eps0 = m.varlist_all["eps0"].casadi_var  # noqa: E501
    epsinf = m.varlist_all["epsinf"].casadi_var  # noqa: E501
    lnf0 = m.varlist_all["lnf0"].casadi_var  # noqa: E501
    alpha = m.varlist_all["alpha"].casadi_var  # noqa: E501
    beta = m.varlist_all["beta"].casadi_var  # noqa: E501
    f0 = ca.exp(lnf0)

    pi = 3.14

    zz = (2*pi*f/f0)**alpha

    r = ca.sqrt((1+zz*ca.cos(pi*alpha/2))**2 + (zz*ca.sin(pi*alpha/2))**2)
    fau = ca.arctan((zz*ca.sin(pi*alpha/2))/(1 + zz*ca.cos(pi*alpha/2)))

    eq1 = e1 - (epsinf + (eps0 - epsinf) * r**-beta * ca.cos(beta*fau))
    eq2 = e2 - ((eps0 - epsinf) * r**-beta * ca.sin(beta*fau))

    # Equations
    m.add_equations_algebraic([eq1, eq2])  # adding the equations to model

    data = [
        [30, 4.22, 0.136],
        [50, 4.167, 0.167],
        [70, 4.132, 0.188],
        [100, 4.038, 0.212],
        [150, 4.019, 0.236],
        [200, 3.956, 0.257],
        [300, 3.884, 0.276],
        [500, 3.784, 0.297],
        [700, 3.713, 0.309],
        [1000, 3.633, 0.311],
        [1500, 3.54, 0.314],
        [2000, 3.433, 0.311],
        [3000, 3.358, 0.305],
        [5000, 3.258, 0.289],
        [7000, 3.193, 0.277],
        [10000, 3.128, 0.255],
        [15000, 3.059, 0.24],
        [20000, 2.984, 0.218],
        [30000, 2.934, 0.202],
        [50000, 2.876, 0.182],
        [70000, 2.838, 0.168],
        [100000, 2.798, 0.153],
        [150000, 2.759, 0.139],
    ]

    exp_data = []

    for f_i, e1_i, e2_i in data:
        var_list = copy.deepcopy(variable_list)
        var_list["f"].value = f_i
        var_list["e1"].value = e1_i
        var_list["e2"].value = e2_i

        var_list["eps0"].fixed = False
        var_list["epsinf"].fixed = False
        var_list["lnf0"].fixed = False
        var_list["alpha"].fixed = False
        var_list["beta"].fixed = False

        var_list.set_bounds()
        exp_data.append(var_list)

    return variable_list, m, exp_data


# Baker yeast growth model Quaglio2018 10.1016/j.cherd.2018.04.041
def yeast_growth(model_type="cantois", piecewise=False, *, ode=False, normalize=False, u1_piecewise_linear=False) -> tuple[
    mopeds.VariableList, mopeds.Model, list[mopeds.VariableList]
]:
    variable_list = mopeds.variables.VariableList()

    variable_list.add_variable(mopeds.VariableState("x1", 5, 0, 10))
    variable_list.add_variable(mopeds.VariableState("x2", 0.01))

    if u1_piecewise_linear:
        variable_list.add_variable(mopeds.VariableState("u1_dot", 0))

    if ode is False:
        variable_list.add_variable(mopeds.VariableAlgebraic("r", 1.7))

    if piecewise:
        variable_list.add_variable(mopeds.VariableControlPiecewiseConstant("u1", 0.125, 0.05, 0.2))
        variable_list.add_variable(mopeds.VariableControlPiecewiseConstant("u2", 35, 5, 35))
    else:
        variable_list.add_variable(mopeds.VariableControl("u1", 0.125, 0.05, 0.2))
        variable_list.add_variable(mopeds.VariableControl("u2", 35, 5, 35))

    variable_list.add_variable(mopeds.VariableParameter("theta1", 0.310, 1e-2, 2))
    variable_list.add_variable(mopeds.VariableParameter("theta2", 0.180, 1e-2, 20))
    variable_list.add_variable(mopeds.VariableParameter("theta3", 0.550, 1e-2, 2))
    variable_list.add_variable(mopeds.VariableParameter("theta4", 0.050, 1e-2, 2))

    if normalize:
        for varname in ["theta1", "theta2", "theta3", "theta4"]:
            variable_list[varname].value = 1
            variable_list[varname].lower_bound = 1e-2
            variable_list[varname].upper_bound = 10

    variable_list["x1"].variance = 0.01
    variable_list["x2"].variance = 0.05

    m = mopeds.Model(variable_list)  # adding all variables to the model

    x1 = m.varlist_all["x1"].casadi_var  # noqa: E501
    x2 = m.varlist_all["x2"].casadi_var  # noqa: E501

    if ode is False:
        r = m.varlist_all["r"].casadi_var  # noqa: E501

    if u1_piecewise_linear:
        u1 = m.varlist_all["u1_dot"].casadi_var  # noqa: E501
        u1_gradient = m.varlist_all["u1"].casadi_var  # noqa: E501
    else:
        u1 = m.varlist_all["u1"].casadi_var  # noqa: E501

    u2 = m.varlist_all["u2"].casadi_var  # noqa: E501

    theta1 = m.varlist_all["theta1"].casadi_var  # noqa: E501
    theta2 = m.varlist_all["theta2"].casadi_var  # noqa: E501
    theta3 = m.varlist_all["theta3"].casadi_var  # noqa: E501
    theta4 = m.varlist_all["theta4"].casadi_var  # noqa0: E501

    if normalize:
        theta1_norm = theta1 * 0.310
        theta2_norm = theta2 * 0.180
        theta3_norm = theta3 * 0.55
        theta4_norm = theta4 * 0.05
    else:
        theta1_norm = theta1
        theta2_norm = theta2
        theta3_norm = theta3
        theta4_norm = theta4

    if model_type == "cantois":
        r_eq = ((theta1_norm * x2) / (theta2_norm * x1 + x2))
    elif model_type == "monod":
        r_eq = (theta1_norm * x2 / (theta2_norm + x2))
    else:
        raise NotImplementedError

    if ode is False:
        eq_alg1 = r - r_eq
    else:
        r = r_eq

    eq1 = (r - u1 - theta4_norm)  * x1
    eq2 = - (r * x1 / theta3_norm) + u1 * (u2 - x2)

    diff_eq = [eq1, eq2]

    if u1_piecewise_linear:
        diff_eq.append(u1_gradient)

    m.add_equations_differential(diff_eq)

    if ode is False:
        m.add_equations_algebraic([eq_alg1])

    data = [
        [5, 7.098, 10.135, 12.108, 12.491],
        [0.01, 6.683, 5.860, 3.209, 2.993]
    ]

    exp_data = []

    x1_i, x2_i = data

    time_grid = [0, 5, 10, 15, 20]

    var_list = copy.deepcopy(variable_list)
    var_list["x1"].set_dataframe_from_value_and_time(x1_i, time_grid)
    var_list["x2"].set_dataframe_from_value_and_time(x2_i, time_grid)

    var_list["theta1"].fixed = False
    var_list["theta2"].fixed = False
    var_list["theta3"].fixed = False
    var_list["theta4"].fixed = False

    exp_data.append(var_list)

    return variable_list, m, exp_data

# Pankajakshan2019
def esterification_BA() -> tuple[
    mopeds.VariableList, mopeds.Model, list[mopeds.VariableList]
]:
    variable_list = mopeds.variables.VariableList()  # Preallocate variable_list

    variable_list.add_variable(mopeds.VariableState("Cba", 1, 0.9, 1.55))
    variable_list.add_variable(mopeds.VariableState("Ce", 4.22))
    variable_list.add_variable(mopeds.VariableState("Ce", 0))
    variable_list.add_variable(mopeds.VariableState("Cw", 0))

    variable_list.add_variable(mopeds.VariableControl("F", 10, 7.5, 30))
    variable_list.add_variable(mopeds.VariableControl("T", 350, 343, 413))

    variable_list.add_variable(mopeds.VariableParameter("theta1", 4.32))
    variable_list.add_variable(mopeds.VariableParameter("theta2", 2.522))

    m = mopeds.Model(variable_list)  # adding all variables to the model

    D = 0.250  # micrometer

    Cba = m.varlist_all["Cba"].casadi_var  # noqa: E501
    F = m.varlist_all["F"].casadi_var  # noqa: E501
    T = m.varlist_all["T"].casadi_var  # noqa: E501
    theta1 = m.varlist_all["theta1"].casadi_var  # noqa: E501
    theta2 = m.varlist_all["theta2"].casadi_var  # noqa: E501

    R = 8.314
    k = ca.exp(theta1 - 10e4 * theta2 / (R * T))
    A_cs = 3.14 * (D * 1e-6) **2 / 4
    v = F / A_cs

    eq1 = (-1 * k * Cba) / v
    eq2 = (-1 * k * Cba) / v
    eq3 = (1 * k * Cba) / v
    eq4 = (1 * k * Cba) / v

    # Equations
    m.add_equations_differential([eq1, eq2, eq3, eq4])  # adding the equations to model

    return variable_list, m

def cstr_nle():
    variable_list = mopeds.VariableList()
    # fmt:off


    variable_list.add_variable(mopeds.VariableAlgebraic("e0_X_c1", 0.8866276885, 0.0, 1.0E9))  # noqa: E501
    variable_list.add_variable(mopeds.VariableAlgebraic("e0_c_c1", 1.376664E-4, 0.0, 1.0E9))  # noqa: E501
    variable_list.add_variable(mopeds.VariableAlgebraic("e0_k", 11.7307437323, -1.0E9, 1.0E9))  # noqa: E501
    variable_list.add_variable(mopeds.VariableAlgebraic("e0_T", 704.755540977, -1.0E9, 1.0E9))  # noqa: E501
    variable_list.add_variable(mopeds.VariableAlgebraic("e0_c_Feed_c1", 0.0012142857, 0.0, 1.0E9))  # noqa: E501

    variable_list.add_variable(mopeds.VariableControl("e0_Q_Feed", 30.0, 28, 32))  # noqa: E501
    variable_list.add_variable(mopeds.VariableControl("e0_x_Feed_c1", 0.3, -1.0E9, 1.0E9))  # noqa: E501
    variable_list.add_variable(mopeds.VariableControl("e0_m_Cat", 20.0, 18, 22))  # noqa: E501
    variable_list.add_variable(mopeds.VariableControl("e0_T_Feed", 560.0, -1.0E9, 1.0E9))  # noqa: E501

    variable_list.add_variable(mopeds.VariableParameter("e0_cp", 1.75, -1.0E9, 1.0E9))  # noqa: E501
    variable_list.add_variable(mopeds.VariableParameter("e0_E", 135518.2, -1.0E9, 1.0E9))  # noqa: E501
    variable_list.add_variable(mopeds.VariableParameter("e0_greek_DeltaHR", -200000.0, -1.0E9, 1.0E9))  # noqa: E501

    variable_list.add_variable(mopeds.VariableConstant("e0_M_c1", 210.0))  # noqa: E501
    variable_list.add_variable(mopeds.VariableConstant("e0_greek_rho", 0.85))  # noqa: E501
    variable_list.add_variable(mopeds.VariableConstant("e0_R", 8.314))  # noqa: E501


    m = mopeds.Model(variable_list)

    e0_Q_Feed = m.varlist_all["e0_Q_Feed"].casadi_var  # noqa: E501
    e0_M_c1 = m.varlist_all["e0_M_c1"].casadi_var  # noqa: E501
    e0_x_Feed_c1 = m.varlist_all["e0_x_Feed_c1"].casadi_var  # noqa: E501
    e0_E = m.varlist_all["e0_E"].casadi_var  # noqa: E501
    e0_R = m.varlist_all["e0_R"].casadi_var  # noqa: E501
    e0_m_Cat = m.varlist_all["e0_m_Cat"].casadi_var  # noqa: E501
    e0_greek_DeltaHR = m.varlist_all["e0_greek_DeltaHR"].casadi_var  # noqa: E501
    e0_greek_rho = m.varlist_all["e0_greek_rho"].casadi_var  # noqa: E501
    e0_T_Feed = m.varlist_all["e0_T_Feed"].casadi_var  # noqa: E501
    e0_cp = m.varlist_all["e0_cp"].casadi_var  # noqa: E501
    e0_X_c1 = m.varlist_all["e0_X_c1"].casadi_var  # noqa: E501
    e0_c_c1 = m.varlist_all["e0_c_c1"].casadi_var  # noqa: E501
    e0_k = m.varlist_all["e0_k"].casadi_var  # noqa: E501
    e0_T = m.varlist_all["e0_T"].casadi_var  # noqa: E501
    e0_c_Feed_c1 = m.varlist_all["e0_c_Feed_c1"].casadi_var  # noqa: E501

    EQ_alg1 = (e0_Q_Feed-(((((1.0/e0_X_c1)-1.0))*(e0_m_Cat*e0_k))))  # noqa: E501,E226
    EQ_alg2 = (((e0_T-e0_T_Feed)/e0_X_c1)-(((-(e0_greek_DeltaHR*e0_c_Feed_c1))/(e0_greek_rho*e0_cp))))  # noqa: E501,E226
    EQ_alg3 = (e0_c_Feed_c1-((e0_x_Feed_c1*(e0_greek_rho/e0_M_c1))))  # noqa: E501,E226
    EQ_alg4 = (e0_X_c1-(((e0_c_Feed_c1-e0_c_c1)/e0_c_Feed_c1)))  # noqa: E501,E226
    EQ_alg5 = (e0_k-((1.3*(((10.0))**(1.0*11.0)*ca.exp(((-e0_E)/(e0_R*e0_T)))))))  # noqa: E501,E226

    list_algebraic_equations = [EQ_alg1, EQ_alg2, EQ_alg3, EQ_alg4, EQ_alg5, ]  # noqa: E501

    # fmt:on

    m.add_equations_algebraic(list_algebraic_equations)

    return variable_list, m

# Copyright Jonathan Frey, Jochem De Schutter, Moritz Diehl

# The 2-Clause BSD License

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


# The original code is modified by Volodymyr Kozachynskyi, adding:
# - changes to API
# - support for DAE systems

from casadi import Callback, Sparsity, Function
import casadi
from acados_template import AcadosSimSolver, AcadosSim, casadi_length
import numpy as np
import copy
from pathlib import Path


def create_casados_integrator(model, integrator_opts, DAE=True):
    sim = AcadosSim()
    options = list(filter(lambda name: name[0] != "_", dir(sim.solver_options)))

    sim.solver_options.T = 1
    sim.solver_options.sens_forw = True
    sim.solver_options.sens_hess = True
    sim.solver_options.sens_adj = True

    if DAE:
        sim.solver_options.sens_algebraic = True
        sim.solver_options.output_z = True

    for key, value in integrator_opts["acados"].items():
        if key in options:
            setattr(sim.solver_options, key, value)
        else:
            if key != "code_reuse":
                print(f"Option {key} was ignored")

    code_reuse = integrator_opts["acados"].get("code_reuse", False)

    sim.model = model

    dir_path = Path.cwd() / "modeps_code"
    sim.code_export_directory = str(
        dir_path / f"c_generated_code_{model.name}_{sim.solver_options.integrator_type}"
    )

    if DAE:
        casados_integrator = CasadosIntegratorDAE(
            sim, integrator_opts, use_cython=False, code_reuse=code_reuse
        )
    else:
        casados_integrator = CasadosIntegrator(
            sim, integrator_opts, use_cython=False, code_reuse=code_reuse
        )

    return casados_integrator


class CasadosIntegrator(Callback):
    """
    This class is a wrapper of the acados integrator (AcadosSimSolver) into a CasADi Callback.
    It offers:
        - first order forward sensitivities (via get_jacobian())
        - first order adjoint sensitivities (via get_reverse())
        - second order sensitivities (hessians) with adjoint seed (via get_reverse() + get_jacobian()) (for acados integrators that offer second order senitivities)
    This makes it fully functional within CasADi NLPs
    """

    def __init__(
        self, acados_sim: AcadosSim, settings, use_cython=True, code_reuse=False
    ):
        dir_path = Path(acados_sim.code_export_directory).parent
        json_file = str(dir_path / f"acados_sim_{acados_sim.model.name}.json")
        if use_cython:
            if not code_reuse:
                AcadosSimSolver.generate(acados_sim, json_file=json_file)
                AcadosSimSolver.build(
                    acados_sim.code_export_directory, with_cython=True
                )
            self.acados_integrator = AcadosSimSolver.create_cython_solver(json_file)
        else:
            if code_reuse:
                self.acados_integrator = AcadosSimSolver(
                    acados_sim, json_file, generate=False, build=False
                )
            else:
                self.acados_integrator = AcadosSimSolver(
                    acados_sim, json_file, generate=True, build=True
                )

        self.settings = copy.deepcopy(settings)
        self.settings.pop("acados")

        self.nx = casadi_length(acados_sim.model.x)
        self.nu = casadi_length(acados_sim.model.u)
        self.model_name = acados_sim.model.name

        self.x0 = None
        self.u0 = None

        # needed to keep the callback alive
        self.jac_callback = None
        self.adj_callback = None
        self.hess_callback = None

        self.reset_timings()

        Callback.__init__(self)
        name = type(self).__name__
        self.construct(name, self.settings)

    def get_sparsity_in(self, i):
        if i == 0:
            out = Sparsity.dense(self.nx)
        elif i == 1:
            out = Sparsity.dense(self.nu)
        return out

    def get_sparsity_out(self, i):
        out = Sparsity.dense(self.nx)
        return out

    def get_name_in(self, i):
        if i == 0:
            out = "x0"
        elif i == 1:
            out = "p"
        return out

    def get_n_in(self):
        return 2

    def get_n_out(self):
        return 1

    def get_name_out(self, i):
        return "xf"

    def eval(self, arg):
        # extract inputs
        x0 = np.array(arg[0])
        u0 = np.array(arg[1])

        self.acados_integrator.options_set("sens_forw", False)
        self.acados_integrator.options_set("sens_adj", False)
        self.acados_integrator.options_set("sens_hess", False)
        # set
        self.acados_integrator.set("x", x0)
        self.acados_integrator.set("u", u0)
        # solve
        status = self.acados_integrator.solve()

        # output
        x_next = self.acados_integrator.get("x")

        self.time_sim += self.acados_integrator.get("time_tot")

        return [x_next]

    def has_jacobian(self, *args) -> bool:
        return True

    def get_jacobian(self, *args):

        sens_callback = CasadosIntegratorSensForw(self)

        nominal_in = self.mx_in()
        nominal_out = self.mx_out()

        jac_fun = Function(
            f"CasadosIntegratorSensForw_{self.model_name}",
            nominal_in + nominal_out,
            sens_callback.call(nominal_in),
        )

        return jac_fun

    def has_reverse(self, nadj) -> bool:
        if nadj == 1:
            return True
        else:
            return False

    def get_reverse(self, *args) -> "casadi::Function":
        # def get_reverse(self, nadj, name, inames, onames, opts) -> "casadi::Function":

        if self.adj_callback is None:
            self.adj_callback = CasadosIntegratorSensAdj(self)

        return self.adj_callback

    def reset_timings(self):
        self.time_sim = 0.0
        self.time_forw = 0.0
        self.time_adj = 0.0
        self.time_hess = 0.0


# NOTE: doesnt even get called -> dead end -> see https://github.com/casadi/casadi/issues/2019
# def uses_output(self, *args) -> bool:
#     r"""
#     uses_output(Function self) -> bool
#     Do the derivative functions need nondifferentiated outputs?
#     """
#     print("in uses_output()\n\n")
#     return False


# JACOBIAN
class CasadosIntegratorSensForw(Callback):
    def __init__(self, casados_integrator):
        self.acados_integrator = casados_integrator.acados_integrator
        self.casados_integrator = casados_integrator

        self.nx = self.casados_integrator.nx
        self.nu = self.casados_integrator.nu

        Callback.__init__(self)
        name = type(self).__name__
        self.construct(name, casados_integrator.settings)
        casados_integrator.jac_callback = self

    def get_sparsity_in(self, i):
        if i == 0:
            out = Sparsity.dense(self.nx)
        elif i == 1:
            out = Sparsity.dense(self.nu)
        return out

    def get_sparsity_out(self, i):
        out = Sparsity.dense(self.nx, self.nx + self.nu)
        return out

    def get_name_in(self, i):
        if i == 0:
            out = "x0"
        elif i == 1:
            out = "u0"
        return out

    def get_n_in(self):
        return 2

    def get_name_out(self, i):
        return "S_forw"

    def eval(self, arg):
        # extract inputs
        x0 = np.array(arg[0])
        u0 = np.array(arg[1])

        # set
        self.acados_integrator.set("x", x0)
        self.acados_integrator.set("u", u0)
        self.acados_integrator.options_set("sens_forw", True)
        self.acados_integrator.options_set("sens_adj", False)
        self.acados_integrator.options_set("sens_hess", False)
        # solve
        status = self.acados_integrator.solve()

        # output
        S_forw = self.acados_integrator.get("S_forw")
        # S_forw = np.ascontiguousarray(S_forw.reshape(S_forw.shape, order="F"))
        self.casados_integrator.time_forw += self.acados_integrator.get("time_tot")

        return [S_forw]

    def has_jacobian(self, *args) -> bool:
        return False

    def has_reverse(self, nadj) -> bool:
        # print(f"CasadosIntegratorSensForw: has_reverse, nadj: {nadj}\n")
        return False


# Citing casadi docstrings:
# Get a function that calculates nadj adjoint derivatives.

# Returns a function with n_in + n_out + n_out inputs and n_in outputs.
# The first n_in inputs correspond to nondifferentiated inputs.
# The next n_out inputs correspond to nondifferentiated outputs.
# The last n_out inputs correspond to adjoint seeds, stacked horizontally

# The n_in outputs correspond to adjoint sensitivities, stacked horizontally.
# (n_in = n_in(),
# n_out = n_out())

# (n_in = n_in(), n_out = n_out())

# ADJOINT
class CasadosIntegratorSensAdj(Callback):
    def __init__(self, casados_integrator):
        self.acados_integrator = casados_integrator.acados_integrator
        self.casados_integrator = casados_integrator

        self.nx = casados_integrator.nx
        self.nu = casados_integrator.nu

        Callback.__init__(self)
        name = type(self).__name__
        self.construct(name, casados_integrator.settings)

    def get_sparsity_in(self, i):
        if i == 0:
            out = Sparsity.dense(self.nx, 1)
        elif i == 1:
            out = Sparsity.dense(self.nu, 1)
        elif i == 2:
            out = Sparsity(self.nx, 1)
        elif i == 3:
            out = Sparsity.dense(self.nx, 1)
        return out

    def get_sparsity_out(self, i):
        if i == 0:
            out = Sparsity.dense(self.nx)
        elif i == 1:
            out = Sparsity.dense(self.nu)
        return out

    def get_name_in(self, i):
        if i == 0:
            out = "x0"
        elif i == 1:
            out = "u0"
        elif i == 2:
            out = "nominal_out"
        elif i == 3:
            out = "adj_seed"
        return out

    def get_n_in(self):
        return 4

    def get_n_out(self):
        return 2

    def get_name_out(self, i):
        return "S_adj"

    def eval(self, arg):
        # extract inputs
        x0 = np.array(arg[0])
        u0 = np.array(arg[1])
        seed = np.array(arg[3])

        # set adj seed:
        self.acados_integrator.set("seed_adj", seed)
        # set input
        self.acados_integrator.set("x", x0)
        self.acados_integrator.set("u", u0)

        # solve
        self.acados_integrator.options_set("sens_adj", True)
        self.acados_integrator.options_set("sens_forw", False)
        self.acados_integrator.options_set("sens_hess", False)
        status = self.acados_integrator.solve()

        # output
        S_adj = self.acados_integrator.get("S_adj")

        S_adj_x = S_adj[: self.nx]
        S_adj_u = S_adj[self.nx :]

        self.casados_integrator.time_adj += self.acados_integrator.get("time_tot")

        return [S_adj_x, S_adj_u]

    def has_jacobian(self, *args) -> bool:
        return True

    def get_jacobian(self, *args):

        if self.casados_integrator.hess_callback is None:
            self.casados_integrator.hess_callback = CasadosIntegratorSensHess(
                self.casados_integrator
            )

        return self.casados_integrator.hess_callback


# HESSIAN
class CasadosIntegratorSensHess(Callback):
    def __init__(self, casados_integrator):
        self.acados_integrator = casados_integrator.acados_integrator
        self.casados_integrator = casados_integrator

        self.nx = casados_integrator.nx
        self.nu = casados_integrator.nu

        Callback.__init__(self)
        name = type(self).__name__
        self.construct(name, casados_integrator.settings)

    def get_sparsity_in(self, i):
        if i == 0:
            out = Sparsity.dense(self.nx, 1)
        elif i == 1:
            out = Sparsity.dense(self.nu, 1)
        elif i == 2:
            out = Sparsity(self.nx, 1)
        elif i == 3:
            out = Sparsity.dense(self.nx, 1)
        elif i == 4:
            out = Sparsity.dense(self.nx, 1)
        elif i == 5:
            out = Sparsity.dense(self.nu, 1)
        return out

    def get_sparsity_out(self, i):
        out = Sparsity.dense(self.nx + self.nu, 3 * self.nx + self.nu)
        return out

    def get_name_in(self, i):
        if i == 0:
            out = "x0"
        elif i == 1:
            out = "u0"
        elif i == 2:
            out = "nominal_out"
        elif i == 3:
            out = "adj_seed"
        elif i == 4:
            out = "S_adj_out_x"
        elif i == 5:
            out = "S_adj_out_u"
        return out

    def get_n_in(self):
        return 6

    def get_n_out(self):
        return 1

    def get_name_out(self, i):
        return "S_hess"

    def eval(self, arg):
        # extract inputs
        x0 = np.array(arg[0])
        seed = np.array(arg[3])
        u0 = np.array(arg[1])

        # set adj seed:
        self.acados_integrator.set("seed_adj", seed)
        # set input
        self.acados_integrator.set("x", x0)
        self.acados_integrator.set("u", u0)

        # solve
        self.acados_integrator.options_set("sens_hess", True)
        self.acados_integrator.options_set("sens_forw", True)
        self.acados_integrator.options_set("sens_adj", True)
        status = self.acados_integrator.solve()

        # output
        S_hess = self.acados_integrator.get("S_hess")
        S_forw = self.acados_integrator.get("S_forw")

        # NOTE: casadi expects jacobian(S_adj, [x, u, nominal_out, seed_adj])
        #                            = [S_hess(for x,u), zeros(nx+nu, nx), S_forw ]
        out = np.concatenate(
            [S_hess, np.zeros((self.nx + self.nu, self.nx)), S_forw.T], axis=1
        )

        self.casados_integrator.time_hess += self.acados_integrator.get("time_tot")

        return [out]

    def has_jacobian(self, *args) -> bool:
        return False


class CasadosIntegratorDAE(CasadosIntegrator):
    def __init__(
        self, acados_sim: AcadosSim, settings, use_cython=True, code_reuse=False
    ):
        self.nz = casadi_length(acados_sim.model.z)
        self.z0 = None

        super().__init__(acados_sim, settings, use_cython, code_reuse)

    def get_sparsity_in(self, i):
        if i == 0:
            out = Sparsity.dense(self.nx)
        elif i == 1:
            out = Sparsity.dense(self.nu)
        elif i == 2:
            out = Sparsity.dense(self.nz)
        return out

    def get_sparsity_out(self, i):
        if i == 0:
            out = Sparsity.dense(self.nx)
        elif i == 1:
            out = Sparsity.dense(self.nz)
        return out

    def get_name_in(self, i):
        if i == 0:
            out = "x0"
        elif i == 1:
            out = "p"
        elif i == 2:
            out = "z0"
        return out

    def get_n_in(self):
        return 3

    def get_n_out(self):
        return 2

    def get_name_out(self, i):
        if i == 0:
            out = "xf"
        elif i == 1:
            out = "zf"
        return out

    def eval(self, arg):
        # extract inputs
        x0 = np.array(arg[0])
        u0 = np.array(arg[1])
        z0 = np.array(arg[2])

        self.acados_integrator.options_set("sens_forw", False)
        self.acados_integrator.options_set("sens_adj", False)
        self.acados_integrator.options_set("sens_hess", False)
        # set
        self.acados_integrator.set("x", x0)
        self.acados_integrator.set("u", u0)
        self.acados_integrator.set("z", z0)
        # solve
        status = self.acados_integrator.solve()

        # output
        x_next = self.acados_integrator.get("x")
        z_next = self.acados_integrator.get("z")

        self.time_sim += self.acados_integrator.get("time_tot")

        return [x_next, z_next]

    def get_jacobian(self, *args):
        sens_callback = CasadosIntegratorSensForwDAE(self)

        nominal_in = self.mx_in()
        nominal_out = self.mx_out()

        jac_fun = Function(
            f"CasadosIntegratorSensForwDAE_{self.model_name}",
            nominal_in + nominal_out,
            sens_callback.call(nominal_in),
        )

        return jac_fun

    def get_reverse(self, *args) -> "casadi::Function":
        # def get_reverse(self, nadj, name, inames, onames, opts) -> "casadi::Function":

        if self.adj_callback is None:
            self.adj_callback = CasadosIntegratorSensAdjDAE(self)

        return self.adj_callback


# NOTE: doesnt even get called -> dead end -> see https://github.com/casadi/casadi/issues/2019
# def uses_output(self, *args) -> bool:
#     r"""
#     uses_output(Function self) -> bool
#     Do the derivative functions need nondifferentiated outputs?
#     """
#     print("in uses_output()\n\n")
#     return False


# JACOBIAN
class CasadosIntegratorSensForwDAE(CasadosIntegratorSensForw):
    def __init__(self, casados_integrator):
        self.nz = casados_integrator.nz
        super().__init__(casados_integrator)

    def get_sparsity_in(self, i):
        if i == 0:
            out = Sparsity.dense(self.nx)
        elif i == 1:
            out = Sparsity.dense(self.nu)
        elif i == 2:
            out = Sparsity.dense(self.nz)
        return out

    def get_sparsity_out(self, i):
        out = Sparsity.dense(self.nx + self.nz, self.nx + self.nu + self.nz)
        return out

    def get_name_in(self, i):
        if i == 0:
            out = "x0"
        elif i == 1:
            out = "u0"
        elif i == 2:
            out = "z0"
        return out

    def get_n_in(self):
        return 3

    def eval(self, arg):
        # extract inputs
        x0 = np.array(arg[0])
        u0 = np.array(arg[1])
        z0 = np.array(arg[2])

        # set
        self.acados_integrator.set("x", x0)
        self.acados_integrator.set("u", u0)
        self.acados_integrator.set("z", z0)
        self.acados_integrator.options_set("sens_forw", True)
        self.acados_integrator.options_set("sens_adj", False)
        self.acados_integrator.options_set("sens_hess", False)
        # solve
        status = self.acados_integrator.solve()

        # output
        S_forw = self.acados_integrator.get("S_forw")
        row1 = np.concatenate([S_forw, np.zeros((self.nx, self.nz))], axis=1)
        out = np.concatenate([row1, np.zeros((self.nz, self.nx + self.nu + self.nz))])
        # S_forw = np.ascontiguousarray(S_forw.reshape(S_forw.shape, order="F"))
        self.casados_integrator.time_forw += self.acados_integrator.get("time_tot")

        return [out]


# Citing casadi docstrings:
# Get a function that calculates nadj adjoint derivatives.

# Returns a function with n_in + n_out + n_out inputs and n_in outputs.
# The first n_in inputs correspond to nondifferentiated inputs.
# The next n_out inputs correspond to nondifferentiated outputs.
# The last n_out inputs correspond to adjoint seeds, stacked horizontally

# The n_in outputs correspond to adjoint sensitivities, stacked horizontally.
# (n_in = n_in(),
# n_out = n_out())

# (n_in = n_in(), n_out = n_out())

# ADJOINT
class CasadosIntegratorSensAdjDAE(CasadosIntegratorSensAdj):
    def __init__(self, casados_integrator):
        self.nz = casados_integrator.nz
        super().__init__(casados_integrator)

    def get_sparsity_in(self, i):
        if i == 0:
            out = Sparsity.dense(self.nx, 1)
        elif i == 1:
            out = Sparsity.dense(self.nu, 1)
        elif i == 2:
            out = Sparsity.dense(self.nz, 1)
        elif i == 3:
            out = Sparsity(self.nx, 1)
        elif i == 4:
            out = Sparsity(self.nz, 1)
        elif i == 5:
            out = Sparsity.dense(self.nx, 1)
        elif i == 6:
            out = Sparsity.dense(self.nz, 1)
        return out

    def get_sparsity_out(self, i):
        if i == 0:
            out = Sparsity.dense(self.nx)
        elif i == 1:
            out = Sparsity.dense(self.nu)
        elif i == 2:
            out = Sparsity.dense(self.nz)
        return out

    def get_name_in(self, i):
        if i == 0:
            out = "x0"
        elif i == 1:
            out = "u0"
        elif i == 2:
            out = "z0"
        elif i == 3:
            out = "nominal_out"
        elif i == 4:
            out = "nominal_out_z"
        elif i == 5:
            out = "adj_seed"
        elif i == 6:
            out = "adj_seed_z"
        return out

    def get_n_in(self):
        return 7

    def get_n_out(self):
        return 3

    def eval(self, arg):
        # extract inputs
        x0 = np.array(arg[0])
        u0 = np.array(arg[1])
        z0 = np.array(arg[2])
        seed = np.array(arg[5])

        # set adj seed:
        self.acados_integrator.set("seed_adj", seed)
        # set input
        self.acados_integrator.set("x", x0)
        self.acados_integrator.set("u", u0)
        self.acados_integrator.set("z", z0)

        # solve
        self.acados_integrator.options_set("sens_adj", True)
        self.acados_integrator.options_set("sens_forw", False)
        self.acados_integrator.options_set("sens_hess", False)
        status = self.acados_integrator.solve()

        # output
        S_adj = self.acados_integrator.get("S_adj")

        S_adj_x = S_adj[: self.nx]
        S_adj_u = S_adj[self.nx :]

        self.casados_integrator.time_adj += self.acados_integrator.get("time_tot")

        return [S_adj_x, S_adj_u, Sparsity(self.nz, 1)]

    def get_jacobian(self, *args):

        if self.casados_integrator.hess_callback is None:
            self.casados_integrator.hess_callback = CasadosIntegratorSensHessDAE(
                self.casados_integrator
            )

        return self.casados_integrator.hess_callback


# HESSIAN
class CasadosIntegratorSensHessDAE(CasadosIntegratorSensHess):
    def __init__(self, casados_integrator):
        self.nz = casados_integrator.nz
        super().__init__(casados_integrator)

    def get_sparsity_in(self, i):
        if i == 0:
            out = Sparsity.dense(self.nx, 1)
        elif i == 1:
            out = Sparsity.dense(self.nu, 1)
        elif i == 2:
            out = Sparsity.dense(self.nz, 1)
        elif i == 3:
            out = Sparsity(self.nx, 1)
        elif i == 4:
            out = Sparsity(self.nz, 1)
        elif i == 5:
            out = Sparsity.dense(self.nx, 1)
        elif i == 6:
            out = Sparsity.dense(self.nz, 1)
        elif i == 7:
            out = Sparsity.dense(self.nx, 1)
        elif i == 8:
            out = Sparsity.dense(self.nu, 1)
        elif i == 9:
            out = Sparsity.dense(self.nz, 1)
        return out

    def get_sparsity_out(self, i):
        out = Sparsity.dense(
            self.nx + self.nu + self.nz, 3 * self.nx + self.nu + 3 * self.nz
        )
        return out

    def get_name_in(self, i):
        if i == 0:
            out = "x0"
        elif i == 1:
            out = "u0"
        elif i == 2:
            out = "z0"
        elif i == 3:
            out = "nominal_out"
        elif i == 4:
            out = "nominal_out_z"
        elif i == 5:
            out = "adj_seed"
        elif i == 6:
            out = "adj_seed_z"
        elif i == 7:
            out = "S_adj_out_x"
        elif i == 8:
            out = "S_adj_out_u"
        elif i == 9:
            out = "S_adj_out_z"
        return out

    def get_n_in(self):
        return 10

    def eval(self, arg):
        # extract inputs
        x0 = np.array(arg[0])
        seed = np.array(arg[5])
        u0 = np.array(arg[1])
        z0 = np.array(arg[2])

        # set adj seed:
        self.acados_integrator.set("seed_adj", seed)
        # set input
        self.acados_integrator.set("x", x0)
        self.acados_integrator.set("u", u0)
        self.acados_integrator.set("z", z0)

        # solve
        self.acados_integrator.options_set("sens_hess", True)
        self.acados_integrator.options_set("sens_forw", True)
        self.acados_integrator.options_set("sens_adj", True)
        status = self.acados_integrator.solve()

        # output
        S_hess = self.acados_integrator.get("S_hess")
        S_forw = self.acados_integrator.get("S_forw")

        # NOTE: casadi expects jacobian(S_adj, [x, u, nominal_out, seed_adj])
        #                            = [S_hess(for x,u), zeros(nx+nu, nx), S_forw ]
        row1 = np.concatenate(
            [
                S_hess,
                np.zeros((self.nx + self.nu, self.nx + 2 * self.nz)),
                S_forw.T,
                np.zeros((self.nx + self.nu, self.nz)),
            ],
            axis=1,
        )

        row2 = np.zeros((self.nz, 3 * self.nx + self.nu + 3 * self.nz))
        out = np.concatenate([row1, row2])

        self.casados_integrator.time_hess += self.acados_integrator.get("time_tot")

        return [out]

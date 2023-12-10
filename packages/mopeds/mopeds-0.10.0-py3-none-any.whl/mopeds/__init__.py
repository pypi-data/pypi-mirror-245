import importlib.metadata

__version__ = importlib.metadata.version("mopeds")

try:
    import acados_template
    import mopeds.casados_integrator

    # casados_integrator doesn't support new API of casadi 3.6
    _ACADOS_SUPPORT = False
except ImportError:
    _ACADOS_SUPPORT = False

from .utilities import MXPickler, show_html_from_dataframe
from .variables import (
    Variable,
    VariableParameter,
    VariableAlgebraic,
    VariableState,
    VariableConstant,
    VariableControlPiecewiseConstant,
    VariableControl,
    VariableList,
)
from .variables import BadVariableError
from .variables import ORIGIN_TS
from .model import Model
from .simulation_dynamic import Simulator
from .simulation_nle import SimulatorNLE
from .optimization import (
    Optimizer,
    ParameterEstimation,
    ParameterEstimationNLE,
    ParameterEstimationNLE_control,
)
from .optimization_oed import OptimalExperimentalDesign, OED_objective, OptimalSampling, AdaptiveOptimalSampling, AdaptiveSampling, FixedGridSampling, OptimalExperimentalDesign_NLE
from .mpc import ModelPredictiveControl

import mopeds.examples
import mopeds.tools

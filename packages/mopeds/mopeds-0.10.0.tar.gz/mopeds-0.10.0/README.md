# mopeds

<img align="right" src="https://git.tu-berlin.de/dbta/optimization/mopeds/-/raw/main/docs/logo.png" width="300px">

mopeds - **Mo**del based **P**arameter **E**stimation and **D**esign of Experiment**s** is a library wrapped around casadi to solve Simulation / Optimization problems based on steady state and dynamic models.

The system of equations can be a set of nonlinear equations (NLE), ordinary differential equations (ODE) or differential and algebraic equations (DAE) of index 1.

Parameter Estimation (PE) and Optimal Experimental Design (OED) are supported out of the box.

The project is looking for case studies and testers, so if you have any problems using the package or have any questions, do not hesitate to contact us.

Documentation is available [here](https://mopeds.readthedocs.io/en/latest/).


## Installation

`pip` Installation:

```
pip install mopeds
```

## Migration from par_est

If you used `par_est` before, in order to move to `mopeds` you need to replace the name, API did not change. In comparison to `par_est`, `mopeds` uses `casadi == 3.6.4`, so different results might be expected.
Considering creating a test to compare the numerical results while migrating.

## What's New?

### 0.10.0

- Rename par_est to mopeds and open-source the package

### 0.9.3.a1

- OED of dynamic models supports multiple different modes and strategies
- Added multiple regularization techniques

### 0.9.2

- fix WLS formulation  (remove division by 2)
- feature -> remove rounding of time_grid in Simulator

### 0.9.1

- fix bugs in identifiability analysis

### 0.9.0

- BREAKING: DAE simulators API change: from self.simulate() to self.simulate_sym()
- Added support for ACADOS ODE / DAE simulator
- Rework how PE for DAE and NLE works -> more simmilar code, easier to maintain
- Rework how Confidence Intervals of Parameters are calculated for multivariate measurements with different variance

### 0.8.0

NLE Simulator and Parameter Estimation were reworked, with focus on analysis of parameter variance-covariance matrix.
Parameter Estimation has different internals on how objective function is calculated, making it a bit faster and much more unrestandable.
Examples from Bates, Watts "Nonlinear Regression analysis and its applications" were imlemented and tested.

## Contributors

Many people have been involved in the development of this package, either by writing actual code, helping with the methods behind it, or simply using it and providing feedback and feature requests. Here are just a few names:

- Volodymyr Kozachynskyi
- Dario Staubach
- Martin Bubel
- Lorenz Hafner
- Mudassar Javed
- Torben Talis
- Joris Weigert
- Erik Esche
- Markus Illner
- Christian Hoffman
- Georg Brösigke
- Maria Stockman

and many, many others ...

## Development

- Clone this repo on your computer `git clone https://git.tu-berlin.de/dbta/optimization/mopeds.git`
- Run `poetry install` (ensure that correct python version is installed ex. pyenv)
- Run tests via `pytest`, final tests should be run with `tox -r` command

## par_est

Built versions of `par_est` are available in internal pypi registry:

```
pip install par_est --index-url https://git.tu-berlin.de/api/v4/projects/1237/packages/pypi/simple
```

## Acknowledgement

This work is funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) - 56091768 and 466397921.

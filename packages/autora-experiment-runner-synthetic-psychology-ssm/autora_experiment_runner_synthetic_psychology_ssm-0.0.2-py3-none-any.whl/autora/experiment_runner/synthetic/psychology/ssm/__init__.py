"""
A sequential sampling synthetic experiment.

Examples:
    >>> from autora.experiment_runner.synthetic.psychology.ssm import (
    ...     ssm_experiment, model_info
    ... )

    We can instantiate the experiment using the imported function
    First, we define the parameters. Here, we want to use a 'ddm' model.
    Let's see what parameters we need.
    >>> model_info('ddm')['params']
    ['v', 'a', 'z', 't']

    For more information about the parameters, see
    https://lnccbrown.github.io/HSSM/
    Here, we set fixed values for a, z, and t and define a linear mixed
    model (lmm) for v
    >>> a = 1
    >>> z = .5
    >>> t = 1

    To simulate a lmm, we use a formula, and define the coefficients
    >>> v = {
    ...     'formula': 'v ~ 1 + x1 + (x2|group)',
    ...     'fixed_effects': {'Intercept': .5, 'x1': .3},
    ...     'random_effects': {'group': {'x2': .1}}
    ... }

    To create our experiment, we must pass in the parameters in the same
    order as they appear in the info
    >>> experiment = ssm_experiment([v, a, z, t], model='ddm')

    Now, we create conditions for the experiment. We use need to make sure
    that the variables in the formula match the column names in a condition
    dataframe.
    >>> conditions = pd.DataFrame(
    ...     {
    ...         'x1': np.tile([1, 2, 3], 3),
    ...         'x2': np.tile([.1, .2, .3], 3),
    ...         'group': np.repeat([0, 1, 2], 3)
    ...     }
    ... )
    >>> conditions
       x1   x2  group
    0   1  0.1      0
    1   2  0.2      0
    2   3  0.3      0
    3   1  0.1      1
    4   2  0.2      1
    5   3  0.3      1
    6   1  0.1      2
    7   2  0.2      2
    8   3  0.3      2

    To run the experiment, we call the run funciton and pass in the conditions.
    Here we also pass in a random_state to make the results reproducible.
    >>> experiment.run(conditions=conditions, random_state=42)
       x1   x2  group        rt  response
    0   1  0.1      0  1.359592       1.0
    1   2  0.2      0  1.538962       1.0
    2   3  0.3      0  2.165649       1.0
    3   1  0.1      1  2.913196       1.0
    4   2  0.2      1  1.707723      -1.0
    5   3  0.3      1  1.383372       1.0
    6   1  0.1      2  1.619269       1.0
    7   2  0.2      2  1.214275       1.0
    8   3  0.3      2  1.430953      -1.0

"""

import warnings
from functools import partial
from typing import List, Optional

import numpy as np
import pandas as pd
from ssms.basic_simulators.simulator import simulator
from ssms.config import model_config

from autora.experiment_runner.synthetic.psychology.ssm._lmm import (
    _extract_variable_names,
    _lmm_data,
)
from autora.experiment_runner.synthetic.utilities import SyntheticExperimentCollection
from autora.variable import DV, IV, VariableCollection


def ssm_experiment(
    # Add any configurable parameters with their defaults here:
    include: List,
    model: str = "ddm",
    X: Optional[List[IV]] = None,
    name: str = "Template Experiment",
):
    """
    A sequential sampling synthetic experiment based on
    https://github.com/AlexanderFengler/ssm-simulators

    Parameters:
        includes: parameters of the simulator. Can be fixed values or linear mixed model formulas
            with coefficiants in a dict
        model: determines the model that will be simulated.
        X: can be used for additional information about independent variables, like value range.
            If omitted, the IVs are extracted from the formulas
        name: name of the experiment
    """

    params = dict(
        # Include all parameters here:
        name=name,
        include=include,
        model=model,
    )

    x = X

    if not X:
        iv_names = []
        for el in include:
            if isinstance(el, dict) and "formula" in el.keys():
                _, fixed_vars, random_vars = _extract_variable_names(el["formula"])
                iv_names += fixed_vars + random_vars
        iv_names = list(set(iv_names))
        x = [IV(name=iv_name) for iv_name in iv_names]

    y = [DV(name="rt"), DV(name="response")]
    variables = VariableCollection(
        independent_variables=x,
        dependent_variables=y,
    )

    def run(
        conditions: pd.DataFrame,
        random_state: Optional[int] = None,
        **kwargs,
    ):
        """A function which simulates noisy observations for a ssm."""
        _n_samples = len(conditions)

        true_values = []
        is_use_lmm = False
        for el in include:
            if isinstance(el, float) or isinstance(el, int):
                true_values.append(np.repeat(el, _n_samples))
            elif not isinstance(el, dict):
                true_values.append(np.array(el))
            else:
                is_use_lmm = True
                if "formula" not in el.keys():
                    raise Exception("No formula found in {el}")
                formula = el["formula"]
                fixed_effects = {}
                random_effects = {}
                if "fixed_effects" in el.keys():
                    fixed_effects = el["fixed_effects"]
                if "random_effects" in el.keys():
                    random_effects = el["random_effects"]
                _data, dependent = _lmm_data(
                    conditions.copy(),
                    formula,
                    fixed_effects,
                    random_effects,
                    random_state,
                )
                true_values.append(np.array(_data[dependent]))

        if is_use_lmm:
            warnings.warn(
                "Includes are evaluated in order of the list, see hssm documenation"
                "for the different model parameters"
            )

        true_values = np.array(true_values).T

        out = simulator(
            true_values, model=model, n_samples=1, random_state=random_state, **kwargs
        )

        out_pd = pd.DataFrame(
            np.column_stack([out["rts"][:, 0], out["choices"][:, 0]]),
            columns=["rt", "response"],
        )

        if conditions is None:
            return out_pd
        return pd.concat([conditions, out_pd], axis=1)

    ground_truth = partial(run, no_noise=True)
    """A function which simulates perfect observations"""

    def domain():
        """A function which returns all possible independent variable values as a 2D array."""
        x = variables.independent_variables[0].allowed_values.reshape(-1, 1)
        return x

    def plotter(model=None):
        """A function which plots the ground truth and (optionally) a fitted model."""
        raise NotImplementedError()

    # The object which gets stored in the synthetic inventory
    collection = SyntheticExperimentCollection(
        name=name,
        description=ssm_experiment.__doc__,
        variables=variables,
        run=run,
        ground_truth=ground_truth,
        domain=domain,
        plotter=plotter,
        params=params,
        factory_function=ssm_experiment,
    )
    return collection


def model_info(model: str):
    return model_config[model]

import re

import numpy as np


def _lmm_data(data, formula, fixed_effects, random_effects, random_state):
    """
    Simulate data for a linear mixed model using existing independent variables.

    Parameters:
    data (pd.DataFrame): DataFrame containing the independent variables.
    formula (str): Formula specifying the model.
    fixed_effects (dict): Dictionary of fixed effects coefficients.
    random_effects (dict): Nested dictionary for random effects.
        Format: {group_var: {effect: std_dev}}
    random_state (int): random state for reproducibilty

    Returns:
    pd.DataFrame: DataFrame with the simulated dependent variable.
    """

    _rng = np.random.default_rng(random_state)

    # Extract the dependent variable name and fixed variable names from the formula
    dependent_var, rhs = formula.split("~")
    dependent_var = dependent_var.strip()
    fixed_vars = re.findall(r"[a-z]\w*", rhs.split("(")[0])

    # Check for the presence of an intercept in the formula
    has_intercept = (
        True if "1" in fixed_effects or re.search(r"\b0\b", rhs) is None else False
    )

    # Initialize the dependent variable
    data[dependent_var] = fixed_effects.get("Intercept", 0) if has_intercept else 0

    # Add fixed effects
    for var in fixed_vars:
        if var in data.columns:
            data[dependent_var] += fixed_effects.get(var, 0) * data[var]

    # Process each random effect term
    random_effect_terms = re.findall(r"\((.+?)\|(.+?)\)", formula)
    for term in random_effect_terms:
        _random_effects, group_var = term
        group_var = group_var.strip()

        # Ensure the group_var is in the data
        if group_var not in data.columns:
            raise ValueError(f"Group variable '{group_var}' not found in the data")

        # Process each part of the random effect (intercept and slopes)
        for part in _random_effects.split("+"):
            part = part.strip()
            std_dev = random_effects[group_var].get(part, 0.5)
            random_effect_values = {
                group: _rng.normal(0, std_dev) for group in data[group_var].unique()
            }
            if part == "1":  # Random intercept
                if has_intercept:
                    data[dependent_var] += data[group_var].map(random_effect_values)
            else:  # Random slopes
                if part in data.columns:
                    data[dependent_var] += (
                        data[group_var].map(random_effect_values) * data[part]
                    )

    return data, dependent_var


def _extract_variable_names(formula):
    """
    Extract fixed and random effects from a linear mixed model formula.

    Parameters:
    formula (str): Formula specifying the model, e.g., 'y ~ x1 + x2 + (1 + x1|group) + (x2|subject)'

    Returns:
    tuple of (list, list): A tuple containing two lists - one for
    fixed effects and another for random effects.
    Examples:
        >>> formula_1 = 'y ~ x1 + x2 + (1 + x1|group) + (x2|subject)'
        >>> _extract_variable_names(formula_1)
        ('y', ['x1', 'x2'], ['group', 'subject'])

        >>> formula_2 = 'rt ~ x_1 + (x_2|group)'
        >>> _extract_variable_names(formula_2)
        ('rt', ['x_1', 'x_2'], ['group'])

        >>> formula_3 = 'RT ~ 1'
        >>> _extract_variable_names(formula_3)
        ('RT', [], [])


    """
    # Extract the right-hand side of the formula
    dependent, rhs = formula.split("~")
    dependent = dependent.strip()

    fixed_effects = re.findall(
        r"[a-z]\w*(?![^\(]*\))", rhs
    )  # Matches variables outside parentheses
    random_effects = re.findall(
        r"\(([^\|]+)\|([^\)]+)\)", rhs
    )  # Matches random effects groups

    # Include variables from random effects in fixed effects and make unique
    for reffect in random_effects:
        fixed_effects.extend(reffect[0].replace("1 + ", "").split("+"))

    # Removing duplicates and stripping whitespaces
    fixed_effects = sorted(list(set([effect.strip() for effect in fixed_effects])))
    random_groups = sorted(
        list(set([reffect[1].strip() for reffect in random_effects]))
    )

    return dependent, fixed_effects, random_groups

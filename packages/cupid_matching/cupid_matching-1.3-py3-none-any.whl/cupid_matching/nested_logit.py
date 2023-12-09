"""The components of the derivative of the entropy for a two-layer nested logit model.
One nest on each side must consist of the 0 option.
The other nests are specified as nested lists.
E.g. [[1, 3], [2,4]] describes two nests, one with types 1 and 3,
and the other with types 2 and 4.
On each side, the nests are the same for each type, with the same parameters.
"""

from math import log
from typing import cast

import numpy as np
from bs_python_utils.bsnputils import ThreeArrays, TwoArrays
from bs_python_utils.bsutils import bs_error_abort

from cupid_matching.entropy import EntropyFunctions, EntropyHessians
from cupid_matching.matching_utils import Matching
from cupid_matching.utils import NestsList, change_indices


def _get_params(
    additional_parameters: list | None,
) -> tuple[NestsList, NestsList]:
    if additional_parameters is None:
        bs_error_abort("additional_parameters must be specified for the nested logit.")
    else:
        nests_for_each_x, nests_for_each_y = additional_parameters
    return nests_for_each_x, nests_for_each_y


def e0_nested_logit(
    muhat: Matching, additional_parameters: list | None = None
) -> np.ndarray:
    """Returns the values of the parameter-independent part $e_0$
    for the nested logit.

    Args:
        muhat: a Matching
        additional_parameters: a list with the nest structure

    Returns:
        the (X,Y) matrix of the parameter-independent part
        of the first derivative of the entropy.
    """
    nests_for_each_x, nests_for_each_y = _get_params(additional_parameters)
    nests_x = change_indices(nests_for_each_x)
    nests_y = change_indices(nests_for_each_y)
    muxy, mux0, mu0y, *_ = muhat.unpack()
    X, Y = muxy.shape
    e0_vals = np.zeros((X, Y))

    for x in range(X):
        mux0_x = mux0[x]
        for nest in nests_x:
            mu_xn = np.sum(muxy[x, nest])
            e0_vals[x, nest] = -log(mu_xn / mux0_x)
    for y in range(Y):
        mu0y_y = mu0y[y]
        for nest in nests_y:
            mu_ny = np.sum(muxy[nest, y])
            e0_vals[nest, y] -= log(mu_ny / mu0y_y)
    return e0_vals


def e0_derivative_mu_nested_logit(
    muhat: Matching, additional_parameters: list | None = None
) -> ThreeArrays:
    """Returns the derivatives of the parameter-independent part $e_0$
    wrt $\\mu$ for the nested logit.

    Args:
        muhat: a Matching
        additional_parameters: a list with the nest structure

    Returns:
        the parameter-independent part of the hessian of the entropy
        wrt $(\\mu,\\mu)$.
    """
    nests_for_each_x, nests_for_each_y = _get_params(additional_parameters)
    nests_x = change_indices(nests_for_each_x)
    nests_y = change_indices(nests_for_each_y)
    muxy, mux0, mu0y, *_ = muhat.unpack()
    X, Y = muxy.shape

    hess_x = np.zeros((X, Y, Y))
    hess_y = np.zeros((X, Y, X))
    hess_xy = np.zeros((X, Y))
    der_logx0 = 1.0 / mux0
    der_log0y = 1.0 / mu0y

    for x in range(X):
        dlogx0 = der_logx0[x]
        for nest in nests_x:
            mu_xn = np.sum(muxy[x, nest])
            der_logxn = 1.0 / mu_xn
            for y in nest:
                hess_x[x, y, :] = -dlogx0
                hess_x[x, y, nest] -= der_logxn
    for y in range(Y):
        dlog0y = der_log0y[y]
        for nest in nests_y:
            mu_ny = np.sum(muxy[nest, y])
            der_logny = 1.0 / mu_ny
            for x in nest:
                hess_y[x, y, :] = -dlog0y
                hess_y[x, y, nest] -= der_logny
    for x in range(X):
        for y in range(Y):
            hess_xy[x, y] = hess_x[x, y, y] + hess_y[x, y, x]

    return hess_x, hess_y, hess_xy


def e0_derivative_r_nested_logit(
    muhat: Matching, additional_parameters: list | None = None
) -> TwoArrays:
    """Returns the derivatives of the parameter-independent part $e_0$
    wrt $r$ for the nested logit.

    Args:
        muhat: a Matching
        additional_parameters: a list with the nest structure

    Returns:
        the parameter-independent part of the hessian of the entropy
        wrt $(\\mu,r)$.
    """
    nests_for_each_x, nests_for_each_y = _get_params(additional_parameters)
    nests_x = change_indices(nests_for_each_x)
    nests_y = change_indices(nests_for_each_y)
    muxy, mux0, mu0y, n, m = muhat.unpack()
    X, Y = muxy.shape

    hess_n = np.zeros((X, Y))
    hess_m = np.zeros((X, Y))
    der_logx0 = 1.0 / mux0
    der_log0y = 1.0 / mu0y

    for x in range(X):
        dlogx0 = der_logx0[x]
        for nest in nests_x:
            for y in nest:
                hess_n[x, y] = dlogx0
    for y in range(Y):
        dlog0y = der_log0y[y]
        for nest in nests_y:
            for x in nest:
                hess_m[x, y] = dlog0y

    return hess_n, hess_m


e0_derivative_nested_logit = (
    e0_derivative_mu_nested_logit,
    e0_derivative_r_nested_logit,
)


def e_nested_logit(
    muhat: Matching, additional_parameters: list | None = None
) -> np.ndarray:
    """Returns the values of the parameter-dependent part  $e$
    for the nested logit.

    Args:
        muhat: a Matching
        additional_parameters: a list with the nest structure

    Returns:
        the (X,Y,n_alpha) array of the parameter-dependent part
        of the first derivative of the entropy.
    """
    nests_for_each_x, nests_for_each_y = _get_params(additional_parameters)
    nests_x = change_indices(nests_for_each_x)
    nests_y = change_indices(nests_for_each_y)
    n_rhos = len(nests_for_each_x)
    n_deltas = len(nests_for_each_y)
    n_alpha = n_rhos + n_deltas

    muxy, *_ = muhat.unpack()
    X, Y = muxy.shape

    e_vals = np.zeros((X, Y, n_alpha))

    for x in range(X):
        for i_n, nest in enumerate(nests_x):
            mux_nest_n = muxy[x, nest]
            mu_xn = np.sum(mux_nest_n)
            e_vals[x, nest, i_n] = -np.log(mux_nest_n / mu_xn)

    for y in range(Y):
        for i_n, nest in enumerate(nests_y):
            muy_nest_n = muxy[nest, y]
            mu_ny = np.sum(muy_nest_n)
            e_vals[nest, y, (i_n + n_rhos)] -= np.log(muy_nest_n / mu_ny)

    return e_vals


def e_derivative_mu_nested_logit(
    muhat: Matching, additional_parameters: list | None = None
) -> ThreeArrays:
    """Returns the derivatives of the parameter-dependent part $e$
     wrt $\\mu$ for the nested logit.

    Args:
        muhat: a Matching
        additional_parameters: a list with the nest structure

    Returns:
        the parameter-dependent part of the hessian of the entropy
        wrt $(\\mu,\\mu)$.
    """
    nests_for_each_x, nests_for_each_y = _get_params(additional_parameters)
    nests_x = change_indices(nests_for_each_x)
    nests_y = change_indices(nests_for_each_y)
    n_rhos = len(nests_for_each_x)
    n_deltas = len(nests_for_each_y)
    n_alpha = n_rhos + n_deltas

    muxy, *_ = muhat.unpack()
    X, Y = muxy.shape

    hess_x = np.zeros((X, Y, Y, n_alpha))
    hess_y = np.zeros((X, Y, X, n_alpha))
    hess_xy = np.zeros((X, Y, n_alpha))
    der_logxy = 1.0 / muxy

    for x in range(X):
        for i_n, nest in enumerate(nests_x):
            mux_nest_n = muxy[x, nest]
            mu_xn = np.sum(mux_nest_n)
            der_logxn = 1.0 / mu_xn
            for t in nest:
                hess_x[x, nest, t, i_n] = der_logxn
            hess_xy[x, nest, i_n] = der_logxn - der_logxy[x, nest]

    for y in range(Y):
        for i_n, nest in enumerate(nests_y):
            muy_nest_n = muxy[nest, y]
            mu_ny = np.sum(muy_nest_n)
            der_logny = 1.0 / mu_ny
            i_n2 = i_n + n_rhos
            for z in nest:
                hess_y[nest, y, z, i_n2] = der_logny
            hess_xy[nest, y, i_n2] = der_logny - der_logxy[nest, y]

    return hess_x, hess_y, hess_xy


def e_derivative_r_nested_logit(
    muhat: Matching, additional_parameters: list | None = None
) -> TwoArrays:
    """Returns the derivatives of the parameter-dependent part $e$
     wrt $r$ for the nested logit.

    Args:
        muhat: a Matching
        additional_parameters: a list with the nest structure

    Returns:
        the parameter-dependent part of the hessian of the entropy
        wrt $(\\mu,r)$.
    """
    nests_for_each_x, nests_for_each_y = _get_params(additional_parameters)
    n_rhos = len(nests_for_each_x)
    n_deltas = len(nests_for_each_y)
    n_alpha = n_rhos + n_deltas

    muxy, *_ = muhat.unpack()
    X, Y = muxy.shape

    hess_n = np.zeros((X, Y, n_alpha))
    hess_m = np.zeros((X, Y, n_alpha))

    return hess_n, hess_m


e_derivative_nested_logit = (
    e_derivative_mu_nested_logit,
    e_derivative_r_nested_logit,
)


def setup_standard_nested_logit(
    nests_for_each_x: NestsList, nests_for_each_y: NestsList
) -> tuple[EntropyFunctions, EntropyFunctions]:
    nests_params = [nests_for_each_x, nests_for_each_y]

    nest_description = "      each x has the same nests over 0, 1, ..., Y:\n"
    for n in nests_for_each_x:
        nest_description += f"      {n}\n"
    nest_description += "      each y has the same nests over 0, 1, ..., X:\n"
    for n in nests_for_each_y:
        nest_description += f"      {n}\n"
    nest_description += "       the parameters rho and delta do not depend on the type."

    entropy_nested_logit = EntropyFunctions(
        e0_fun=e0_nested_logit,
        parameter_dependent=True,
        e_fun=e_nested_logit,
        additional_parameters=nests_params,
        hessian="provided",
        e0_derivative=cast(EntropyHessians, e0_derivative_nested_logit),
        e_derivative=cast(EntropyHessians, e_derivative_nested_logit),
        description="Two-layer nested logit with analytic Hessian\n" + nest_description,
    )

    entropy_nested_logit_numeric = EntropyFunctions(
        e0_fun=e0_nested_logit,
        parameter_dependent=True,
        additional_parameters=nests_params,
        e_fun=e_nested_logit,
        description="Two-layer nested logit with numerical Hessian\n"
        + nest_description,
    )

    return entropy_nested_logit, entropy_nested_logit_numeric

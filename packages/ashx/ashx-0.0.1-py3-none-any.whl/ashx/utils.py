#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: benvial
# This file is part of ashx
# License: GPLv3
# See the documentation at  gitlab.com/benvial/ashx


"""
Utility functions
"""


__all__ = ["project", "array2function", "function2array", "integrate"]


import ufl
from dolfinx.fem import Function, assemble_scalar, form
from dolfinx.fem.petsc import LinearProblem
from ufl import TestFunction, TrialFunction, dx, inner


def integrate(fun, dx=None, domain=None):
    """Integration

    Parameters
    ----------
    fun : dolfinx.fem.Function
        Function to integrate
    dx : Measure, optional
        Integration measure, by default None
    domain : str or list of str, int or list of int, optional
        The subdomain where to perform the integration, by default None

    Returns
    -------
    scalar float or complex
        The integral
    """
    dx = dx or ufl.dx
    if domain is not None:
        dx = dx(domain)
    return assemble_scalar(form(fun * dx))


def array2function(array, function=None, space=None):
    if function is None:
        function = Function(space)
    function.x.array[:] = array
    return function


def function2array(function):
    return function.x.array


def project(function, space, bcs=[]):
    u, v = TrialFunction(space), TestFunction(space)
    A = inner(u, v) * dx
    b = inner(function, v) * dx
    problem = LinearProblem(
        A, b, bcs=bcs, petsc_options={"ksp_type": "preonly", "pc_type": "lu"}
    )
    return problem.solve()

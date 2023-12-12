#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: benvial
# This file is part of ashx
# License: GPLv3
# See the documentation at  gitlab.com/benvial/ashx


import os

import numpy as np
from dolfinx.fem import Function, FunctionSpace

import ashx
from ashx import array2function as a2f
from ashx import function2array as f2a


def test_project():
    data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")

    mesh, ct, ft, msh = ashx.gmsh2dolfinx(
        0,
        mshfile=os.path.join(data_dir, "tri.msh"),
        dim=2,
    )
    V = FunctionSpace(mesh, ("Lagrange", 2))

    u = Function(V)
    u.vector.array[:] = 1
    Vproj = FunctionSpace(mesh, ("DG", 2))

    uproj = ashx.project(u, Vproj)
    tests = []
    f = Function(Vproj)
    for i in range(2048):
        test = a2f(f2a(uproj), function=f)
        tests.append(test)
    assert np.allclose(uproj.vector.array, 1)
    assert np.allclose(a2f(f2a(uproj), space=Vproj).vector.array, 1)

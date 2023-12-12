#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: benvial
# This file is part of ashx
# License: GPLv3
# See the documentation at  gitlab.com/benvial/ashx


import os

import numpy as np
from dolfinx.fem import Function

import ashx


def test_geo():
    data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
    self = ashx.BaseGeometry(
        mshfile=os.path.join(data_dir, "tri.msh"),
        dim=2,
    )

    f = Function(self.Vmat)
    f.vector.array = 1

    vol = self.integrate(f)
    volc = self.integrate(self.constant(1))

    assert np.allclose(vol, 1)
    assert sum(self.cell_vol) == vol == volc

    vol_incl = self.get_volume("inclusion")

    assert np.allclose(vol_incl, 0.3**2)

    pwdict2 = {}
    for i, subdomain in enumerate(self.subdomains):
        pwdict2[subdomain] = i + 1
    fun1 = self.piecewise(pwdict2)

    pwdict2 = dict(cell=lambda x: x[0] * 2, inclusion=lambda x: np.cos(x[1]))
    self.piecewise(pwdict2)

    s1 = np.ones(self.num_sub_cells["cell"])
    s2 = np.ones(self.num_sub_cells["inclusion"]) * 2
    pwdict3 = dict(cell=s1, inclusion=s2)
    fun3 = self.piecewise(pwdict3)
    assert np.allclose(fun1.x.array, fun3.x.array)

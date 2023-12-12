#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: benvial
# This file is part of ashx
# License: GPLv3
# See the documentation at  gitlab.com/benvial/ashx


import os

import numpy as np
from dolfinx.fem import Constant

import ashx


def test_measure():
    r = 0.3
    surf_incl = r**2

    data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")

    subdomains_dict = dict(cell=1, incl=2)
    mesh, ct, ft, msh = ashx.gmsh2dolfinx(
        0,
        mshfile=os.path.join(data_dir, "tri.msh"),
        dim=2,
    )

    # markers1 = ct.find(1)

    meas1 = ashx.Measure(
        "dx",
        domain=mesh,
        subdomain_data=ct,
        subdomain_dict=subdomains_dict,
    )
    Id = Constant(mesh, 1.0)
    surf1 = ashx.integrate(Id, meas1, "cell")

    surf2 = ashx.integrate(Id, meas1, "incl")
    surf3 = ashx.integrate(Id, meas1)

    assert np.allclose(surf1, 1 - surf_incl)
    assert np.allclose(surf2, surf_incl)

    assert np.allclose(surf3, 1)

    surf4 = ashx.integrate(Id, meas1, ["cell", "incl"])

    assert np.allclose(surf4, 1)
    assert np.allclose(ashx.integrate(Id, meas1("cell")), ashx.integrate(Id, meas1(1)))

    meas2 = ashx.Measure(
        "dx",
        domain=mesh,
        subdomain_data=ct,
        subdomain_dict=subdomains_dict,
        subdomain_id="cell",
    )
    assert np.allclose(surf1, ashx.integrate(Id, meas2))

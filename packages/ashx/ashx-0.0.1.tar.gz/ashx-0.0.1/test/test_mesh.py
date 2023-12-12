#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: benvial
# This file is part of ashx
# License: GPLv3
# See the documentation at  gitlab.com/benvial/ashx


import os

import pytest

import ashx


def test_mesh():
    data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")

    with pytest.raises(ValueError):
        ashx.gmsh2dolfinx(
            0,
            dim=4,
        )

    ashx.gmsh2dolfinx(
        0,
        mshfile=os.path.join(data_dir, "tri.msh"),
        dim=2,
    )

    ashx.gmsh2dolfinx(
        0,
        mshfile=os.path.join(data_dir, "quad.msh"),
        dim=2,
        quad="True",
    )

    mesh, ct, ft, msh = ashx.gmsh2dolfinx(
        0,
        mshfile=os.path.join(data_dir, "tet.msh"),
        dim=3,
    )

    mesh, ct, ft, msh = ashx.gmsh2dolfinx(
        0,
        mshfile=os.path.join(data_dir, "hex.msh"),
        dim=3,
        quad=True,
    )

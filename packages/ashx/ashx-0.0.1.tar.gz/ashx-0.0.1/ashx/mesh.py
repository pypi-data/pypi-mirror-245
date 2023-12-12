#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: benvial
# This file is part of ashx
# License: GPLv3
# See the documentation at  gitlab.com/benvial/ashx


"""Mesh functions and classes.
"""

__all__ = ["create_mesh", "gmsh2dolfinx"]

import os
import tempfile

import meshio
from dolfinx.io import XDMFFile, gmshio
from mpi4py import MPI


def create_mesh(mesh, cell_type, prune_z=False):
    cells = mesh.get_cells_type(cell_type)
    cell_data = mesh.get_cell_data("gmsh:physical", cell_type)
    # try:
    #     cell_data = mesh.get_cell_data("gmsh:physical", cell_type)
    # except ValueError:
    #     return None
    points = mesh.points[:, :2] if prune_z else mesh.points
    out_mesh = meshio.Mesh(
        points=points, cells={cell_type: cells}, cell_data={"name_to_read": [cell_data]}
    )
    return out_mesh


# TODO: deal with physical points in 2D and physiscal points/lines in 3D


def gmsh2dolfinx(
    proc,
    mshfile=None,
    cellxdmf=None,
    facetxdmf=None,
    data_dir=None,
    dim=3,
    quad=False,
):
    if dim not in [2, 3]:
        raise ValueError
    if dim == 3:
        cell = "hexahedron" if quad else "tetra"
        facet = "quad" if quad else "triangle"
    else:
        cell = "quad" if quad else "triangle"
        facet = "line"

    data_dir = data_dir or tempfile.mkdtemp()
    mshfile = mshfile or "mesh.msh"
    cellxdmf = cellxdmf or "cells.xdmf"
    facetxdmf = facetxdmf or "facets.xdmf"
    # mshfile = os.path.join(data_dir, mshfile)
    cellxdmf = os.path.join(data_dir, cellxdmf)
    facetxdmf = os.path.join(data_dir, facetxdmf)

    mesh, cell_markers, facet_markers = gmshio.read_from_msh(
        mshfile, MPI.COMM_WORLD, gdim=dim
    )
    prune_z = dim != 3

    if proc == 0:
        # Read in mesh
        msh = meshio.read(mshfile)
        # Create and save one file for the mesh, and one file for the facets
        cell_mesh = create_mesh(msh, cell, prune_z=prune_z)
        facet_mesh = create_mesh(msh, facet, prune_z=prune_z)
        meshio.write(cellxdmf, cell_mesh)
        meshio.write(facetxdmf, facet_mesh)

    with XDMFFile(MPI.COMM_WORLD, cellxdmf, "r") as xdmf:
        mesh = xdmf.read_mesh(name="Grid")
        ct = xdmf.read_meshtags(mesh, name="Grid")
    mesh.topology.create_connectivity(mesh.topology.dim, mesh.topology.dim - 1)
    with XDMFFile(MPI.COMM_WORLD, facetxdmf, "r") as xdmf:
        ft = xdmf.read_meshtags(mesh, name="Grid")
    return mesh, ct, ft, msh

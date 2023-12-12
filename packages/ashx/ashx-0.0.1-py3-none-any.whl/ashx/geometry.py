#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: benvial
# This file is part of ashx
# License: GPLv3
# See the documentation at  gitlab.com/benvial/ashx


"""
Geometry definition
"""

__all__ = ["BaseGeometry"]


import tempfile

from dolfinx.fem import Constant, Function, FunctionSpace, form
from dolfinx.fem.petsc import assemble_vector
from petsc4py.PETSc import ScalarType
from ufl import TestFunction, inner

from .measure import Measure
from .mesh import gmsh2dolfinx
from .utils import integrate


class BaseGeometry:
    """Base geometry object"""

    def __init__(self, dim, mshfile, data_dir=None, proc=0):
        """_summary_

        Parameters
        ----------
        dim : int
            Physical dimension (2 or 3)
        mshfile : str
            Name of gmsh .msh file
        data_dir : str, optional
            Path to the data directory where the output xdmf files will be written.
            If the default None, a temporary directory will be created.
        proc : int, optional
            MPI process, by default 0
        """
        self.data_dir = data_dir or tempfile.mkdtemp()
        self.dim = dim
        self.proc = proc

        self.mesh, ct, ft, self.mshio_mesh = gmsh2dolfinx(
            proc, mshfile, data_dir=self.data_dir, dim=dim
        )

        self.data = dict(cells=ct, facets=ft)
        self.physical = self.mshio_mesh.field_data
        self.cells = {}
        self.facets = {}
        self.subdomain_map = {}
        self.facets_map = {}
        for dom, dimtag in self.physical.items():
            if dimtag[1] == dim:
                self.cells[dom] = self.data["cells"].find(dimtag[0])
                self.subdomain_map[dom] = dimtag[0]
            if dimtag[1] == dim - 1:
                self.facets[dom] = self.data["facets"].find(dimtag[0])
                self.facets_map[dom] = dimtag[0]

        self.subdomains = list(self.cells.keys())
        self.boundaries = list(self.facets.keys())
        self.num_sub_cells = {}
        for subdomain in self.subdomains:
            self.num_sub_cells[subdomain] = len(self.cells[subdomain])
        self.num_cells = sum(self.num_sub_cells.values())
        self.num_sub_facets = {}
        for boundary in self.boundaries:
            self.num_sub_facets[subdomain] = len(self.facets[boundary])
        self.num_facets = sum(self.num_sub_facets.values())
        self.Vmat = FunctionSpace(self.mesh, ("DG", 0))

        self.dx = Measure(
            "dx",
            domain=None,
            subdomain_id="everywhere",
            metadata=None,
            subdomain_data=self.data["cells"],
            subdomain_dict=self.subdomain_map,
        )

    def integrate(self, f, subdomain="everywhere", metadata={}):
        return integrate(f, self.dx(metadata=metadata, subdomain_id=subdomain))

    def constant(self, c):
        return Constant(self.mesh, ScalarType(c))

    def get_volume(self, physical_id="everywhere"):
        return self.integrate(self.constant(1), physical_id)

    @property
    def cell_vol(self):
        q_degree = 0
        vol = Function(self.Vmat)
        assemble_vector(
            vol.vector,
            form(
                inner(ScalarType(1), TestFunction(self.Vmat))
                * self.dx(metadata={"quadrature_degree": q_degree})
            ),
        )
        vol.x.scatter_forward()
        return vol.x.array.real

    def piecewise(self, subdomain_dict, pw_fun=None):
        pw_fun = pw_fun or Function(self.Vmat)
        for subdomain, value in subdomain_dict.items():
            cells = self.cells[subdomain]
            if callable(value):
                # _pw_fun = Function(self.Vmat)
                _pw_fun = pw_fun.copy()
                _pw_fun.interpolate(value)
                pw_fun.x.array[cells] = _pw_fun.x.array[cells]
                pw_fun.x.scatter_forward()
            else:
                pw_fun.x.array[cells] = ScalarType(value)
        return pw_fun

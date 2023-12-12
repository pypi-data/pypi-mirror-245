#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: benvial
# This file is part of ashx
# License: GPLv3
# See the documentation at  gitlab.com/benvial/ashx

"""
Custom integration measures
"""

__all__ = ["Measure"]

import ufl


class Measure(ufl.Measure):
    """Representation of an integration measure.

    The Measure object holds information about integration properties
    to be transferred to a Form on multiplication with a scalar
    expression.

    Parameters
    ----------
    integral_type : one of "cell", etc, or short form "dx", etc
        The type of integral
    domain : ufl.domain.AbstractDomain, optional
        An AbstractDomain object (most often a Mesh), by default None
    subdomain_id : either string "everywhere", a single subdomain id int or str, or tuple of ints or str, optional
        ID of the subdomain, by default "everywhere"
    metadata : dict, optional
        Additional compiler-specific parameters
        affecting how code is generated, including parameters
        for optimization or debugging of generated code, by default None
    subdomain_data : dolfinx.mesh.MeshTags, optional
        Object representing data to interpret subdomain_id with, by default None
    subdomain_dict : dict, optional
        Mapping from physical domain str to int representation, by default None
    """

    def __init__(
        self,
        integral_type,
        domain=None,
        subdomain_id="everywhere",
        metadata=None,
        subdomain_data=None,
        subdomain_dict=None,
    ):
        self.subdomain_dict = subdomain_dict
        if (
            self.subdomain_dict
            and isinstance(subdomain_id, str)
            and subdomain_id != "everywhere"
        ):
            subdomain_id = self.subdomain_dict[subdomain_id]
        super().__init__(
            integral_type,
            domain=domain,
            subdomain_id=subdomain_id,
            metadata=metadata,
            subdomain_data=subdomain_data,
        )

    def __call_single__(self, subdomain_id=None, **kwargs):
        if (
            self.subdomain_dict
            and isinstance(subdomain_id, str)
            and subdomain_id != "everywhere"
        ):
            subdomain_id = self.subdomain_dict[subdomain_id]
        return super().__call__(subdomain_id=subdomain_id, **kwargs)

    def __call__(self, subdomain_id=None, **kwargs):
        subdomain_id = None if subdomain_id == [] else subdomain_id
        if not isinstance(subdomain_id, list):
            return self.__call_single__(subdomain_id=subdomain_id, **kwargs)
        for i, sid in enumerate(subdomain_id):
            if i == 0:
                out = self.__call_single__(subdomain_id=sid, **kwargs)
            else:
                out += self.__call_single__(subdomain_id=sid, **kwargs)
        return out

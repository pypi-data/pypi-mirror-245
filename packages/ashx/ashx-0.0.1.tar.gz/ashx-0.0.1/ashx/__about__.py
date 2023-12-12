#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: benvial
# This file is part of ashx
# License: GPLv3
# See the documentation at  gitlab.com/benvial/ashx


import importlib.metadata as metadata


def get_meta(metadata):
    data = metadata.metadata("ashx")
    __version__ = metadata.version("ashx")
    __author__ = data.get("Author-email")
    __description__ = data.get("Summary")
    return __version__, __author__, __description__, data


__version__, __author__, __description__, data = get_meta(metadata)

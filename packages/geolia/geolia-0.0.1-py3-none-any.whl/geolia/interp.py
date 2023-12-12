#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: benvial
# This file is part of geolia
# License: GPLv3
# See the documentation at  gitlab.com/benvial/geolia


"""Interpolation tools"""

import numpy as np
from scipy.interpolate import LinearNDInterpolator, NearestNDInterpolator


def interpolator(meshobject, cell, kind="nearest", **kwargs):
    mesh = meshobject[cell]
    if kind not in ["nearest", "linear"]:
        raise ValueError(
            f"Wrong interpolation kind: {kind}, Choose betwwen 'nearest' or 'linear'"
        )
    points = np.mean(mesh.points[mesh.cells[0].data], axis=1)
    values = mesh.cell_data[cell][0]
    Interp = NearestNDInterpolator if kind == "nearest" else LinearNDInterpolator
    return Interp(points, values, **kwargs)


def interpolate(grid, meshobject, cell, kind="nearest", **kwargs):
    interp = interpolator(meshobject, cell, kind=kind, **kwargs)
    return interp(*grid)

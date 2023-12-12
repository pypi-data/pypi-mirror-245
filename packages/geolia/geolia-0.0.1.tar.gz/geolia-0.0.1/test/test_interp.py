#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: benvial
# This file is part of geolia
# License: GPLv3
# See the documentation at  gitlab.com/benvial/geolia

import numpy as np
import pytest

import geolia as gl


def test_interp2D():
    a = 1

    geom = gl.Geometry()

    corner = -a / 2, -a / 2, 0
    r = 0.3
    center = [0, 0, 0]
    cell = geom.add_square(corner, a)
    circ = geom.add_disk(center, r)
    circ, cell = cell / circ
    geom.add(cell, "cell")
    geom.add(circ, "circ")
    pmesh = a / 11
    geom.set_size("cell", pmesh)
    geom.set_size("circ", pmesh)
    geom.build()
    geom.finalize()

    mesh = geom.mesh

    n = 2**7
    x = y = np.linspace(-a / 2, a / 2, n)
    X, Y = np.meshgrid(x, y)
    for kind in ["nearest", "linear"]:
        gl.interpolate([X, Y], mesh, "triangle", kind)
    with pytest.raises(ValueError):
        gl.interpolate([X, Y], mesh, "triangle", "wrong")


def test_interp3D():
    a = 1
    geom = gl.Geometry(dim=3)
    corner = -a / 2, -a / 2, -a / 2
    center = [0, 0, 0]
    cell = geom.add_box(corner, (a, a, a))
    r = a / 3
    incl = geom.add_sphere(center, r)

    incl, cell = cell / incl

    geom.add(cell, "cell")
    geom.add(incl, "inclusion")
    geom.set_size("cell", a / 5)
    geom.set_size("inclusion", a / 5)
    geom.build()
    geom.finalize()
    Npts = 11
    x = y = z = np.linspace(-a / 2, a / 2, Npts)
    x1, y1, z1 = np.meshgrid(x, y, z)
    for kind in ["nearest", "linear"]:
        gl.interpolate((x1, y1, z1), geom.mesh, cell="tetra", kind=kind)

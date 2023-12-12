#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: benvial
# This file is part of geolia
# License: GPLv3
# See the documentation at  gitlab.com/benvial/geolia

import uuid
from math import pi

import matplotlib.pyplot as plt
import numpy as np

from geolia import geometry as geo
from geolia import mesh as meshmod


def test_dev():
    a = 1
    geoname = uuid.uuid4().hex.upper()[0:6]

    geom = geo.Geometry(model_name=geoname)

    vertices = (0, 1, 0), (1, 1, 0), (1, 2, 0)
    p = geom.add_point(vertices[0])
    print(p)
    line = geom.add_line(vertices[0], vertices[1])
    print(line)
    # sys.exit(0)
    corner = -a / 2, -a / 2, 0
    r = 0.3
    center = [0, 0, 0]
    cell = geom.add_square(corner, a)
    print(cell)
    circ = geom.add_disk(center, r)
    circ += geom.add_disk((0, -0.3, 0), r / 2)

    cell.rotate(center, pi / 3)

    circ, cell = cell / circ

    circ1 = geom.add_disk((0.1, 0, 0), r / 4)
    circ2 = geom.add_disk((0, 0.2, 0), r / 2)
    circ2 *= geom.add_square((0.1, 0.1, 0), r / 2)

    circs = [circ1, circ2]
    circ -= circs

    print(cell)

    test1 = geom.add_disk((0.1, 0.4, 0), 0.1 * r)
    test2 = geom.add_disk((0.3, 0.3, 0), 0.2 * r)
    test = [test1, test2]

    *test, cell = cell / test

    pol = geom.add_polygon(vertices)
    geom.add(pol, "pol")

    vertices = np.array(vertices) + np.array([1, -2, 0])
    spl = geom.add_spline(vertices)
    geom.add(spl, "spl")

    geom.add(cell, "cell")
    # geom.set_size("cell",0.05)
    geom.add(circ)
    geom.add(test, "whatever")
    geom.set_size("cell", 0.08)
    geom.set_size(circ.name, 0.01)
    geom.set_size("whatever", 0.01)
    geom.set_size("pol", 0.1)
    geom.set_size("spl", 0.1)

    geom.build()

    geom.finalize()

    mesh = geom.mesh["triangle"]

    _, ax = plt.subplots()
    meshmod.plot_mesh(ax, mesh, lw=0.4, color="#379798")
    # plt.axis("scaled")

    _, ax = plt.subplots()
    ax, cax = geo.plot_geometry(ax, geom)
    plt.xlabel("$x$")
    plt.ylabel("$y$")

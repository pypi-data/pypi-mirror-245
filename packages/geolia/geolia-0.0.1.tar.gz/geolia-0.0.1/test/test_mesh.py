#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: benvial
# This file is part of geolia
# License: GPLv3
# See the documentation at  gitlab.com/benvial/geolia


import pytest

import geolia as gl
import geolia.geometry as geo


def test_mesh():
    geo.gmsh.initialize()
    with pytest.raises(Exception):
        geom = geo.Geometry(1, options={"General.DefaultFileName": {}})
    options = {
        "Mesh.Color.Triangles": {160, 150, 255},
        "General.DefaultFileName": "geometry.geo",
    }
    geo.gmsh_options.get("Mesh.Color.Triangles")
    geo.gmsh_options.get("Unknown")
    geo.gmsh_options.set("General.DefaultFileName", "test.geo")
    assert geo.gmsh_options.get("General.DefaultFileName") == "test.geo"
    geom = geo.Geometry(1, options=options)
    assert geo.gmsh_options.get("General.DefaultFileName") == "geometry.geo"
    vertices = (0, 1, 0), (1, 1, 0), (1, 2, 0)
    p = geom.add_point(vertices[0])
    line = geom.add_line(vertices[0], vertices[1])
    geom.add(p, "p")
    geom.add(line, "line")

    geom.add_line(vertices[1], p.tag)

    bnds1 = geom.get_boundaries(line.tag, physical=False)
    bnds = geom.get_boundaries("line")
    assert bnds1 == bnds
    geom.set_size(p.tag, 0.4, dim=0)
    geom.set_size(line.tag, 0.4)
    geom.set_size([line.tag], 0.4)
    geom.build()
    geom.finalize()
    gl.read_mesh(
        geom.msh_file, data_dir=None, data_dir_xdmf=None, dim=1, subdomains="line"
    )
    options = {"General.Verbosity": True}
    geom = geo.Geometry(3, options=options)
    vertices = (0, 1, 0), (1, 1, 0), (1, 2, 0)
    b = geom.add_box((0, 0, 0), (1, 1, 1))
    geom.add(b, "b")
    bnds = geom.get_boundaries("b")
    geom.set_size(b.tag, 0.4)
    geom.set_size([b.tag], 0.4)
    geom.build()
    geom.read_mesh_file("b")
    geom.finalize()

    with pytest.raises(Exception):
        b = geom.add_box((0, 0, 0), (1, 1, 1))

    geom = geo.Geometry(2, quad=True)
    d1 = geom.add_ellipse((0, 1, 0), 2.1, 2.0)
    d2 = geom.add_ellipse((0, 0, 0), 2, 2.1)
    geom.rotate(d1.tag, (0, 0, 0), (0, 0, 1), 0.1)
    geom.tagdim(d2.dimtag)
    geom._translation_matrix([1, 1, 1])
    out = geom.fuse(d1.tag, d2.tag)
    geom.get_boundaries(out[0], physical=False)
    d1 = geom.add_disk((0, 0, 0), 3)
    d2 = geom.add_disk((0, 0, 0), 2)
    out1, out2 = geom.fragment(d1.tag, d2.tag)
    d1 = geom.add_disk((0, 0, 0), 1)
    d2 = geom.add_disk((0, 1, 0), 2)
    out = geom.intersect(d1.tag, d2.tag)
    d1 = geom.add_disk((0, 0, 0), 1)
    d2 = geom.add_disk((0, 1, 0), 2)
    out = geom.cut(d2.tag, d1.tag)
    geom.add_physical(out, "out")
    geom.get_boundaries("out")
    geom.subdomains["volumes"] = dict(unknown=100)
    geom._check_subdomains()
    # geom.add(p, "p")
    # geom.add(line, "line")
    # geom.set_size(p.tag, 0.4, dim=0)
    # geom.set_size(line.tag, 0.4)
    # geom.set_size([line.tag], 0.4)
    # geom.build()
    # geom.finalize()
    geom.is_initialized()
    geom.finalize()
    geom.finalize()

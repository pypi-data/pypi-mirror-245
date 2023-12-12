#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: benvial
# This file is part of geolia
# License: GPLv3
# See the documentation at  gitlab.com/benvial/geolia


"""Meshing utilities"""


__all__ = ["read_mesh", "mesh2triang", "plot_mesh"]

import tempfile

import meshio
import numpy as np


def read_mesh(
    mesh_file, data_dir=None, data_dir_xdmf=None, dim=3, subdomains=None, quad=False
):
    data_dir_xdmf = data_dir_xdmf or tempfile.mkdtemp()
    meshio_mesh = meshio.read(mesh_file, file_format="gmsh")
    if dim == 3:
        base_cell_type = "hexahedron" if quad else "tetra"
    elif dim == 2:
        base_cell_type = "quad" if quad else "triangle"
    else:
        base_cell_type = "line"

    points = meshio_mesh.points if dim == 3 else meshio_mesh.points[:, :2]
    physicals = meshio_mesh.cell_data_dict["gmsh:physical"]

    cell_types, data_gmsh = zip(*physicals.items())
    data_gmsh = list(data_gmsh)
    cells = {ct: [] for ct in cell_types}

    for cell_type in cell_types:
        for cell in meshio_mesh.cells:
            if cell.type == cell_type:
                cells[cell_type].append(cell.data)
        cells[cell_type] = np.vstack(cells[cell_type])

    icell = np.where(np.array(cell_types) == base_cell_type)[0][0]
    if subdomains is not None:
        doms = subdomains if hasattr(subdomains, "__len__") else [subdomains]
        mask = np.hstack([np.where(data_gmsh[icell] == i) for i in doms])[0]
        data_gmsh_ = data_gmsh[icell][mask]
        data_gmsh[icell] = data_gmsh_
        cells[base_cell_type] = cells[base_cell_type][mask]

    mesh_data = {}

    for cell_type, data in zip(cell_types, data_gmsh):
        meshio_data = meshio.Mesh(
            points=points,
            cells={cell_type: cells[cell_type]},
            cell_data={cell_type: [data]},
        )
        meshio.xdmf.write(f"{data_dir_xdmf}/{cell_type}.xdmf", meshio_data)
        mesh_data[cell_type] = meshio_data
    return mesh_data


def mesh2triang(mesh):
    import matplotlib.tri as tri

    xy = mesh.points
    cells = mesh.cells[0].data
    return tri.Triangulation(xy[:, 0], xy[:, 1], cells)


def plot_mesh(ax, mesh, **kwargs):
    color = kwargs.pop("color", "#808080")
    out = ax.triplot(mesh2triang(mesh), color=color, **kwargs)
    ax.set_aspect(1)
    return out

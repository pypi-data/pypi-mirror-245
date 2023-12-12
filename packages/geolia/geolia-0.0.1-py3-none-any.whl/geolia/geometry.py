#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: benvial
# This file is part of geolia
# License: GPLv3
# See the documentation at  gitlab.com/benvial/geolia


"""
Geometry definition using Gmsh api.
For more information see Gmsh's `documentation <https://gmsh.info/doc/texinfo/gmsh.html>`_
"""


import numbers
import os
import re
import tempfile
from functools import wraps

import gmsh
import numpy as np

from .mesh import mesh2triang, read_mesh

geo = gmsh.model.geo
occ = gmsh.model.occ
model = gmsh.model
setnum = gmsh.option.setNumber
gmsh_options = gmsh.option


def _set_opt_gmsh(name, value):
    if isinstance(value, str):
        return gmsh_options.set_string(name, value)
    elif isinstance(value, set) or isinstance(value, tuple) or isinstance(value, list):
        return gmsh_options.set_color(name, *value)
    elif isinstance(value, (numbers.Number, bool)):
        if isinstance(value, bool):
            value = int(value)
        return gmsh_options.set_number(name, value)
    else:
        raise ValueError(
            "value must be string or number or any of set/tuple/list of length 3 (for setting colors)"
        )


def _get_opt_gmsh(name):
    try:
        return gmsh_options.get_number(name)
    except Exception:
        try:
            return gmsh_options.get_string(name)
        except Exception:
            try:
                return gmsh_options.get_color(name)
            except Exception:
                return None


setattr(gmsh_options, "set", _set_opt_gmsh)
setattr(gmsh_options, "get", _get_opt_gmsh)


def _add_method(cls, func, name):
    @wraps(func)
    def wrapper(*args, sync=True, **kwargs):
        if not gmsh.is_initialized():
            raise RuntimeError("Geometry is not initialized")
        out = func(*args, **kwargs)
        if sync:
            occ.synchronize()
        return out

    setattr(cls, name, wrapper)
    return func


def _dimtag(tag, dim=2):
    if not isinstance(tag, list):
        tag = [tag]
    return [(dim, t) for t in tag]


def _get_bnd(idf, dim):
    out = gmsh.model.getBoundary(_dimtag(idf, dim=dim), False, False, False)
    return [b[1] for b in out]


def _convert_name(name):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def geowrapp(method, self, dim=None):
    def wrapper(*args, **kwargs):
        tag = method(*args, **kwargs)
        # self = args[0]
        dimtag = self.dimtag(tag) if dim is None else _dimtag(tag, dim)
        return GeoBase(dimtag)

    return wrapper


def is_iter(element):
    try:
        iter(element)
    except TypeError:
        return False
    return True


def _check_length(x):
    return x[0] if len(x) == 1 else x


def __boolean_operation__(self, other, function):
    otag = [o.dimtag for o in other] if is_iter(other) else [other.dimtag]
    out, outmap = function([self.dimtag], otag)
    occ.synchronize()
    geo_out = [GeoBase(o) for o in out]
    # # out contains all the generated entities of the same dimension as the input
    # # entities:
    # print("fragment produced volumes:")
    # for e in out:
    #     print(e)
    # # outmap contains the parent-child relationships for all the input entities:
    # print("before/after fragment relations:")
    # for e in zip([self.dimtag, other.dimtag], outmap):
    #     print("parent " + str(e[0]) + " -> child " + str(e[1]))

    return _check_length(geo_out)


class GeoBase:
    def __init__(self, dimtag, name=None, physical_tag=None):
        self.dimtag = _check_length(dimtag)
        self.name = name or f"geo_{self.__hash__()}"
        self.physical_tag = physical_tag

    @property
    def dim(self):
        return self.dimtag[0]

    @property
    def tag(self):
        return self.dimtag[1]

    @property
    def tags(self):
        return dict(geometrical=self.tag, physical=self.physical_tag)

    def __repr__(self):
        return f"GeoBase {self.name}, dim={self.dim}, tags={self.tags}"

    def __add__(self, other):
        return __boolean_operation__(self, other, occ.fuse)

    def __sub__(self, other):
        return __boolean_operation__(self, other, occ.cut)

    def __truediv__(self, other):
        return __boolean_operation__(self, other, occ.fragment)

    def __mul__(self, other):
        return __boolean_operation__(self, other, occ.intersect)

    def rotate(self, point, angle, axis=(0, 0, 1)):
        occ.rotate([self.dimtag], *point, *axis, angle)
        return self

    def __len__(self):
        return 0


def _add_gmsh_methods(self):
    for object_name in dir(occ):
        if (
            not object_name.startswith("__")
            and object_name != "mesh"
            and object_name not in dir(self)
        ):
            bound_method = getattr(occ, object_name)
            name = _convert_name(bound_method.__name__)
            if name.startswith("add_"):
                dim = None
                if name == "add_point":
                    dim = 0
                if name in ["add_line"]:
                    dim = 1
                bound_method = geowrapp(bound_method, self, dim)
            _add_method(self, bound_method, name)


class Geometry:
    """Base class for geometry models."""

    def __init__(
        self,
        dim=2,
        model_name=None,
        data_dir=None,
        gmsh_args=None,
        options=None,
        quad=False,
    ):
        self.dim = dim
        self.model_name = model_name or f"model_{self.__hash__()}"
        self.data_dir = data_dir or tempfile.mkdtemp()
        self.gmsh_args = gmsh_args or []
        self.options = options or {}
        self.quad = quad

        self.mesh_name = f"{self.model_name}.msh"
        self.subdomains = dict(volumes={}, surfaces={}, curves={}, points={})
        self.occ = occ
        self.model = model
        self.mesh = None

        _add_gmsh_methods(self)
        self._gmsh_add_disk = self.add_disk
        del self.add_disk
        self._gmsh_add_ellipse = self.add_ellipse
        del self.add_ellipse
        self._gmsh_add_spline = self.add_spline
        del self.add_spline
        self._gmsh_add_rectangle = self.add_rectangle
        del self.add_rectangle
        self._gmsh_add_point = self.add_point
        del self.add_point
        self._gmsh_add_line = self.add_line
        del self.add_line
        self._gmsh_add_box = self.add_box
        del self.add_box
        self._gmsh_add_sphere = self.add_sphere
        del self.add_sphere

        self.finalize()

        if not gmsh.is_initialized():
            gmsh.initialize(self.gmsh_args)

        for k, v in self.options.items():
            gmsh_options.set(k, v)

        if quad:
            set_quad()
        else:
            unset_quad()

    def is_initialized(self):
        gmsh.is_initialized()

    def finalize(self):
        if gmsh.is_initialized():
            gmsh.finalize()
            # try:
            #     gmsh.finalize()
            # except Exception:
            #     pass

    def _check_dim(self, dim):
        return self.dim if dim is None else dim

    def rotate(self, tag, point, axis, angle, dim=None):
        dt = self.dimtag(tag, dim=dim)
        return occ.rotate(dt, *point, *axis, angle)

    def add_physical(self, idf, name, dim=None):
        """Add a physical domain.

        Parameters
        ----------
        idf : int or list of int
            The identifiant(s) of elementary entities making the physical domain.
        name : str
            Name of the domain.
        dim : int
            Dimension.
        """
        dim = self._check_dim(dim)
        dicname = list(self.subdomains)[3 - dim]
        if not isinstance(idf, list):
            idf = [idf]
        num = gmsh.model.addPhysicalGroup(dim, idf)
        self.subdomains[dicname][name] = num
        gmsh.model.removePhysicalName(name)
        gmsh.model.setPhysicalName(dim, self.subdomains[dicname][name], name)
        return num

    def add(self, entity, name=None):
        name = name or entity.name
        if len(entity) > 0:
            tag = [e.tag for e in entity]
            dim = [e.dim for e in entity]
            assert np.allclose(dim, dim[0])
            dim = dim[0]
        else:
            tag = entity.tag
            dim = entity.dim
        phys_tag = self.add_physical(tag, name, dim=dim)
        if len(entity) > 0:
            for e in entity:
                e.physical_tag = phys_tag
                e.name = name
        else:
            entity.physical_tag = phys_tag
            entity.name = name
        return phys_tag

    def dimtag(self, idf, dim=None):
        """Convert an integer or list of integer to gmsh DimTag notation.

        Parameters
        ----------
        idf : int or list of int
            Label or list of labels.
        dim : type
            Dimension.

        Returns
        -------
        int or list of int
            A tuple (dim, tag) or list of such tuples (gmsh DimTag notation).

        """
        dim = self._check_dim(dim)

        return _dimtag(idf, dim=dim)

    def tagdim(self, x):
        if not isinstance(x, list):
            x = [x]
        return [t[1] for t in x]

    def _translation_matrix(self, t):
        M = [
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
        ]
        M[3], M[7], M[11] = t
        return M

    # def add_circle(self,x, y, z, ax, ay,**kwargs):
    #     ell = self._gmsh_add_ellipse(x, y, z, ax, ay,**kwargs)
    #     ell = self.add_curve_loop([ell])
    #     return self.add_plane_surface([ell])

    def add_point(self, coords, **kwargs):
        return self._gmsh_add_point(*coords, **kwargs)

    def add_line(self, p1, p2, **kwargs):
        ps = []
        for p in [p1, p2]:
            if isinstance(p, GeoBase):
                ps.append(p.tag)
            elif not isinstance(p, int):
                p = self.add_point(p, **kwargs)
                ps.append(p.tag)
            else:
                ps.append(p)
        return self._gmsh_add_line(*ps, **kwargs)

    def add_disk(self, center, radius, **kwargs):
        return self.add_ellipse(center, radius, radius, **kwargs)

    def add_ellipse(self, center, ax, ay, **kwargs):
        if ax < ay:
            ell = self._gmsh_add_disk(*center, ay, ax, **kwargs)
            self.rotate(ell.tag, center, (0, 0, 1), np.pi / 2, dim=2)
            return ell
        else:
            return self._gmsh_add_disk(*center, ax, ay, **kwargs)

    def add_rectangle(self, corner, dx, dy, **kwargs):
        tag = self._gmsh_add_rectangle(*corner, dx, dy, **kwargs)
        return tag

    def add_square(self, corner, dx, **kwargs):
        return self.add_rectangle(corner, dx, dx, **kwargs)

    def add_box(self, coords, widths, **kwargs):
        return self._gmsh_add_box(*coords, *widths, **kwargs)

    def add_sphere(self, center, radius, **kwargs):
        return self._gmsh_add_sphere(*center, radius, **kwargs)

    def add_polygon(self, vertices, mesh_size=0.0, **kwargs):
        """Adds a polygon.

        Parameters
        ----------
        vertices : array of shape (Npoints,3)
            Coordinates of the vertices.
        mesh_size : float
            Mesh sizes at vertices (the default is 0.0).

        Returns
        -------
        int
            The tag of the polygon.

        """
        verts = np.array(vertices)
        N = len(vertices)
        points = []
        for coord in verts:
            p0 = self.add_point(coord, meshSize=mesh_size)
            points.append(p0)
        lines = []
        for i in range(N - 1):
            lines.append(self.add_line(points[i], points[i + 1]))
        if not np.allclose(coord[0], coord[-1]):
            lines.append(self.add_line(points[i + 1], points[0]))
        lines = [line.tag for line in lines]
        loop = self.add_curve_loop(lines, **kwargs)
        loop = loop.tag
        return self.add_plane_surface([loop])

    def add_spline(self, points, mesh_size=0.0, **kwargs):
        """Adds a spline.

        Parameters
        ----------
        points : array of shape (Npoints,3)
            Corrdinates of the points.
        mesh_size : float
            Mesh sizes at points (the default is 0.0).

        Returns
        -------
        int
            The tag of the spline.

        """
        dt = [self.add_point(p, meshSize=mesh_size) for p in points]
        if not np.allclose(points[0], points[-1]):
            dt.append(dt[0])
        dt = [d.tag for d in dt]
        spl = self._gmsh_add_spline(dt, **kwargs)
        spl = self.add_curve_loop([spl.tag])
        return self.add_plane_surface([spl.tag])

    def fragment(self, id1, id2, dim1=None, dim2=None, sync=True, map=False, **kwargs):
        dim1 = self._check_dim(dim1)
        dim2 = self._check_dim(dim2)
        a1 = self.dimtag(id1, dim1)
        a2 = self.dimtag(id2, dim2)
        dimtags, mapping = occ.fragment(a1, a2, **kwargs)
        if sync:
            occ.synchronize()
        tags = [_[1] for _ in dimtags]
        return (tags, mapping) if map else tags

    def intersect(self, id1, id2, dim1=None, dim2=None, sync=True, map=False, **kwargs):
        dim1 = self._check_dim(dim1)
        dim2 = self._check_dim(dim2)
        a1 = self.dimtag(id1, dim1)
        a2 = self.dimtag(id2, dim2)
        dimtags, mapping = occ.intersect(a1, a2, **kwargs)
        if sync:
            occ.synchronize()
        tags = [_[1] for _ in dimtags]
        return (tags, mapping) if map else tags

    def cut(self, id1, id2, dim1=None, dim2=None, sync=True, **kwargs):
        dim1 = self._check_dim(dim1)
        dim2 = self._check_dim(dim2)
        a1 = self.dimtag(id1, dim1)
        a2 = self.dimtag(id2, dim2)
        ov, ovv = occ.cut(a1, a2, **kwargs)
        if sync:
            occ.synchronize()
        return [o[1] for o in ov]

    def fuse(self, id1, id2, dim1=None, dim2=None, sync=True):
        dim1 = self._check_dim(dim1)
        dim2 = self._check_dim(dim2)
        a1 = self.dimtag(id1, dim1)
        a2 = self.dimtag(id2, dim2)
        ov, ovv = occ.fuse(a1, a2)
        if sync:
            occ.synchronize()
        return [o[1] for o in ov]

    def get_boundaries(self, idf, dim=None, physical=True):
        dim = self._check_dim(dim)
        if isinstance(idf, str):
            if dim == 2:
                type_entity = "surfaces"
            elif dim == 3:
                type_entity = "volumes"
            else:
                type_entity = "curves"
            idf = self.subdomains[type_entity][idf]

            n = gmsh.model.getEntitiesForPhysicalGroup(dim, idf)
            bnds = [_get_bnd(n_, dim=dim) for n_ in n]
            bnds = [item for sublist in bnds for item in sublist]
            return list(dict.fromkeys(bnds))
        else:
            n = gmsh.model.getEntitiesForPhysicalGroup(dim, idf)[0] if physical else idf
            return _get_bnd(n, dim=dim)

    def _set_size(self, idf, s, dim=None):
        dim = self._check_dim(dim)
        p = gmsh.model.getBoundary(
            self.dimtag(idf, dim=dim), False, False, True
        )  # Get all points
        gmsh.model.mesh.setSize(p, s)

    def _check_subdomains(self):
        groups = gmsh.model.getPhysicalGroups()
        names = [gmsh.model.getPhysicalName(*g) for g in groups]
        for subtype, subitems in self.subdomains.items():
            for idf in subitems.copy().keys():
                if idf not in names:
                    subitems.pop(idf)

    def set_mesh_size(self, params, dim=None):
        dim = self._check_dim(dim)
        if dim == 3:
            type_entity = "volumes"
        elif dim == 2:
            type_entity = "surfaces"
        elif dim == 1:
            type_entity = "curves"
        elif dim == 0:
            type_entity = "points"

        # revert sort so that smaller sizes are set last
        params = dict(
            sorted(params.items(), key=lambda item: float(item[1]), reverse=True)
        )

        for idf, p in params.items():
            if isinstance(idf, str):
                num = self.subdomains[type_entity][idf]
                n = gmsh.model.getEntitiesForPhysicalGroup(dim, num)
                for n_ in n:
                    self._set_size(n_, p, dim=dim)
            else:
                self._set_size(idf, p, dim=dim)

    def set_size(self, idf, s, dim=None):
        if hasattr(idf, "__len__") and not isinstance(idf, str):
            for i, id_ in enumerate(idf):
                s_ = s[i] if hasattr(s, "__len__") else s
                params = {id_: s_}
                self.set_mesh_size(params, dim=dim)
        else:
            self.set_mesh_size({idf: s}, dim=dim)

    def read_mesh_info(self):
        if self.dim == 1:
            self.domains = self.subdomains["curves"]
            self.lines = {}
            self.boundaries = {}
        elif self.dim == 2:
            self.domains = self.subdomains["surfaces"]
            self.lines = {}
            self.boundaries = self.subdomains["curves"]
        else:
            self.domains = self.subdomains["volumes"]
            self.lines = self.subdomains["curves"]
            self.boundaries = self.subdomains["surfaces"]

        self.points = self.subdomains["points"]

    @property
    def msh_file(self):
        return os.path.join(self.data_dir, self.mesh_name)

    def build(
        self,
        interactive=False,
        generate_mesh=True,
        write_mesh=True,
        read_info=True,
        read_mesh=True,
        check_subdomains=True,
    ):
        """Build the geometry.

        Parameters
        ----------
        interactive : bool
            Open ``gmsh`` GUI? (the default is False).
        generate_mesh : bool
            Mesh with ``gmsh``? (the default is True).
        write_mesh : bool
            Write mesh to disk? (the default is True).
        read_info : bool
            Read subdomain markers information? (the default is True).
        read_mesh : bool
            Read mesh information? (the default is True).
        check_subdomains : bool
            Sanity check of subdomains names? (the default is True).

        Returns
        -------
        dict
            A dictionary containing the mesh and markers.

        """
        if check_subdomains:
            self._check_subdomains()

        self.mesh = self.generate_mesh(
            generate=generate_mesh, write=write_mesh, read=read_mesh
        )

        if read_info:
            self.read_mesh_info()
        if interactive:  # pragma: no cover
            gmsh.fltk.run()  # pragma: no cover
        return self.mesh

    def read_mesh_file(self, subdomains=None):
        if subdomains is not None:
            if isinstance(subdomains, str):
                subdomains = [subdomains]
            key = "volumes" if self.dim == 3 else "surfaces"
            subdomains_num = [self.subdomains[key][s] for s in subdomains]
        else:
            subdomains_num = subdomains

        return read_mesh(
            self.msh_file,
            data_dir=self.data_dir,
            dim=self.dim,
            subdomains=subdomains_num,
            quad=self.quad,
        )

    def generate_mesh(self, generate=True, write=True, read=True):
        if generate:
            gmsh.model.mesh.generate(self.dim)
        if write:
            gmsh.write(self.msh_file)
        if read:
            return self.read_mesh_file()


# def is_on_plane(P, A, B, C, eps=1e-12):
#     Ax, Ay, Az = A
#     Bx, By, Bz = B
#     Cx, Cy, Cz = C

#     a = (By - Ay) * (Cz - Az) - (Cy - Ay) * (Bz - Az)
#     b = (Bz - Az) * (Cx - Ax) - (Cz - Az) * (Bx - Ax)
#     c = (Bx - Ax) * (Cy - Ay) - (Cx - Ax) * (By - Ay)
#     d = -(a * Ax + b * Ay + c * Az)

#     return np.allclose(a * P[0] + b * P[1] + c * P[2] + d, 0, atol=eps)


# def is_on_line(p, p1, p2, eps=1e-12):
#     x, y = p
#     x1, y1 = p1
#     x2, y2 = p2
#     return np.allclose((y - y1) * (x2 - x1), (y2 - y1) * (x - x1), atol=eps)


# def is_on_line3D(p, p1, p2, eps=1e-12):
#     return is_on_plane(p, *p1, eps=eps) and is_on_plane(p, *p2, eps=eps)


def plot_geometry(ax, geom, **kwargs):
    import matplotlib.pyplot as plt

    mesh = geom.mesh["triangle"]
    data = mesh.cell_data["triangle"][0]
    cmap = kwargs.pop("cmap", "tab20")
    cmap = plt.get_cmap(cmap, np.max(data) - np.min(data) + 1)
    triplt = ax.tripcolor(
        mesh2triang(mesh),
        facecolors=data,
        vmin=np.min(data) - 0.5,
        vmax=np.max(data) + 0.5,
        cmap=cmap,
        **kwargs,
    )
    ax.set_aspect(1)
    ticks = [s for s in geom.subdomains["surfaces"]]
    cax = plt.colorbar(triplt, ticks=np.arange(np.min(data), np.max(data) + 1))
    cax.set_ticklabels(ticks)
    return triplt, cax


def set_quad():
    # gmsh.option.setNumber("Mesh.Algorithm", 8)
    gmsh.option.setNumber("Mesh.RecombinationAlgorithm", 2)
    # gmsh.option.setNumber('Mesh.RecombineOptimizeTopology', 1)
    # gmsh.option.setNumber('Mesh.RecombineNodeRepositioning', 1)
    # gmsh.option.setNumber('Mesh.RecombineMinimumQuality', 1e-3)
    gmsh.option.setNumber("Mesh.RecombineAll", 1)


def unset_quad():
    gmsh.option.setNumber("Mesh.RecombineAll", 0)

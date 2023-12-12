#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: benvial
# This file is part of geolia
# License: GPLv3
# See the documentation at  gitlab.com/benvial/geolia


import importlib.metadata as metadata


def get_meta(metadata):
    data = metadata.metadata("geolia")
    __version__ = metadata.version("geolia")
    __author__ = data.get("Author-email")
    __description__ = data.get("Summary")
    return __version__, __author__, __description__, data


__version__, __author__, __description__, data = get_meta(metadata)

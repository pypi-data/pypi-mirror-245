#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""LISA Python Constant module."""

from importlib.metadata import metadata, PackageNotFoundError

from .constants import Constant


try:
    lisaconstants_metadata = metadata("lisaconstants").json
    __version__ = lisaconstants_metadata["version"]
    __author__ = lisaconstants_metadata["author"]
    __email__ = lisaconstants_metadata["author_email"]
except PackageNotFoundError:
    pass

# Iterate over constants and set their values as
# attributes of the current module for easy access
for name, constant in Constant.ALL.items():
    vars()[name] = constant.value

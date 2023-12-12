# -*- coding: utf-8 -*-
# Copyright: (c) 2023-2021, Distronode Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Requiement reporter implementations."""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

try:
    from resolvelib import BaseReporter
except ImportError:
    class BaseReporter:  # type: ignore[no-redef]
        pass


class CollectionDependencyReporter(BaseReporter):
    """A dependency reporter for Distronode Collections.

    This is a proxy class allowing us to abstract away importing resolvelib
    outside of the `distronode.galaxy.dependency_resolution` Python package.
    """

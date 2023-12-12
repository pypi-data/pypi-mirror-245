# (c) 2017, Distronode by RedHat Inc,
#
# This file is part of Distronode
#
# Distronode is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Distronode is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Distronode.  If not, see <http://www.gnu.org/licenses/>.

#############################################
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from distronode.utils.vars import combine_vars


def sort_groups(groups):
    return sorted(groups, key=lambda g: (g.depth, g.priority, g.name))


def get_group_vars(groups):
    """
    Combine all the group vars from a list of inventory groups.

    :param groups: list of distronode.inventory.group.Group objects
    :rtype: dict
    """
    results = {}
    for group in sort_groups(groups):
        results = combine_vars(results, group.get_vars())

    return results

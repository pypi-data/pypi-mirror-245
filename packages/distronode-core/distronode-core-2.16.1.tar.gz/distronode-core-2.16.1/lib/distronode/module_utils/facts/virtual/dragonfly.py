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

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from distronode.module_utils.facts.virtual.freebsd import FreeBSDVirtual, VirtualCollector


class DragonFlyVirtualCollector(VirtualCollector):
    # Note the _fact_class impl is actually the FreeBSDVirtual impl
    _fact_class = FreeBSDVirtual
    _platform = 'DragonFly'

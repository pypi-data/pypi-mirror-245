# (c) 2014 James Cammarata, <jcammarata@khulnasoft.com>
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

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


def is_quoted(data):
    return len(data) > 1 and data[0] == data[-1] and data[0] in ('"', "'") and data[-2] != '\\'


def unquote(data):
    ''' removes first and last quotes from a string, if the string starts and ends with the same quotes '''
    if is_quoted(data):
        return data[1:-1]
    return data

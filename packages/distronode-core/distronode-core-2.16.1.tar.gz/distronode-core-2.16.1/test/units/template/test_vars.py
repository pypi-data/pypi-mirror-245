# (c) 2012-2014, KhulnaSoft Ltd <info@khulnasoft.com>
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

from distronode.template import Templar
from distronode.template.vars import DistronodeJ2Vars


def test_globals_empty():
    assert isinstance(dict(DistronodeJ2Vars(Templar(None), {})), dict)


def test_globals():
    res = dict(DistronodeJ2Vars(Templar(None), {'foo': 'bar', 'blip': [1, 2, 3]}))
    assert isinstance(res, dict)
    assert 'foo' in res
    assert res['foo'] == 'bar'

#
# (c) 2020 Red Hat Inc.
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

from io import StringIO

from units.compat import unittest
from distronode.plugins.connection import local
from distronode.playbook.play_context import PlayContext


class TestLocalConnectionClass(unittest.TestCase):

    def test_local_connection_module(self):
        play_context = PlayContext()
        play_context.prompt = (
            '[sudo via distronode, key=ouzmdnewuhucvuaabtjmweasarviygqq] password: '
        )
        in_stream = StringIO()

        self.assertIsInstance(local.Connection(play_context, in_stream), local.Connection)

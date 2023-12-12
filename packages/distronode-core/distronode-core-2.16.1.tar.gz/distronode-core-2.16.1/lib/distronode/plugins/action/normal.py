# (c) 2012, KhulnaSoft Ltd <info@khulnasoft.com>
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
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from distronode import constants as C
from distronode.plugins.action import ActionBase
from distronode.utils.vars import merge_hash


class ActionModule(ActionBase):

    _supports_check_mode = True
    _supports_async = True

    def run(self, tmp=None, task_vars=None):

        # individual modules might disagree but as the generic the action plugin, pass at this point.
        result = super(ActionModule, self).run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        wrap_async = self._task.async_val and not self._connection.has_native_async

        # do work!
        result = merge_hash(result, self._execute_module(task_vars=task_vars, wrap_async=wrap_async))

        # hack to keep --verbose from showing all the setup module result
        # moved from setup module as now we filter out all _distronode_ from result
        if self._task.action in C._ACTION_SETUP:
            result['_distronode_verbose_override'] = True

        if not wrap_async:
            # remove a temporary path we created
            self._remove_tmp_path(self._connection._shell.tmpdir)

        return result

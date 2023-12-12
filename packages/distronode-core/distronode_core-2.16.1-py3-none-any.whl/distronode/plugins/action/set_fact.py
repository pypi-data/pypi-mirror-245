# Copyright 2013 Dag Wieers <dag@wieers.com>
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

from distronode.errors import DistronodeActionFail
from distronode.module_utils.six import string_types
from distronode.module_utils.parsing.convert_bool import boolean
from distronode.plugins.action import ActionBase
from distronode.utils.vars import isidentifier

import distronode.constants as C


class ActionModule(ActionBase):

    TRANSFERS_FILES = False
    _requires_connection = False

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        facts = {}
        cacheable = boolean(self._task.args.pop('cacheable', False))

        if self._task.args:
            for (k, v) in self._task.args.items():
                k = self._templar.template(k)

                if not isidentifier(k):
                    raise DistronodeActionFail("The variable name '%s' is not valid. Variables must start with a letter or underscore character, "
                                            "and contain only letters, numbers and underscores." % k)

                # NOTE: this should really use BOOLEANS from convert_bool, but only in the k=v case,
                # right now it converts matching explicit YAML strings also when 'jinja2_native' is disabled.
                if not C.DEFAULT_JINJA2_NATIVE and isinstance(v, string_types) and v.lower() in ('true', 'false', 'yes', 'no'):
                    v = boolean(v, strict=False)
                facts[k] = v
        else:
            raise DistronodeActionFail('No key/value pairs provided, at least one is required for this action to succeed')

        if facts:
            # just as _facts actions, we don't set changed=true as we are not modifying the actual host
            result['distronode_facts'] = facts
            result['_distronode_facts_cacheable'] = cacheable
        else:
            # this should not happen, but JIC we get here
            raise DistronodeActionFail('Unable to create any variables with provided arguments')

        return result

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

from distronode.plugins.action import ActionBase
from distronode.plugins.action.template import ActionModule as TemplateActionModule


# Even though TemplateActionModule inherits from ActionBase, we still need to
# directly inherit from ActionBase to appease the plugin loader.
class ActionModule(TemplateActionModule, ActionBase):
    DEFAULT_NEWLINE_SEQUENCE = '\r\n'

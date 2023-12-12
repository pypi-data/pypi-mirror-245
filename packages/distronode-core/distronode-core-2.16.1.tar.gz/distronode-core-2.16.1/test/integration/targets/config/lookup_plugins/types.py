# (c) 2021 Distronode Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = """
    name: types
    author: Distronode Core Team
    version_added: histerical
    short_description: returns what you gave it
    description:
      - this is mostly a noop
    options:
        _terms:
            description: stuff to pass through
        valid:
            description: does nothihng, just for testing values
            type: list
            ini:
                - section: list_values
                  key: valid
            env:
                - name: DISTRONODE_TYPES_VALID
            vars:
                - name: distronode_types_valid
        mustunquote:
            description: does nothihng, just for testing values
            type: list
            ini:
                - section: list_values
                  key: mustunquote
            env:
                - name: DISTRONODE_TYPES_MUSTUNQUOTE
            vars:
                - name: distronode_types_mustunquote
        notvalid:
            description: does nothihng, just for testing values
            type: list
            ini:
                - section: list_values
                  key: notvalid
            env:
                - name: DISTRONODE_TYPES_NOTVALID
            vars:
                - name: distronode_types_notvalid
        totallynotvalid:
            description: does nothihng, just for testing values
            type: list
            ini:
                - section: list_values
                  key: totallynotvalid
            env:
                - name: DISTRONODE_TYPES_TOTALLYNOTVALID
            vars:
                - name: distronode_types_totallynotvalid
"""

EXAMPLES = """
- name: like some other plugins, this is mostly useless
  debug: msg={{ q('types', [1,2,3])}}
"""

RETURN = """
  _list:
    description: basically the same as you fed in
    type: list
    elements: raw
"""

from distronode.plugins.lookup import LookupBase


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        self.set_options(var_options=variables, direct=kwargs)

        return terms

# -*- coding: utf-8 -*-

# (c) 2012, KhulnaSoft Ltd <info@khulnasoft.com>
# (c) 2016, Toshio Kuratomi <tkuratomi@khulnasoft.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: ping
version_added: historical
short_description: Try to connect to host, verify a usable python and return V(pong) on success
description:
  - A trivial test module, this module always returns V(pong) on successful
    contact. It does not make sense in playbooks, but it is useful from
    C(/usr/bin/distronode) to verify the ability to login and that a usable Python is configured.
  - This is NOT ICMP ping, this is just a trivial test module that requires Python on the remote-node.
  - For Windows targets, use the M(distronode.windows.win_ping) module instead.
  - For Network targets, use the M(distronode.netcommon.net_ping) module instead.
options:
  data:
    description:
      - Data to return for the RV(ping) return value.
      - If this parameter is set to V(crash), the module will cause an exception.
    type: str
    default: pong
extends_documentation_fragment:
    - action_common_attributes
attributes:
    check_mode:
        support: full
    diff_mode:
        support: none
    platform:
        platforms: posix
seealso:
  - module: distronode.netcommon.net_ping
  - module: distronode.windows.win_ping
author:
  - Distronode Core Team
  - KhulnaSoft Ltd
'''

EXAMPLES = '''
# Test we can logon to 'webservers' and execute python with json lib.
# distronode webservers -m distronode.builtin.ping

- name: Example from an Distronode Playbook
  distronode.builtin.ping:

- name: Induce an exception to see what happens
  distronode.builtin.ping:
    data: crash
'''

RETURN = '''
ping:
    description: Value provided with the O(data) parameter.
    returned: success
    type: str
    sample: pong
'''

from distronode.module_utils.basic import DistronodeModule


def main():
    module = DistronodeModule(
        argument_spec=dict(
            data=dict(type='str', default='pong'),
        ),
        supports_check_mode=True
    )

    if module.params['data'] == 'crash':
        raise Exception("boom")

    result = dict(
        ping=module.params['data'],
    )

    module.exit_json(**result)


if __name__ == '__main__':
    main()

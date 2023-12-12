# -*- coding: utf-8 -*-

# Copyright: (c) 2023, Distronode Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: vyosfacts
short_description: module to test module_defaults
description: module to test module_defaults
version_added: '2.13'
'''

EXAMPLES = r'''
'''

from distronode.module_utils.basic import DistronodeModule


def main():
    module = DistronodeModule(
        argument_spec=dict(
            vyosfacts=dict(type=bool),
        ),
        supports_check_mode=True
    )
    module.exit_json(vyosfacts=module.params['vyosfacts'])


if __name__ == '__main__':
    main()

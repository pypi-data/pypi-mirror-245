#!/usr/bin/python
from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: test_docs_returns_broken
short_description: Test module
description:
    - Test module
author:
    - Distronode Core Team
'''

EXAMPLES = '''
'''

RETURN = '''
test:
    description: A test return value.
   type: str

broken_key: [
'''


from distronode.module_utils.basic import DistronodeModule


def main():
    module = DistronodeModule(
        argument_spec=dict(),
    )

    module.exit_json()


if __name__ == '__main__':
    main()

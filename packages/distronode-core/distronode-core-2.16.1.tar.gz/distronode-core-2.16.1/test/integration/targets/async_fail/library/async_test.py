from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import sys
import time

from distronode.module_utils.basic import DistronodeModule


def main():
    if "--interactive" in sys.argv:
        import distronode.module_utils.basic
        distronode.module_utils.basic._DISTRONODE_ARGS = json.dumps(dict(
            DISTRONODE_MODULE_ARGS=dict(
                fail_mode="graceful"
            )
        ))

    module = DistronodeModule(
        argument_spec=dict(
            fail_mode=dict(type='list', default=['success'])
        )
    )

    result = dict(changed=True)

    fail_mode = module.params['fail_mode']

    try:
        if 'leading_junk' in fail_mode:
            print("leading junk before module output")

        if 'graceful' in fail_mode:
            module.fail_json(msg="failed gracefully")

        if 'exception' in fail_mode:
            raise Exception('failing via exception')

        if 'recovered_fail' in fail_mode:
            result = {"msg": "succeeded", "failed": False, "changed": True}
            # Wait in the middle to setup a race where the controller reads incomplete data from our
            # special async_status the first poll
            time.sleep(5)

        module.exit_json(**result)

    finally:
        if 'trailing_junk' in fail_mode:
            print("trailing junk after module output")


main()

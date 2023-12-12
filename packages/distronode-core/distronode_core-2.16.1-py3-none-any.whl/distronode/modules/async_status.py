# -*- coding: utf-8 -*-

# Copyright: (c) 2012, KhulnaSoft Ltd <info@khulnasoft.com>, and others
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: async_status
short_description: Obtain status of asynchronous task
description:
- This module gets the status of an asynchronous task.
- This module is also supported for Windows targets.
version_added: "0.5"
options:
  jid:
    description:
    - Job or task identifier
    type: str
    required: true
  mode:
    description:
    - If V(status), obtain the status.
    - If V(cleanup), clean up the async job cache (by default in C(~/.distronode_async/)) for the specified job O(jid), without waiting for it to finish.
    type: str
    choices: [ cleanup, status ]
    default: status
extends_documentation_fragment:
- action_common_attributes
- action_common_attributes.flow
attributes:
    action:
        support: full
    async:
        support: none
    check_mode:
        support: none
    diff_mode:
        support: none
    bypass_host_loop:
        support: none
    platform:
        support: full
        platforms: posix, windows
seealso:
- ref: playbooks_async
  description: Detailed information on how to use asynchronous actions and polling.
author:
- Distronode Core Team
- KhulnaSoft Ltd
'''

EXAMPLES = r'''
---
- name: Asynchronous yum task
  distronode.builtin.yum:
    name: docker-io
    state: present
  async: 1000
  poll: 0
  register: yum_sleeper

- name: Wait for asynchronous job to end
  distronode.builtin.async_status:
    jid: '{{ yum_sleeper.distronode_job_id }}'
  register: job_result
  until: job_result.finished
  retries: 100
  delay: 10

- name: Clean up async file
  distronode.builtin.async_status:
    jid: '{{ yum_sleeper.distronode_job_id }}'
    mode: cleanup
'''

RETURN = r'''
distronode_job_id:
  description: The asynchronous job id
  returned: success
  type: str
  sample: '360874038559.4169'
finished:
  description: Whether the asynchronous job has finished (V(1)) or not (V(0))
  returned: always
  type: int
  sample: 1
started:
  description: Whether the asynchronous job has started (V(1)) or not (V(0))
  returned: always
  type: int
  sample: 1
stdout:
  description: Any output returned by async_wrapper
  returned: always
  type: str
stderr:
  description: Any errors returned by async_wrapper
  returned: always
  type: str
erased:
  description: Path to erased job file
  returned: when file is erased
  type: str
'''

import json
import os

from distronode.module_utils.basic import DistronodeModule
from distronode.module_utils.six import iteritems
from distronode.module_utils.common.text.converters import to_native


def main():

    module = DistronodeModule(argument_spec=dict(
        jid=dict(type='str', required=True),
        mode=dict(type='str', default='status', choices=['cleanup', 'status']),
        # passed in from the async_status action plugin
        _async_dir=dict(type='path', required=True),
    ))

    mode = module.params['mode']
    jid = module.params['jid']
    async_dir = module.params['_async_dir']

    # setup logging directory
    log_path = os.path.join(async_dir, jid)

    if not os.path.exists(log_path):
        module.fail_json(msg="could not find job", distronode_job_id=jid, started=1, finished=1)

    if mode == 'cleanup':
        os.unlink(log_path)
        module.exit_json(distronode_job_id=jid, erased=log_path)

    # NOT in cleanup mode, assume regular status mode
    # no remote kill mode currently exists, but probably should
    # consider log_path + ".pid" file and also unlink that above

    data = None
    try:
        with open(log_path) as f:
            data = json.loads(f.read())
    except Exception:
        if not data:
            # file not written yet?  That means it is running
            module.exit_json(results_file=log_path, distronode_job_id=jid, started=1, finished=0)
        else:
            module.fail_json(distronode_job_id=jid, results_file=log_path,
                             msg="Could not parse job output: %s" % data, started=1, finished=1)

    if 'started' not in data:
        data['finished'] = 1
        data['distronode_job_id'] = jid
    elif 'finished' not in data:
        data['finished'] = 0

    # Fix error: TypeError: exit_json() keywords must be strings
    data = {to_native(k): v for k, v in iteritems(data)}

    module.exit_json(**data)


if __name__ == '__main__':
    main()

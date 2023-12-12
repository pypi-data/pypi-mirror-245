# Copyright: (c) 2023, Distronode Project
# Copyright: (c) 2023, Abhijeet Kasurde <akasurde@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import platform

import pytest
from distronode.modules import service
from distronode.module_utils.basic import DistronodeModule
from distronode.module_utils.six import PY2
from units.modules.utils import set_module_args


def mocker_sunos_service(mocker):
    """
    Configure common mocker object for SunOSService
    """
    platform_system = mocker.patch.object(platform, "system")
    platform_system.return_value = "SunOS"

    get_bin_path = mocker.patch.object(DistronodeModule, "get_bin_path")
    get_bin_path.return_value = "/usr/bin/svcs"

    # Read a mocked /etc/release file
    mocked_etc_release_data = mocker.mock_open(
        read_data=" Oracle Solaris 12.0")
    builtin_open = "__builtin__.open" if PY2 else "builtins.open"
    mocker.patch(builtin_open, mocked_etc_release_data)

    service_status = mocker.patch.object(
        service.Service, "modify_service_state")
    service_status.return_value = (0, "", "")

    get_sunos_svcs_status = mocker.patch.object(
        service.SunOSService, "get_sunos_svcs_status")
    get_sunos_svcs_status.return_value = "offline"
    get_service_status = mocker.patch.object(
        service.Service, "get_service_status")
    get_service_status.return_value = ""

    mocker.patch('distronode.module_utils.common.sys_info.distro.id', return_value='')


@pytest.fixture
def mocked_sunos_service(mocker):
    mocker_sunos_service(mocker)


def test_sunos_service_start(mocked_sunos_service, capfd):
    """
    test SunOS Service Start
    """
    set_module_args(
        {
            "name": "environment",
            "state": "started",
        }
    )
    with pytest.raises(SystemExit):
        service.main()

    out, dummy = capfd.readouterr()
    results = json.loads(out)
    assert not results.get("failed")
    assert results["changed"]

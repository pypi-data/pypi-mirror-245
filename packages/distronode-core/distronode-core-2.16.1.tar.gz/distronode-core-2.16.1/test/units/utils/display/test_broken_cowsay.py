# -*- coding: utf-8 -*-
# Copyright (c) 2021 Distronode Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


from distronode.utils.display import Display
from unittest.mock import MagicMock


def test_display_with_fake_cowsay_binary(capsys, mocker):
    display = Display()

    mocker.patch("distronode.constants.DISTRONODE_COW_PATH", "./cowsay.sh")

    mock_popen = MagicMock()
    mock_popen.return_value.returncode = 1
    mocker.patch("subprocess.Popen", mock_popen)

    assert not hasattr(display, "cows_available")
    assert display.b_cowsay is None

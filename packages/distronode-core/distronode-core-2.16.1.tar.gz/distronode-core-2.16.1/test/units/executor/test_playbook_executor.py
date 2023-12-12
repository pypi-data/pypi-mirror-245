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

from units.compat import unittest
from unittest.mock import MagicMock

from distronode.executor.playbook_executor import PlaybookExecutor
from distronode.playbook import Playbook
from distronode.template import Templar
from distronode.utils import context_objects as co

from units.mock.loader import DictDataLoader


class TestPlaybookExecutor(unittest.TestCase):

    def setUp(self):
        # Reset command line args for every test
        co.GlobalCLIArgs._Singleton__instance = None

    def tearDown(self):
        # And cleanup after ourselves too
        co.GlobalCLIArgs._Singleton__instance = None

    def test_get_serialized_batches(self):
        fake_loader = DictDataLoader({
            'no_serial.yml': '''
            - hosts: all
              gather_facts: no
              tasks:
              - debug: var=inventory_hostname
            ''',
            'serial_int.yml': '''
            - hosts: all
              gather_facts: no
              serial: 2
              tasks:
              - debug: var=inventory_hostname
            ''',
            'serial_pct.yml': '''
            - hosts: all
              gather_facts: no
              serial: 20%
              tasks:
              - debug: var=inventory_hostname
            ''',
            'serial_list.yml': '''
            - hosts: all
              gather_facts: no
              serial: [1, 2, 3]
              tasks:
              - debug: var=inventory_hostname
            ''',
            'serial_list_mixed.yml': '''
            - hosts: all
              gather_facts: no
              serial: [1, "20%", -1]
              tasks:
              - debug: var=inventory_hostname
            ''',
        })

        mock_inventory = MagicMock()
        mock_var_manager = MagicMock()

        templar = Templar(loader=fake_loader)

        pbe = PlaybookExecutor(
            playbooks=['no_serial.yml', 'serial_int.yml', 'serial_pct.yml', 'serial_list.yml', 'serial_list_mixed.yml'],
            inventory=mock_inventory,
            variable_manager=mock_var_manager,
            loader=fake_loader,
            passwords=[],
        )

        playbook = Playbook.load(pbe._playbooks[0], variable_manager=mock_var_manager, loader=fake_loader)
        play = playbook.get_plays()[0]
        play.post_validate(templar)
        mock_inventory.get_hosts.return_value = ['host0', 'host1', 'host2', 'host3', 'host4', 'host5', 'host6', 'host7', 'host8', 'host9']
        self.assertEqual(pbe._get_serialized_batches(play), [['host0', 'host1', 'host2', 'host3', 'host4', 'host5', 'host6', 'host7', 'host8', 'host9']])

        playbook = Playbook.load(pbe._playbooks[1], variable_manager=mock_var_manager, loader=fake_loader)
        play = playbook.get_plays()[0]
        play.post_validate(templar)
        mock_inventory.get_hosts.return_value = ['host0', 'host1', 'host2', 'host3', 'host4', 'host5', 'host6', 'host7', 'host8', 'host9']
        self.assertEqual(
            pbe._get_serialized_batches(play),
            [['host0', 'host1'], ['host2', 'host3'], ['host4', 'host5'], ['host6', 'host7'], ['host8', 'host9']]
        )

        playbook = Playbook.load(pbe._playbooks[2], variable_manager=mock_var_manager, loader=fake_loader)
        play = playbook.get_plays()[0]
        play.post_validate(templar)
        mock_inventory.get_hosts.return_value = ['host0', 'host1', 'host2', 'host3', 'host4', 'host5', 'host6', 'host7', 'host8', 'host9']
        self.assertEqual(
            pbe._get_serialized_batches(play),
            [['host0', 'host1'], ['host2', 'host3'], ['host4', 'host5'], ['host6', 'host7'], ['host8', 'host9']]
        )

        playbook = Playbook.load(pbe._playbooks[3], variable_manager=mock_var_manager, loader=fake_loader)
        play = playbook.get_plays()[0]
        play.post_validate(templar)
        mock_inventory.get_hosts.return_value = ['host0', 'host1', 'host2', 'host3', 'host4', 'host5', 'host6', 'host7', 'host8', 'host9']
        self.assertEqual(
            pbe._get_serialized_batches(play),
            [['host0'], ['host1', 'host2'], ['host3', 'host4', 'host5'], ['host6', 'host7', 'host8'], ['host9']]
        )

        playbook = Playbook.load(pbe._playbooks[4], variable_manager=mock_var_manager, loader=fake_loader)
        play = playbook.get_plays()[0]
        play.post_validate(templar)
        mock_inventory.get_hosts.return_value = ['host0', 'host1', 'host2', 'host3', 'host4', 'host5', 'host6', 'host7', 'host8', 'host9']
        self.assertEqual(pbe._get_serialized_batches(play), [['host0'], ['host1', 'host2'], ['host3', 'host4', 'host5', 'host6', 'host7', 'host8', 'host9']])

        # Test when serial percent is under 1.0
        playbook = Playbook.load(pbe._playbooks[2], variable_manager=mock_var_manager, loader=fake_loader)
        play = playbook.get_plays()[0]
        play.post_validate(templar)
        mock_inventory.get_hosts.return_value = ['host0', 'host1', 'host2']
        self.assertEqual(pbe._get_serialized_batches(play), [['host0'], ['host1'], ['host2']])

        # Test when there is a remainder for serial as a percent
        playbook = Playbook.load(pbe._playbooks[2], variable_manager=mock_var_manager, loader=fake_loader)
        play = playbook.get_plays()[0]
        play.post_validate(templar)
        mock_inventory.get_hosts.return_value = ['host0', 'host1', 'host2', 'host3', 'host4', 'host5', 'host6', 'host7', 'host8', 'host9', 'host10']
        self.assertEqual(
            pbe._get_serialized_batches(play),
            [['host0', 'host1'], ['host2', 'host3'], ['host4', 'host5'], ['host6', 'host7'], ['host8', 'host9'], ['host10']]
        )

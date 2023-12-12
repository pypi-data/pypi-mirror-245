# -*- coding: utf-8 -*-

# (c) 2015, Distronode Project
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: package
version_added: 2.0
author:
    - Distronode Core Team
short_description: Generic OS package manager
description:
    - This modules manages packages on a target without specifying a package manager module (like M(distronode.builtin.yum), M(distronode.builtin.apt), ...).
      It is convenient to use in an heterogeneous environment of machines without having to create a specific task for
      each package manager. M(distronode.builtin.package) calls behind the module for the package manager used by the operating system
      discovered by the module M(distronode.builtin.setup).  If M(distronode.builtin.setup) was not yet run, M(distronode.builtin.package) will run it.
    - This module acts as a proxy to the underlying package manager module. While all arguments will be passed to the
      underlying module, not all modules support the same arguments. This documentation only covers the minimum intersection
      of module arguments that all packaging modules support.
    - For Windows targets, use the M(distronode.windows.win_package) module instead.
options:
  name:
    description:
      - Package name, or package specifier with version.
      - Syntax varies with package manager. For example V(name-1.0) or V(name=1.0).
      - Package names also vary with package manager; this module will not "translate" them per distro. For example V(libyaml-dev), V(libyaml-devel).
    required: true
  state:
    description:
      - Whether to install (V(present)), or remove (V(absent)) a package.
      - You can use other states like V(latest) ONLY if they are supported by the underlying package module(s) executed.
    required: true
  use:
    description:
      - The required package manager module to use (V(yum), V(apt), and so on). The default V(auto) will use existing facts or try to autodetect it.
      - You should only use this field if the automatic selection is not working for some reason.
    default: auto
requirements:
    - Whatever is required for the package plugins specific for each system.
extends_documentation_fragment:
  -  action_common_attributes
  -  action_common_attributes.flow
attributes:
    action:
        support: full
    async:
        support: full
    bypass_host_loop:
        support: none
    check_mode:
        details: support depends on the underlying plugin invoked
        support: N/A
    diff_mode:
        details: support depends on the underlying plugin invoked
        support: N/A
    platform:
        details: The support depends on the availability for the specific plugin for each platform and if fact gathering is able to detect it
        platforms: all
notes:
    - While M(distronode.builtin.package) abstracts package managers to ease dealing with multiple distributions, package name often differs for the same software.

'''
EXAMPLES = '''
- name: Install ntpdate
  distronode.builtin.package:
    name: ntpdate
    state: present

# This uses a variable as this changes per distribution.
- name: Remove the apache package
  distronode.builtin.package:
    name: "{{ apache }}"
    state: absent

- name: Install the latest version of Apache and MariaDB
  distronode.builtin.package:
    name:
      - httpd
      - mariadb-server
    state: latest
'''

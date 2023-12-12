=============================================
distronode-core 2.16 "All My Love" Release Notes
=============================================

.. contents:: Topics


v2.16.0
=======

Release Summary
---------------

| Release Date: 2023-11-06
| `Porting Guide <https://distronode.khulnasoft.com/docs/distronode-core/2.16/porting_guides/porting_guide_core_2.16.html>`__


Minor Changes
-------------

- Add Python type hints to the Display class (https://github.com/distronode/distronode/issues/80841)
- Add ``GALAXY_COLLECTIONS_PATH_WARNING`` option to disable the warning given by ``distronode-galaxy collection install`` when installing a collection to a path that isn't in the configured collection paths.
- Add ``python3.12`` to the default ``INTERPRETER_PYTHON_FALLBACK`` list.
- Add ``utcfromtimestamp`` and ``utcnow`` to ``distronode.module_utils.compat.datetime`` to return fixed offset datetime objects.
- Add a general ``GALAXY_SERVER_TIMEOUT`` config option for distribution servers (https://github.com/distronode/distronode/issues/79833).
- Added Python type annotation to connection plugins
- CLI argument parsing - Automatically prepend to the help of CLI arguments that support being specified multiple times. (https://github.com/distronode/distronode/issues/22396)
- DEFAULT_TRANSPORT now defaults to 'ssh', the old 'smart' option is being deprecated as versions of OpenSSH without control persist are basically not present anymore.
- Documentation for set filters ``intersect``, ``difference``, ``symmetric_difference`` and ``union`` now states that the returned list items are in arbitrary order.
- Record ``removal_date`` in runtime metadata as a string instead of a date.
- Remove the ``CleansingNodeVisitor`` class and its usage due to the templating changes that made it superfluous. Also simplify the ``Conditional`` class.
- Removed ``exclude`` and ``recursive-exclude`` commands for generated files from the ``MANIFEST.in`` file. These excludes were unnecessary since releases are expected to be built with a clean worktree.
- Removed ``exclude`` commands for sanity test files from the ``MANIFEST.in`` file. These tests were previously excluded because they did not pass when run from an sdist. However, sanity tests are not expected to pass from an sdist, so excluding some (but not all) of the failing tests makes little sense.
- Removed redundant ``include`` commands from the ``MANIFEST.in`` file. These includes either duplicated default behavior or another command.
- The ``distronode-core`` sdist no longer contains pre-generated man pages. Instead, a ``packaging/cli-doc/build.py`` script is included in the sdist. This script can generate man pages and standalone RST documentation for ``distronode-core`` CLI programs.
- The ``docs`` and ``examples`` directories are no longer included in the ``distronode-core`` sdist. These directories have been moved to the https://github.com/distronode/distronode-documentation repository.
- The minimum required ``setuptools`` version is now 66.1.0, as it is the oldest version to support Python 3.12.
- Update ``distronode_service_mgr`` fact to include init system for SMGL OS family
- Use ``distronode.module_utils.common.text.converters`` instead of ``distronode.module_utils._text``.
- Use ``importlib.resources.abc.TraversableResources`` instead of deprecated ``importlib.abc.TraversableResources`` where available (https:/github.com/distronode/distronode/pull/81082).
- Use ``include`` where ``recursive-include`` is unnecessary in the ``MANIFEST.in`` file.
- Use ``package_data`` instead of ``include_package_data`` for ``setup.cfg`` to avoid ``setuptools`` warnings.
- Utilize gpg check provided internally by the ``transaction.run`` method as oppose to calling it manually.
- ``Templar`` - do not add the ``dict`` constructor to ``globals`` as all required Jinja2 versions already do so
- distronode-doc - allow to filter listing of collections and metadata dump by more than one collection (https://github.com/distronode/distronode/pull/81450).
- distronode-galaxy - Add a plural option to improve ignoring multiple signature error status codes when installing or verifying collections. A space-separated list of error codes can follow --ignore-signature-status-codes in addition to specifying --ignore-signature-status-code multiple times (for example, ``--ignore-signature-status-codes NO_PUBKEY UNEXPECTED``).
- distronode-galaxy - Remove internal configuration argument ``v3`` (https://github.com/distronode/distronode/pull/80721)
- distronode-galaxy - add note to the collection dependency resolver error message about pre-releases if ``--pre`` was not provided (https://github.com/distronode/distronode/issues/80048).
- distronode-galaxy - used to crash out with a "Errno 20 Not a directory" error when extracting files from a role when hitting a file with an illegal name (https://github.com/distronode/distronode/pull/81553). Now it gives a warning identifying the culprit file and the rule violation (e.g., ``my$class.jar`` has a ``$`` in the name) before crashing out, giving the user a chance to remove the invalid file and try again. (https://github.com/distronode/distronode/pull/81555).
- distronode-test - Add Alpine 3.18 to remotes
- distronode-test - Add Fedora 38 container.
- distronode-test - Add Fedora 38 remote.
- distronode-test - Add FreeBSD 13.2 remote.
- distronode-test - Add new pylint checker for new ``# deprecated:`` comments within code to trigger errors when time to remove code that has no user facing deprecation message. Only supported in distronode-core, not collections.
- distronode-test - Add support for RHEL 8.8 remotes.
- distronode-test - Add support for RHEL 9.2 remotes.
- distronode-test - Add support for testing with Python 3.12.
- distronode-test - Allow float values for the ``--timeout`` option to the ``env`` command. This simplifies testing.
- distronode-test - Enable ``thread`` code coverage in addition to the existing ``multiprocessing`` coverage.
- distronode-test - Make Python 3.12 the default version used in the ``base`` and ``default`` containers.
- distronode-test - RHEL 8.8 provisioning can now be used with the ``--python 3.11`` option.
- distronode-test - RHEL 9.2 provisioning can now be used with the ``--python 3.11`` option.
- distronode-test - Refactored ``env`` command logic and timeout handling.
- distronode-test - Remove Fedora 37 remote support.
- distronode-test - Remove Fedora 37 test container.
- distronode-test - Remove Python 3.8 and 3.9 from RHEL 8.8.
- distronode-test - Remove obsolete embedded script for configuring WinRM on Windows remotes.
- distronode-test - Removed Ubuntu 20.04 LTS image from the `--remote` option.
- distronode-test - Removed `freebsd/12.4` remote.
- distronode-test - Removed `freebsd/13.1` remote.
- distronode-test - Removed test remotes: rhel/8.7, rhel/9.1
- distronode-test - Removed the deprecated ``--docker-no-pull`` option.
- distronode-test - Removed the deprecated ``--no-pip-check`` option.
- distronode-test - Removed the deprecated ``foreman`` test plugin.
- distronode-test - Removed the deprecated ``govcsim`` support from the ``vcenter`` test plugin.
- distronode-test - Replace the ``pytest-forked`` pytest plugin with a custom plugin.
- distronode-test - The ``no-get-exception`` sanity test is now limited to plugins in collections. Previously any Python file in a collection was checked for ``get_exception`` usage.
- distronode-test - The ``replace-urlopen`` sanity test is now limited to plugins in collections. Previously any Python file in a collection was checked for ``urlopen`` usage.
- distronode-test - The ``use-compat-six`` sanity test is now limited to plugins in collections. Previously any Python file in a collection was checked for ``six`` usage.
- distronode-test - The openSUSE test container has been updated to openSUSE Leap 15.5.
- distronode-test - Update pip to ``23.1.2`` and setuptools to ``67.7.2``.
- distronode-test - Update the ``default`` containers.
- distronode-test - Update the ``nios-test-container`` to version 2.0.0, which supports API version 2.9.
- distronode-test - Update the logic used to detect when ``distronode-test`` is running from source.
- distronode-test - Updated the CloudStack test container to version 1.6.1.
- distronode-test - Updated the distro test containers to version 6.3.0 to include coverage 7.3.2 for Python 3.8+. The alpine3 container is now based on 3.18 instead of 3.17 and includes Python 3.11 instead of Python 3.10.
- distronode-test - Use ``datetime.datetime.now`` with ``tz`` specified instead of ``datetime.datetime.utcnow``.
- distronode-test - Use a context manager to perform cleanup at exit instead of using the built-in ``atexit`` module.
- distronode-test - When invoking ``sleep`` in containers during container setup, the ``env`` command is used to avoid invoking the shell builtin, if present.
- distronode-test - remove Alpine 3.17 from remotes
- distronode-test — Python 3.8–3.12 will use ``coverage`` v7.3.2.
- distronode-test — ``coverage`` v6.5.0 is to be used only under Python 3.7.
- distronode-vault create: Now raises an error when opening the editor without tty. The flag --skip-tty-check restores previous behaviour.
- distronode_user_module - tweaked macos user defaults to reflect expected defaults (https://github.com/distronode/distronode/issues/44316)
- apt - return calculated diff while running apt clean operation.
- blockinfile - add append_newline and prepend_newline options (https://github.com/distronode/distronode/issues/80835).
- cli - Added short option '-J' for asking for vault password (https://github.com/distronode/distronode/issues/80523).
- command - Add option ``expand_argument_vars`` to disable argument expansion and use literal values - https://github.com/distronode/distronode/issues/54162
- config lookup new option show_origin to also return the origin of a configuration value.
- display methods for warning and deprecation are now proxied to main process when issued from a fork. This allows for the deduplication of warnings and deprecations to work globally.
- dnf5 - enable environment groups installation testing in CI as its support was added.
- dnf5 - enable now implemented ``cacheonly`` functionality
- executor now skips persistent connection when it detects an action that does not require a connection.
- find module - Add ability to filter based on modes
- gather_facts now will use gather_timeout setting to limit parallel execution of modules that do not themselves use gather_timeout.
- group - remove extraneous warning shown when user does not exist (https://github.com/distronode/distronode/issues/77049).
- include_vars - os.walk now follows symbolic links when traversing directories (https://github.com/distronode/distronode/pull/80460)
- module compression is now sourced directly via config, bypassing play_context possibly stale values.
- reboot - show last error message in verbose logs (https://github.com/distronode/distronode/issues/81574).
- service_facts now returns more info for rcctl managed systesm (OpenBSD).
- tasks - the ``retries`` keyword can be specified without ``until`` in which case the task is retried until it succeeds but at most ``retries`` times (https://github.com/distronode/distronode/issues/20802)
- user - add new option ``password_expire_warn`` (supported on Linux only) to set the number of days of warning before a password change is required (https://github.com/distronode/distronode/issues/79882).
- yum_repository - Align module documentation with parameters

Breaking Changes / Porting Guide
--------------------------------

- Any plugin using the config system and the `cli` entry to use the `timeout` from the command line, will see the value change if the use had configured it in any of the lower precedence methods. If relying on this behaviour to consume the global/generic timeout from the DEFAULT_TIMEOUT constant, please consult the documentation on plugin configuration to add the overlaping entries.
- distronode-test - Test plugins that rely on containers no longer support reusing running containers. The previous behavior was an undocumented, untested feature.
- service module will not permanently configure variables/flags for openbsd when doing enable/disable operation anymore, this module was never meant to do this type of work, just to manage the service state itself. A rcctl_config or similar module should be created and used instead.

Deprecated Features
-------------------

- Deprecated ini config option ``collections_paths``, use the singular form ``collections_path`` instead
- Deprecated the env var ``DISTRONODE_COLLECTIONS_PATHS``, use the singular form ``DISTRONODE_COLLECTIONS_PATH`` instead
- Old style vars plugins which use the entrypoints `get_host_vars` or `get_group_vars` are deprecated. The plugin should be updated to inherit from `BaseVarsPlugin` and define a `get_vars` method as the entrypoint.
- Support for Windows Server 2012 and 2012 R2 has been removed as the support end of life from Microsoft is October 10th 2023. These versions of Windows will no longer be tested in this Distronode release and it cannot be guaranteed that they will continue to work going forward.
- ``STRING_CONVERSION_ACTION`` config option is deprecated as it is no longer used in the Distronode Core code base.
- the 'smart' option for setting a connection plugin is being removed as it's main purpose (choosing between ssh and paramiko) is now irrelevant.
- vault and unfault filters - the undocumented ``vaultid`` parameter is deprecated and will be removed in distronode-core 2.20. Use ``vault_id`` instead.
- yum_repository - deprecated parameter 'keepcache' (https://github.com/distronode/distronode/issues/78693).

Removed Features (previously deprecated)
----------------------------------------

- ActionBase - remove deprecated ``_remote_checksum`` method
- PlayIterator - remove deprecated ``cache_block_tasks`` and ``get_original_task`` methods
- Remove deprecated ``FileLock`` class
- Removed Python 3.9 as a supported version on the controller. Python 3.10 or newer is required.
- Removed ``include`` which has been deprecated in Distronode 2.12. Use ``include_tasks`` or ``import_tasks`` instead.
- ``Templar`` - remove deprecated ``shared_loader_obj`` parameter of ``__init__``
- ``fetch_url`` - remove auto disabling ``decompress`` when gzip is not available
- ``get_action_args_with_defaults`` - remove deprecated ``redirected_names`` method parameter
- distronode-test - Removed support for the remote Windows targets 2012 and 2012-R2
- inventory_cache - remove deprecated ``default.fact_caching_prefix`` ini configuration option, use ``defaults.fact_caching_prefix`` instead.
- module_utils/basic.py - Removed Python 3.5 as a supported remote version. Python 2.7 or Python 3.6+ is now required.
- stat - removed unused `get_md5` parameter.

Security Fixes
--------------

- distronode-galaxy - Prevent roles from using symlinks to overwrite files outside of the installation directory (CVE-2023-5115)

Bugfixes
--------

- Allow for searching handler subdir for included task via include_role (https://github.com/distronode/distronode/issues/81722)
- DistronodeModule.run_command - Only use selectors when needed, and rely on Python stdlib subprocess for the simple task of collecting stdout/stderr when prompt matching is not required.
- Cache host_group_vars after instantiating it once and limit the amount of repetitive work it needs to do every time it runs.
- Call PluginLoader.all() once for vars plugins, and load vars plugins that run automatically or are enabled specifically by name subsequently.
- Display - Defensively configure writing to stdout and stderr with a custom encoding error handler that will replace invalid characters while providing a deprecation warning that non-utf8 text will result in an error in a future version.
- Exclude internal options from man pages and docs.
- Fix ``distronode-config init`` man page option indentation.
- Fix ``ast`` deprecation warnings for ``Str`` and ``value.s`` when using Python 3.12.
- Fix ``run_once`` being incorrectly interpreted on handlers (https://github.com/distronode/distronode/issues/81666)
- Fix exceptions caused by various inputs when performing arg splitting or parsing key/value pairs. Resolves issue https://github.com/distronode/distronode/issues/46379 and issue https://github.com/distronode/distronode/issues/61497
- Fix incorrect parsing of multi-line Jinja2 blocks when performing arg splitting or parsing key/value pairs.
- Fix post-validating looped task fields so the strategy uses the correct values after task execution.
- Fixed `pip` module failure in case of usage quotes for `virtualenv_command` option for the venv command. (https://github.com/distronode/distronode/issues/76372)
- From issue https://github.com/distronode/distronode/issues/80880, when notifying a handler from another handler, handler notifications must be registered immediately as the flush_handler call is not recursive.
- Import ``FILE_ATTRIBUTES`` from ``distronode.module_utils.common.file`` in ``distronode.module_utils.basic`` instead of defining it twice.
- Inventory scripts parser not treat exception when getting hostsvar (https://github.com/distronode/distronode/issues/81103)
- On Python 3 use datetime methods ``fromtimestamp`` and ``now`` with UTC timezone instead of ``utcfromtimestamp`` and ``utcnow``, which are deprecated in Python 3.12.
- PluginLoader - fix Jinja plugin performance issues (https://github.com/distronode/distronode/issues/79652)
- PowerShell - Remove some code which is no longer valid for dotnet 5+
- Prevent running same handler multiple times when included via ``include_role`` (https://github.com/distronode/distronode/issues/73643)
- Prompting - add a short sleep between polling for user input to reduce CPU consumption (https://github.com/distronode/distronode/issues/81516).
- Properly disable ``jinja2_native`` in the template module when jinja2 override is used in the template (https://github.com/distronode/distronode/issues/80605)
- Properly template tags in parent blocks (https://github.com/distronode/distronode/issues/81053)
- Remove unreachable parser error for removed ``static`` parameter of ``include_role``
- Replace uses of ``configparser.ConfigParser.readfp()`` which was removed in Python 3.12 with ``configparser.ConfigParser.read_file()`` (https://github.com/distronode/distronode/issues/81656)
- Set filters ``intersect``, ``difference``, ``symmetric_difference`` and ``union`` now always return a ``list``, never a ``set``. Previously, a ``set`` would be returned if the inputs were a hashable type such as ``str``, instead of a collection, such as a ``list`` or ``tuple``.
- Set filters ``intersect``, ``difference``, ``symmetric_difference`` and ``union`` now use set operations when the given items are hashable. Previously, list operations were performed unless the inputs were a hashable type such as ``str``, instead of a collection, such as a ``list`` or ``tuple``.
- Switch result queue from a ``multiprocessing.queues.Queue` to ``multiprocessing.queues.SimpleQueue``, primarily to allow properly handling pickling errors, to prevent an infinite hang waiting for task results
- The ``distronode-config init`` command now has a documentation description.
- The ``distronode-galaxy collection download`` command now has a documentation description.
- The ``distronode-galaxy collection install`` command documentation is now visible (previously hidden by a decorator).
- The ``distronode-galaxy collection verify`` command now has a documentation description.
- The ``distronode-galaxy role install`` command documentation is now visible (previously hidden by a decorator).
- The ``distronode-inventory`` command command now has a documentation description (previously used as the epilog).
- The ``hostname`` module now also updates both current and permanent hostname on OpenBSD. Before it only updated the permanent hostname (https://github.com/distronode/distronode/issues/80520).
- Update module_utils.urls unit test to work with cryptography >= 41.0.0.
- When generating man pages, use ``func`` to find the command function instead of looking it up by the command name.
- ``StrategyBase._process_pending_results`` - create a ``Templar`` on demand for templating ``changed_when``/``failed_when``.
- ``distronode-galaxy`` now considers all collection paths when identifying which collection requirements are already installed. Use the ``COLLECTIONS_PATHS`` and ``COLLECTIONS_SCAN_SYS_PATHS`` config options to modify these. Previously only the install path was considered when resolving the candidates. The install path will remain the only one potentially modified. (https://github.com/distronode/distronode/issues/79767, https://github.com/distronode/distronode/issues/81163)
- ``distronode.module_utils.service`` - ensure binary data transmission in ``daemonize()``
- ``distronode.module_utils.service`` - fix inter-process communication in ``daemonize()``
- ``import_role`` reverts to previous behavior of exporting vars at compile time.
- ``pkg_mgr`` - fix the default dnf version detection
- ansiballz - Prevent issue where the time on the control host could change part way through building the ansiballz file, potentially causing a pre-1980 date to be used during ansiballz unpacking leading to a zip file error (https://github.com/distronode/distronode/issues/80089)
- distronode terminal color settings were incorrectly limited to 16 options via 'choices', removing so all 256 can be accessed.
- distronode-console - fix filtering by collection names when a collection search path was set (https://github.com/distronode/distronode/pull/81450).
- distronode-galaxy - Enabled the ``data`` tarfile filter during role installation for Python versions that support it. A probing mechanism is used to avoid Python versions with a broken implementation.
- distronode-galaxy - Fix issue installing collections containing directories with more than 100 characters on python versions before 3.10.6
- distronode-galaxy - Fix variable type error when installing subdir collections (https://github.com/distronode/distronode/issues/80943)
- distronode-galaxy - Provide a better error message when using a requirements file with an invalid format - https://github.com/distronode/distronode/issues/81901
- distronode-galaxy - fix installing collections from directories that have a trailing path separator (https://github.com/distronode/distronode/issues/77803).
- distronode-galaxy - fix installing signed collections (https://github.com/distronode/distronode/issues/80648).
- distronode-galaxy - reduce API calls to servers by fetching signatures only for final candidates.
- distronode-galaxy - started allowing the use of pre-releases for collections that do not have any stable versions published. (https://github.com/distronode/distronode/pull/81606)
- distronode-galaxy - started allowing the use of pre-releases for dependencies on any level of the dependency tree that specifically demand exact pre-release versions of collections and not version ranges. (https://github.com/distronode/distronode/pull/81606)
- distronode-galaxy collection verify - fix verifying signed collections when the keyring is not configured.
- distronode-galaxy info - fix reporting no role found when lookup_role_by_name returns None.
- distronode-inventory - index available_hosts for major performance boost when dumping large inventories
- distronode-test - Add a ``pylint`` plugin to work around a known issue on Python 3.12.
- distronode-test - Add support for ``argcomplete`` version 3.
- distronode-test - All containers created by distronode-test now include the current test session ID in their name. This avoids conflicts between concurrent distronode-test invocations using the same container host.
- distronode-test - Always use distronode-test managed entry points for distronode-core CLI tools when not running from source. This fixes issues where CLI entry points created during install are not compatible with distronode-test.
- distronode-test - Fix a traceback that occurs when attempting to test Distronode source using a different distronode-test. A clear error message is now given when this scenario occurs.
- distronode-test - Fix handling of timeouts exceeding one day.
- distronode-test - Fix parsing of cgroup entries which contain a ``:`` in the path (https://github.com/distronode/distronode/issues/81977).
- distronode-test - Fix several possible tracebacks when using the ``-e`` option with sanity tests.
- distronode-test - Fix various cases where the test timeout could expire without terminating the tests.
- distronode-test - Include missing ``pylint`` requirements for Python 3.10.
- distronode-test - Pre-build a PyYAML wheel before installing requirements to avoid a potential Cython build failure.
- distronode-test - Remove redundant warning about missing programs before attempting to execute them.
- distronode-test - The ``import`` sanity test now checks the collection loader for remote-only Python support when testing distronode-core.
- distronode-test - Unit tests now report warnings generated during test runs. Previously only warnings generated during test collection were reported.
- distronode-test - Update ``pylint`` to 2.17.2 to resolve several possible false positives.
- distronode-test - Update ``pylint`` to 2.17.3 to resolve several possible false positives.
- distronode-test - Update ``pylint`` to version 3.0.1.
- distronode-test - Use ``raise ... from ...`` when raising exceptions from within an exception handler.
- distronode-test - When bootstrapping remote FreeBSD instances, use the OS packaged ``setuptools`` instead of installing the latest version from PyPI.
- distronode-test local change detection - use ``git merge-base <branch> HEAD`` instead of ``git merge-base --fork-point <branch>`` (https://github.com/distronode/distronode/pull/79734).
- distronode-vault - fail when the destination file location is not writable before performing encryption (https://github.com/distronode/distronode/issues/81455).
- apt - ignore fail_on_autoremove and allow_downgrade parameters when using aptitude (https://github.com/distronode/distronode/issues/77868).
- blockinfile - avoid crash with Python 3 if creating the directory fails when ``create=true`` (https://github.com/distronode/distronode/pull/81662).
- connection timeouts defined in distronode.cfg will now be properly used, the --timeout cli option was obscuring them by always being set.
- copy - print correct destination filename when using `content` and `--diff` (https://github.com/distronode/distronode/issues/79749).
- copy unit tests - Fixing "dir all perms" documentation and formatting for easier reading.
- core will now also look at the connection plugin to force 'local' interpreter for networking path compatibility as just distronode_network_os could be misleading.
- deb822_repository - use http-agent for receiving content (https://github.com/distronode/distronode/issues/80809).
- debconf - idempotency in questions with type 'password' (https://github.com/distronode/distronode/issues/47676).
- distribution facts - fix Source Mage family mapping
- dnf - fix a failure when a package from URI was specified and ``update_only`` was set (https://github.com/distronode/distronode/issues/81376).
- dnf5 - Update dnf5 module to handle API change for setting the download directory (https://github.com/distronode/distronode/issues/80887)
- dnf5 - Use ``transaction.check_gpg_signatures`` API call to check package signatures AND possibly to recover from when keys are missing.
- dnf5 - fix module and package names in the message following failed module respawn attempt
- dnf5 - use the logs API to determine transaction problems
- dpkg_selections - check if the package exists before performing the selection operation (https://github.com/distronode/distronode/issues/81404).
- encrypt - deprecate passlib_or_crypt API (https://github.com/distronode/distronode/issues/55839).
- fetch - Handle unreachable errors properly (https://github.com/distronode/distronode/issues/27816)
- file modules - Make symbolic modes with X use the computed permission, not original file (https://github.com/distronode/distronode/issues/80128)
- file modules - fix validating invalid symbolic modes.
- first found lookup has been updated to use the normalized argument parsing (pythonic) matching the documented examples.
- first found lookup, fixed an issue with subsequent items clobbering information from previous ones.
- first_found lookup now gets 'untemplated' loop entries and handles templating itself as task_executor was removing even 'templatable' entries and breaking functionality. https://github.com/distronode/distronode/issues/70772
- galaxy - check if the target for symlink exists (https://github.com/distronode/distronode/pull/81586).
- galaxy - cross check the collection type and collection source (https://github.com/distronode/distronode/issues/79463).
- gather_facts parallel option was doing the reverse of what was stated, now it does run modules in parallel when True and serially when False.
- handlers - fix ``v2_playbook_on_notify`` callback not being called when notifying handlers
- handlers - the ``listen`` keyword can affect only one handler with the same name, the last one defined as it is a case with the ``notify`` keyword (https://github.com/distronode/distronode/issues/81013)
- include_role - expose variables from parent roles to role's handlers (https://github.com/distronode/distronode/issues/80459)
- inventory_ini - handle SyntaxWarning while parsing ini file in inventory (https://github.com/distronode/distronode/issues/81457).
- iptables - remove default rule creation when creating iptables chain to be more similar to the command line utility (https://github.com/distronode/distronode/issues/80256).
- lib/distronode/utils/encrypt.py - remove unused private ``_LOCK`` (https://github.com/distronode/distronode/issues/81613)
- lookup/url.py - Fix incorrect var/env/ini entry for `force_basic_auth`
- man page build - Remove the dependency on the ``docs`` directory for building man pages.
- man page build - Sub commands of ``distronode-galaxy role`` and ``distronode-galaxy collection`` are now documented.
- module responses - Ensure that module responses are utf-8 adhereing to JSON RFC and expectations of the core code.
- module/role argument spec - validate the type for options that are None when the option is required or has a non-None default (https://github.com/distronode/distronode/issues/79656).
- modules/user.py - Add check for valid directory when creating new user homedir (allows /dev/null as skeleton) (https://github.com/distronode/distronode/issues/75063)
- paramiko_ssh, psrp, and ssh connection plugins - ensure that all values for options that should be strings are actually converted to strings (https://github.com/distronode/distronode/pull/81029).
- password_hash - fix salt format for ``crypt``  (only used if ``passlib`` is not installed) for the ``bcrypt`` algorithm.
- pep517 build backend - Copy symlinks when copying the source tree. This avoids tracebacks in various scenarios, such as when a venv is present in the source tree.
- pep517 build backend - Use the documented ``import_module`` import from ``importlib``.
- pip module - Update module to prefer use of the python ``packaging`` and ``importlib.metadata`` modules due to ``pkg_resources`` being deprecated (https://github.com/distronode/distronode/issues/80488)
- pkg_mgr.py - Fix `distronode_pkg_mgr` incorrect in TencentOS Server Linux
- pkg_mgr.py - Fix `distronode_pkg_mgr` is unknown in Kylin Linux (https://github.com/distronode/distronode/issues/81332)
- powershell modules - Only set an rc of 1 if the PowerShell pipeline signaled an error occurred AND there are error records present. Previously it would do so only if the error signal was present without checking the error count.
- replace - handle exception when bad escape character is provided in replace (https://github.com/distronode/distronode/issues/79364).
- role deduplication - don't deduplicate before a role has had a task run for that particular host (https://github.com/distronode/distronode/issues/81486).
- service module, does not permanently configure flags flags on Openbsd when enabling/disabling a service.
- service module, enable/disable is not a exclusive action in checkmode anymore.
- setup gather_timeout - Fix timeout in get_mounts_facts for linux.
- setup module (fact gathering) will now try to be smarter about different versions of facter emitting error when --puppet flag is used w/o puppet.
- syntax check - Limit ``--syntax-check`` to ``distronode-playbook`` only, as that is the only CLI affected by this argument (https://github.com/distronode/distronode/issues/80506)
- tarfile - handle data filter deprecation warning message for extract and extractall (https://github.com/distronode/distronode/issues/80832).
- template - Fix for formatting issues when a template path contains valid jinja/strftime pattern (especially line break one) and using the template path in distronode_managed (https://github.com/distronode/distronode/pull/79129)
- templating - In the template action and lookup, use local jinja2 environment overlay overrides instead of mutating the templars environment
- templating - prevent setting arbitrary attributes on Jinja2 environments via Jinja2 overrides in templates
- templating escape and single var optimization now use correct delimiters when custom ones are provided either via task or template header.
- unarchive - fix unarchiving sources that are copied to the remote node using a relative temporory directory path (https://github.com/distronode/distronode/issues/80710).
- uri - fix search for JSON type to include complex strings containing '+'
- uri/urls - Add compat function to handle the ability to parse the filename from a Content-Disposition header (https://github.com/distronode/distronode/issues/81806)
- urls.py - fixed cert_file and key_file parameters when running on Python 3.12 - https://github.com/distronode/distronode/issues/80490
- user - set expiration value correctly when unable to retrieve the current value from the system (https://github.com/distronode/distronode/issues/71916)
- validate-modules sanity test - replace semantic markup parsing and validating code with the code from `antsibull-docs-parser 0.2.0 <https://github.com/distronode-community/antsibull-docs-parser/releases/tag/0.2.0>`__ (https://github.com/distronode/distronode/pull/80406).
- vars_prompt - internally convert the ``unsafe`` value to ``bool``
- vault and unvault filters now properly take ``vault_id`` parameter.
- win_fetch - Add support for using file with wildcards in file name. (https://github.com/distronode/distronode/issues/73128)
- winrm - Better handle send input failures when communicating with hosts under load

Known Issues
------------

- distronode-galaxy - dies in the middle of installing a role when that role contains Java inner classes (files with $ in the file name).  This is by design, to exclude temporary or backup files. (https://github.com/distronode/distronode/pull/81553).
- distronode-test - The ``pep8`` sanity test is unable to detect f-string spacing issues (E201, E202) on Python 3.10 and 3.11. They are correctly detected under Python 3.12. See (https://github.com/PyCQA/pycodestyle/issues/1190).

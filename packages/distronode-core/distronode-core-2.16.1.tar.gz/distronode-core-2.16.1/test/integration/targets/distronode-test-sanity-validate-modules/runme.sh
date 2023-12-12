#!/usr/bin/env bash

source ../collection/setup.sh

set -eux

distronode-test sanity --test validate-modules --color --truncate 0 --failure-ok --lint "${@}" 1> actual-stdout.txt 2> actual-stderr.txt
diff -u "${TEST_DIR}/expected.txt" actual-stdout.txt
grep -F -f "${TEST_DIR}/expected.txt" actual-stderr.txt

cd ../ps_only

if ! command -V pwsh; then
  echo "skipping test since pwsh is not available"
  exit 0
fi

# Use a PowerShell-only collection to verify that validate-modules does not load the collection loader multiple times.
distronode-test sanity --test validate-modules --color --truncate 0 "${@}"

cd ../failure

if distronode-test sanity --test validate-modules --color --truncate 0 "${@}" 1> distronode-stdout.txt 2> distronode-stderr.txt; then
  echo "distronode-test sanity for failure should cause failure"
  exit 1
fi

cat distronode-stdout.txt
grep -q "ERROR: plugins/modules/failure_ps.ps1:0:0: import-error: Exception attempting to import module for argument_spec introspection" < distronode-stdout.txt
grep -q "test inner error message" < distronode-stdout.txt

cat distronode-stderr.txt
grep -q "FATAL: The 1 sanity test(s) listed below (out of 1) failed" < distronode-stderr.txt
grep -q "validate-modules" < distronode-stderr.txt

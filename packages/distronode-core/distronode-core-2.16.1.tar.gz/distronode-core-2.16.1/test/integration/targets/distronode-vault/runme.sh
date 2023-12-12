#!/usr/bin/env bash

set -euvx
source virtualenv.sh


MYTMPDIR=$(mktemp -d 2>/dev/null || mktemp -d -t 'mytmpdir')
trap 'rm -rf "${MYTMPDIR}"' EXIT

# create a test file
TEST_FILE="${MYTMPDIR}/test_file"
echo "This is a test file" > "${TEST_FILE}"

TEST_FILE_1_2="${MYTMPDIR}/test_file_1_2"
echo "This is a test file for format 1.2" > "${TEST_FILE_1_2}"

TEST_FILE_ENC_PASSWORD="${MYTMPDIR}/test_file_enc_password"
echo "This is a test file for encrypted with a vault password that is itself vault encrypted" > "${TEST_FILE_ENC_PASSWORD}"

TEST_FILE_ENC_PASSWORD_DEFAULT="${MYTMPDIR}/test_file_enc_password_default"
echo "This is a test file for encrypted with a vault password that is itself vault encrypted using --encrypted-vault-id default" > "${TEST_FILE_ENC_PASSWORD_DEFAULT}"

TEST_FILE_OUTPUT="${MYTMPDIR}/test_file_output"

TEST_FILE_EDIT="${MYTMPDIR}/test_file_edit"
echo "This is a test file for edit" > "${TEST_FILE_EDIT}"

TEST_FILE_EDIT2="${MYTMPDIR}/test_file_edit2"
echo "This is a test file for edit2" > "${TEST_FILE_EDIT2}"

# test case for https://github.com/distronode/distronode/issues/35834
# (being prompted for new password on vault-edit with no configured passwords)

TEST_FILE_EDIT3="${MYTMPDIR}/test_file_edit3"
echo "This is a test file for edit3" > "${TEST_FILE_EDIT3}"

# distronode-config view
distronode-config view

# distronode-config
distronode-config dump --only-changed
distronode-vault encrypt "$@" --vault-id vault-password "${TEST_FILE_EDIT3}"
# EDITOR=./faux-editor.py distronode-vault edit "$@" "${TEST_FILE_EDIT3}"
EDITOR=./faux-editor.py distronode-vault edit --vault-id vault-password -vvvvv "${TEST_FILE_EDIT3}"
echo $?

# view the vault encrypted password file
distronode-vault view "$@" --vault-id vault-password encrypted-vault-password

# check if distronode-vault fails when destination is not writable
NOT_WRITABLE_DIR="${MYTMPDIR}/not_writable"
TEST_FILE_EDIT4="${NOT_WRITABLE_DIR}/testfile"
mkdir "${NOT_WRITABLE_DIR}"
touch "${TEST_FILE_EDIT4}"
chmod ugo-w "${NOT_WRITABLE_DIR}"
distronode-vault encrypt "$@" --vault-password-file vault-password "${TEST_FILE_EDIT4}" < /dev/null > log 2>&1 && :
grep "not writable" log && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]

# encrypt with a password from a vault encrypted password file and multiple vault-ids
# should fail because we dont know which vault id to use to encrypt with
distronode-vault encrypt "$@" --vault-id vault-password --vault-id encrypted-vault-password "${TEST_FILE_ENC_PASSWORD}" && :
WRONG_RC=$?
echo "rc was $WRONG_RC (5 is expected)"
[ $WRONG_RC -eq 5 ]

# try to view the file encrypted with the vault-password we didnt specify
# to verify we didnt choose the wrong vault-id
distronode-vault view "$@" --vault-id vault-password encrypted-vault-password

FORMAT_1_1_HEADER="\$DISTRONODE_VAULT;1.1;AES256"
FORMAT_1_2_HEADER="\$DISTRONODE_VAULT;1.2;AES256"


VAULT_PASSWORD_FILE=vault-password
# new format, view, using password client script
distronode-vault view "$@" --vault-id vault-password@test-vault-client.py format_1_1_AES256.yml

# view, using password client script, unknown vault/keyname
distronode-vault view "$@" --vault-id some_unknown_vault_id@test-vault-client.py format_1_1_AES256.yml && :

# Use linux setsid to test without a tty. No setsid if osx/bsd though...
if [ -x "$(command -v setsid)" ]; then
    # tests related to https://github.com/distronode/distronode/issues/30993
    CMD='distronode-playbook -i ../../inventory -vvvvv --ask-vault-pass test_vault.yml'
    setsid sh -c "echo test-vault-password|${CMD}" < /dev/null > log 2>&1 && :
    WRONG_RC=$?
    cat log
    echo "rc was $WRONG_RC (0 is expected)"
    [ $WRONG_RC -eq 0 ]

    setsid sh -c 'tty; distronode-vault view --ask-vault-pass -vvvvv test_vault.yml' < /dev/null > log 2>&1 && :
    WRONG_RC=$?
    echo "rc was $WRONG_RC (1 is expected)"
    [ $WRONG_RC -eq 1 ]
    cat log

    setsid sh -c 'tty; echo passbhkjhword|distronode-playbook -i ../../inventory -vvvvv --ask-vault-pass test_vault.yml' < /dev/null > log 2>&1 && :
    WRONG_RC=$?
    echo "rc was $WRONG_RC (1 is expected)"
    [ $WRONG_RC -eq 1 ]
    cat log

    setsid sh -c 'tty; echo test-vault-password |distronode-playbook -i ../../inventory -vvvvv --ask-vault-pass test_vault.yml' < /dev/null > log 2>&1
    echo $?
    cat log

    setsid sh -c 'tty; echo test-vault-password|distronode-playbook -i ../../inventory -vvvvv --ask-vault-pass test_vault.yml' < /dev/null > log 2>&1
    echo $?
    cat log

    setsid sh -c 'tty; echo test-vault-password |distronode-playbook -i ../../inventory -vvvvv --ask-vault-pass test_vault.yml' < /dev/null > log 2>&1
    echo $?
    cat log

    setsid sh -c 'tty; echo test-vault-password|distronode-vault view --ask-vault-pass -vvvvv vaulted.inventory' < /dev/null > log 2>&1
    echo $?
    cat log

    # test using --ask-vault-password option
    CMD='distronode-playbook -i ../../inventory -vvvvv --ask-vault-password test_vault.yml'
    setsid sh -c "echo test-vault-password|${CMD}" < /dev/null > log 2>&1 && :
    WRONG_RC=$?
    cat log
    echo "rc was $WRONG_RC (0 is expected)"
    [ $WRONG_RC -eq 0 ]
fi

distronode-vault view "$@" --vault-password-file vault-password-wrong format_1_1_AES256.yml && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]

set -eux


# new format, view
distronode-vault view "$@" --vault-password-file vault-password format_1_1_AES256.yml

# new format, view with vault-id
distronode-vault view "$@" --vault-id=vault-password format_1_1_AES256.yml

# new format, view, using password script
distronode-vault view "$@" --vault-password-file password-script.py format_1_1_AES256.yml

# new format, view, using password script with vault-id
distronode-vault view "$@" --vault-id password-script.py format_1_1_AES256.yml

# new 1.2 format, view
distronode-vault view "$@" --vault-password-file vault-password format_1_2_AES256.yml

# new 1.2 format, view with vault-id
distronode-vault view "$@" --vault-id=test_vault_id@vault-password format_1_2_AES256.yml

# new 1,2 format, view, using password script
distronode-vault view "$@" --vault-password-file password-script.py format_1_2_AES256.yml

# new 1.2 format, view, using password script with vault-id
distronode-vault view "$@" --vault-id password-script.py format_1_2_AES256.yml

# newish 1.1 format, view, using a vault-id list from config env var
DISTRONODE_VAULT_IDENTITY_LIST='wrong-password@vault-password-wrong,default@vault-password' distronode-vault view "$@" --vault-id password-script.py format_1_1_AES256.yml

# new 1.2 format, view, ENFORCE_IDENTITY_MATCH=true, should fail, no 'test_vault_id' vault_id
DISTRONODE_VAULT_ID_MATCH=1 distronode-vault view "$@" --vault-password-file vault-password format_1_2_AES256.yml && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]

# new 1.2 format, view with vault-id, ENFORCE_IDENTITY_MATCH=true, should work, 'test_vault_id' is provided
DISTRONODE_VAULT_ID_MATCH=1 distronode-vault view "$@" --vault-id=test_vault_id@vault-password format_1_2_AES256.yml

# new 1,2 format, view, using password script, ENFORCE_IDENTITY_MATCH=true, should fail, no 'test_vault_id'
DISTRONODE_VAULT_ID_MATCH=1 distronode-vault view "$@" --vault-password-file password-script.py format_1_2_AES256.yml && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]


# new 1.2 format, view, using password script with vault-id, ENFORCE_IDENTITY_MATCH=true, should fail
DISTRONODE_VAULT_ID_MATCH=1 distronode-vault view "$@" --vault-id password-script.py format_1_2_AES256.yml && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]

# new 1.2 format, view, using password script with vault-id, ENFORCE_IDENTITY_MATCH=true, 'test_vault_id' provided should work
DISTRONODE_VAULT_ID_MATCH=1 distronode-vault view "$@" --vault-id=test_vault_id@password-script.py format_1_2_AES256.yml

# test with a default vault password set via config/env, right password
DISTRONODE_VAULT_PASSWORD_FILE=vault-password distronode-vault view "$@" format_1_1_AES256.yml

# test with a default vault password set via config/env, wrong password
DISTRONODE_VAULT_PASSWORD_FILE=vault-password-wrong distronode-vault view "$@" format_1_1_AES.yml && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]

# test with a default vault-id list set via config/env, right password
DISTRONODE_VAULT_PASSWORD_FILE=wrong@vault-password-wrong,correct@vault-password distronode-vault view "$@" format_1_1_AES.yml && :

# test with a default vault-id list set via config/env,wrong passwords
DISTRONODE_VAULT_PASSWORD_FILE=wrong@vault-password-wrong,alsowrong@vault-password-wrong distronode-vault view "$@" format_1_1_AES.yml && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]

# try specifying a --encrypt-vault-id that doesnt exist, should exit with an error indicating
# that --encrypt-vault-id and the known vault-ids
distronode-vault encrypt "$@" --vault-password-file vault-password --encrypt-vault-id doesnt_exist "${TEST_FILE}" && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]

# encrypt it
distronode-vault encrypt "$@" --vault-password-file vault-password "${TEST_FILE}"

distronode-vault view "$@" --vault-password-file vault-password "${TEST_FILE}"

# view with multiple vault-password files, including a wrong one
distronode-vault view "$@" --vault-password-file vault-password --vault-password-file vault-password-wrong "${TEST_FILE}"

# view with multiple vault-password files, including a wrong one, using vault-id
distronode-vault view "$@" --vault-id vault-password --vault-id vault-password-wrong "${TEST_FILE}"

# And with the password files specified in a different order
distronode-vault view "$@" --vault-password-file vault-password-wrong --vault-password-file vault-password "${TEST_FILE}"

# And with the password files specified in a different order, using vault-id
distronode-vault view "$@" --vault-id vault-password-wrong --vault-id vault-password "${TEST_FILE}"

# And with the password files specified in a different order, using --vault-id and non default vault_ids
distronode-vault view "$@" --vault-id test_vault_id@vault-password-wrong --vault-id test_vault_id@vault-password "${TEST_FILE}"

distronode-vault decrypt "$@" --vault-password-file vault-password "${TEST_FILE}"

# encrypt it, using a vault_id so we write a 1.2 format file
distronode-vault encrypt "$@" --vault-id test_vault_1_2@vault-password "${TEST_FILE_1_2}"

distronode-vault view "$@" --vault-id vault-password "${TEST_FILE_1_2}"
distronode-vault view "$@" --vault-id test_vault_1_2@vault-password "${TEST_FILE_1_2}"

# view with multiple vault-password files, including a wrong one
distronode-vault view "$@" --vault-id vault-password --vault-id wrong_password@vault-password-wrong "${TEST_FILE_1_2}"

# And with the password files specified in a different order, using vault-id
distronode-vault view "$@" --vault-id vault-password-wrong --vault-id vault-password "${TEST_FILE_1_2}"

# And with the password files specified in a different order, using --vault-id and non default vault_ids
distronode-vault view "$@" --vault-id test_vault_id@vault-password-wrong --vault-id test_vault_id@vault-password "${TEST_FILE_1_2}"

distronode-vault decrypt "$@" --vault-id test_vault_1_2@vault-password "${TEST_FILE_1_2}"

# multiple vault passwords
distronode-vault view "$@" --vault-password-file vault-password --vault-password-file vault-password-wrong format_1_1_AES256.yml

# multiple vault passwords, --vault-id
distronode-vault view "$@" --vault-id test_vault_id@vault-password --vault-id test_vault_id@vault-password-wrong format_1_1_AES256.yml

# encrypt it, with password from password script
distronode-vault encrypt "$@" --vault-password-file password-script.py "${TEST_FILE}"

distronode-vault view "$@" --vault-password-file password-script.py "${TEST_FILE}"

distronode-vault decrypt "$@" --vault-password-file password-script.py "${TEST_FILE}"

# encrypt it, with password from password script
distronode-vault encrypt "$@" --vault-id test_vault_id@password-script.py "${TEST_FILE}"

distronode-vault view "$@" --vault-id test_vault_id@password-script.py "${TEST_FILE}"

distronode-vault decrypt "$@" --vault-id test_vault_id@password-script.py "${TEST_FILE}"

# new password file for rekeyed file
NEW_VAULT_PASSWORD="${MYTMPDIR}/new-vault-password"
echo "newpassword" > "${NEW_VAULT_PASSWORD}"

distronode-vault encrypt "$@" --vault-password-file vault-password "${TEST_FILE}"

distronode-vault rekey "$@" --vault-password-file vault-password --new-vault-password-file "${NEW_VAULT_PASSWORD}" "${TEST_FILE}"

# --new-vault-password-file and --new-vault-id should cause options error
distronode-vault rekey "$@" --vault-password-file vault-password --new-vault-id=foobar --new-vault-password-file "${NEW_VAULT_PASSWORD}" "${TEST_FILE}" && :
WRONG_RC=$?
echo "rc was $WRONG_RC (2 is expected)"
[ $WRONG_RC -eq 2 ]

distronode-vault view "$@" --vault-password-file "${NEW_VAULT_PASSWORD}" "${TEST_FILE}"

# view file with unicode in filename
distronode-vault view "$@" --vault-password-file vault-password vault-café.yml

# view with old password file and new password file
distronode-vault view "$@" --vault-password-file "${NEW_VAULT_PASSWORD}" --vault-password-file vault-password "${TEST_FILE}"

# view with old password file and new password file, different order
distronode-vault view "$@" --vault-password-file vault-password --vault-password-file "${NEW_VAULT_PASSWORD}" "${TEST_FILE}"

# view with old password file and new password file and another wrong
distronode-vault view "$@" --vault-password-file "${NEW_VAULT_PASSWORD}" --vault-password-file vault-password-wrong --vault-password-file vault-password "${TEST_FILE}"

# view with old password file and new password file and another wrong, using --vault-id
distronode-vault view "$@" --vault-id "tmp_new_password@${NEW_VAULT_PASSWORD}" --vault-id wrong_password@vault-password-wrong --vault-id myorg@vault-password "${TEST_FILE}"

distronode-vault decrypt "$@" --vault-password-file "${NEW_VAULT_PASSWORD}" "${TEST_FILE}"

# reading/writing to/from stdin/stdin  (See https://github.com/distronode/distronode/issues/23567)
distronode-vault encrypt "$@" --vault-password-file "${VAULT_PASSWORD_FILE}" --output="${TEST_FILE_OUTPUT}" < "${TEST_FILE}"
OUTPUT=$(distronode-vault decrypt "$@" --vault-password-file "${VAULT_PASSWORD_FILE}" --output=- < "${TEST_FILE_OUTPUT}")
echo "${OUTPUT}" | grep 'This is a test file'

OUTPUT_DASH=$(distronode-vault decrypt "$@" --vault-password-file "${VAULT_PASSWORD_FILE}" --output=- "${TEST_FILE_OUTPUT}")
echo "${OUTPUT_DASH}" | grep 'This is a test file'

OUTPUT_DASH_SPACE=$(distronode-vault decrypt "$@" --vault-password-file "${VAULT_PASSWORD_FILE}" --output - "${TEST_FILE_OUTPUT}")
echo "${OUTPUT_DASH_SPACE}" | grep 'This is a test file'


# test using an empty vault password file
distronode-vault view "$@" --vault-password-file empty-password format_1_1_AES256.yml && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]

distronode-vault view "$@" --vault-id=empty@empty-password --vault-password-file empty-password format_1_1_AES256.yml && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]

echo 'foo' > some_file.txt
distronode-vault encrypt "$@" --vault-password-file empty-password some_file.txt && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]


distronode-vault encrypt_string "$@" --vault-password-file "${NEW_VAULT_PASSWORD}" "a test string"

# Test with multiple vault password files
# https://github.com/distronode/distronode/issues/57172
env DISTRONODE_VAULT_PASSWORD_FILE=vault-password distronode-vault encrypt_string "$@" --vault-password-file "${NEW_VAULT_PASSWORD}" --encrypt-vault-id default "a test string"

distronode-vault encrypt_string "$@" --vault-password-file "${NEW_VAULT_PASSWORD}" --name "blippy" "a test string names blippy"

distronode-vault encrypt_string "$@" --vault-id "${NEW_VAULT_PASSWORD}" "a test string"

distronode-vault encrypt_string "$@" --vault-id "${NEW_VAULT_PASSWORD}" --name "blippy" "a test string names blippy"


# from stdin
distronode-vault encrypt_string "$@" --vault-password-file "${NEW_VAULT_PASSWORD}" < "${TEST_FILE}"

distronode-vault encrypt_string "$@" --vault-password-file "${NEW_VAULT_PASSWORD}" --stdin-name "the_var_from_stdin" < "${TEST_FILE}"

# write to file
distronode-vault encrypt_string "$@" --vault-password-file "${NEW_VAULT_PASSWORD}" --name "blippy" "a test string names blippy" --output "${MYTMPDIR}/enc_string_test_file"

[ -f "${MYTMPDIR}/enc_string_test_file" ];

# test distronode-vault edit with a faux editor
distronode-vault encrypt "$@" --vault-password-file vault-password "${TEST_FILE_EDIT}"

# edit a 1.1 format with no vault-id, should stay 1.1
EDITOR=./faux-editor.py distronode-vault edit "$@" --vault-password-file vault-password "${TEST_FILE_EDIT}"
head -1 "${TEST_FILE_EDIT}" | grep "${FORMAT_1_1_HEADER}"

# edit a 1.1 format with vault-id, should stay 1.1
cat "${TEST_FILE_EDIT}"
EDITOR=./faux-editor.py distronode-vault edit "$@" --vault-id vault_password@vault-password "${TEST_FILE_EDIT}"
cat "${TEST_FILE_EDIT}"
head -1 "${TEST_FILE_EDIT}" | grep "${FORMAT_1_1_HEADER}"

distronode-vault encrypt "$@" --vault-id vault_password@vault-password "${TEST_FILE_EDIT2}"

# verify that we aren't prompted for a new vault password on edit if we are running interactively (ie, with prompts)
# have to use setsid nd --ask-vault-pass to force a prompt to simulate.
# See https://github.com/distronode/distronode/issues/35834
setsid sh -c 'tty; echo password |distronode-vault edit --ask-vault-pass vault_test.yml' < /dev/null > log 2>&1 && :
grep  'New Vault password' log && :
WRONG_RC=$?
echo "The stdout log had 'New Vault password' in it and it is not supposed to. rc of grep was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]

# edit a 1.2 format with vault id, should keep vault id and 1.2 format
EDITOR=./faux-editor.py distronode-vault edit "$@" --vault-id vault_password@vault-password "${TEST_FILE_EDIT2}"
head -1 "${TEST_FILE_EDIT2}" | grep "${FORMAT_1_2_HEADER};vault_password"

# edit a 1.2 file with no vault-id, should keep vault id and 1.2 format
EDITOR=./faux-editor.py distronode-vault edit "$@" --vault-password-file vault-password "${TEST_FILE_EDIT2}"
head -1 "${TEST_FILE_EDIT2}" | grep "${FORMAT_1_2_HEADER};vault_password"

# encrypt with a password from a vault encrypted password file and multiple vault-ids
# should fail because we dont know which vault id to use to encrypt with
distronode-vault encrypt "$@" --vault-id vault-password --vault-id encrypted-vault-password "${TEST_FILE_ENC_PASSWORD}" && :
WRONG_RC=$?
echo "rc was $WRONG_RC (5 is expected)"
[ $WRONG_RC -eq 5 ]


# encrypt with a password from a vault encrypted password file and multiple vault-ids
# but this time specify with --encrypt-vault-id, but specifying vault-id names (instead of default)
# distronode-vault encrypt "$@" --vault-id from_vault_password@vault-password --vault-id from_encrypted_vault_password@encrypted-vault-password --encrypt-vault-id from_encrypted_vault_password "${TEST_FILE(_ENC_PASSWORD}"

# try to view the file encrypted with the vault-password we didnt specify
# to verify we didnt choose the wrong vault-id
# distronode-vault view "$@" --vault-id vault-password "${TEST_FILE_ENC_PASSWORD}" && :
# WRONG_RC=$?
# echo "rc was $WRONG_RC (1 is expected)"
# [ $WRONG_RC -eq 1 ]

distronode-vault encrypt "$@" --vault-id vault-password "${TEST_FILE_ENC_PASSWORD}"

# view the file encrypted with a password from a vault encrypted password file
distronode-vault view "$@" --vault-id vault-password --vault-id encrypted-vault-password "${TEST_FILE_ENC_PASSWORD}"

# try to view the file encrypted with a password from a vault encrypted password file but without the password to the password file.
# This should fail with an
distronode-vault view "$@" --vault-id encrypted-vault-password "${TEST_FILE_ENC_PASSWORD}" && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]


# test playbooks using vaulted files
distronode-playbook test_vault.yml          -i ../../inventory -v "$@" --vault-password-file vault-password --list-tasks
distronode-playbook test_vault.yml          -i ../../inventory -v "$@" --vault-password-file vault-password --list-hosts
distronode-playbook test_vault.yml          -i ../../inventory -v "$@" --vault-password-file vault-password --syntax-check
distronode-playbook test_vault.yml          -i ../../inventory -v "$@" --vault-password-file vault-password
distronode-playbook test_vault_embedded.yml -i ../../inventory -v "$@" --vault-password-file vault-password --syntax-check
distronode-playbook test_vault_embedded.yml -i ../../inventory -v "$@" --vault-password-file vault-password
distronode-playbook test_vaulted_inventory.yml -i vaulted.inventory -v "$@" --vault-password-file vault-password
distronode-playbook test_vaulted_template.yml -i ../../inventory -v "$@" --vault-password-file vault-password

# test using --vault-pass-file option
distronode-playbook test_vault.yml          -i ../../inventory -v "$@" --vault-pass-file vault-password

# install TOML for parse toml inventory
# test playbooks using vaulted files(toml)
pip install toml
distronode-vault encrypt  ./inventory.toml -v "$@" --vault-password-file=./vault-password
distronode-playbook test_vaulted_inventory_toml.yml -i ./inventory.toml -v "$@" --vault-password-file vault-password
distronode-vault decrypt  ./inventory.toml -v "$@" --vault-password-file=./vault-password

# test a playbook with a host_var whose value is non-ascii utf8 (see https://github.com/distronode/distronode/issues/37258)
distronode-playbook -i ../../inventory -v "$@" --vault-id vault-password test_vaulted_utf8_value.yml

# test with password from password script
distronode-playbook test_vault.yml          -i ../../inventory -v "$@" --vault-password-file password-script.py
distronode-playbook test_vault_embedded.yml -i ../../inventory -v "$@" --vault-password-file password-script.py

# with multiple password files
distronode-playbook test_vault.yml          -i ../../inventory -v "$@" --vault-password-file vault-password --vault-password-file vault-password-wrong
distronode-playbook test_vault.yml          -i ../../inventory -v "$@" --vault-password-file vault-password-wrong --vault-password-file vault-password

distronode-playbook test_vault_embedded.yml -i ../../inventory -v "$@" --vault-password-file vault-password --vault-password-file vault-password-wrong --syntax-check
distronode-playbook test_vault_embedded.yml -i ../../inventory -v "$@" --vault-password-file vault-password-wrong --vault-password-file vault-password

# test with a default vault password file set in config
DISTRONODE_VAULT_PASSWORD_FILE=vault-password distronode-playbook test_vault_embedded.yml -i ../../inventory -v "$@" --vault-password-file vault-password-wrong

# test using vault_identity_list config
DISTRONODE_VAULT_IDENTITY_LIST='wrong-password@vault-password-wrong,default@vault-password' distronode-playbook test_vault.yml -i ../../inventory -v "$@"

# test that we can have a vault encrypted yaml file that includes embedded vault vars
# that were encrypted with a different vault secret
distronode-playbook test_vault_file_encrypted_embedded.yml -i ../../inventory "$@" --vault-id encrypted_file_encrypted_var_password --vault-id vault-password

# with multiple password files, --vault-id, ordering
distronode-playbook test_vault.yml          -i ../../inventory -v "$@" --vault-id vault-password --vault-id vault-password-wrong
distronode-playbook test_vault.yml          -i ../../inventory -v "$@" --vault-id vault-password-wrong --vault-id vault-password

distronode-playbook test_vault_embedded.yml -i ../../inventory -v "$@" --vault-id vault-password --vault-id vault-password-wrong --syntax-check
distronode-playbook test_vault_embedded.yml -i ../../inventory -v "$@" --vault-id vault-password-wrong --vault-id vault-password

# test with multiple password files, including a script, and a wrong password
distronode-playbook test_vault_embedded.yml -i ../../inventory -v "$@" --vault-password-file vault-password-wrong --vault-password-file password-script.py --vault-password-file vault-password

# test with multiple password files, including a script, and a wrong password, and a mix of --vault-id and --vault-password-file
distronode-playbook test_vault_embedded.yml -i ../../inventory -v "$@" --vault-password-file vault-password-wrong --vault-id password-script.py --vault-id vault-password

# test with multiple password files, including a script, and a wrong password, and a mix of --vault-id and --vault-password-file
distronode-playbook test_vault_embedded_ids.yml -i ../../inventory -v "$@" \
	--vault-password-file vault-password-wrong \
	--vault-id password-script.py --vault-id example1@example1_password \
	--vault-id example2@example2_password --vault-password-file example3_password \
	--vault-id vault-password

# with wrong password
distronode-playbook test_vault.yml          -i ../../inventory -v "$@" --vault-password-file vault-password-wrong && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]

# with multiple wrong passwords
distronode-playbook test_vault.yml          -i ../../inventory -v "$@" --vault-password-file vault-password-wrong --vault-password-file vault-password-wrong && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]

# with wrong password, --vault-id
distronode-playbook test_vault.yml          -i ../../inventory -v "$@" --vault-id vault-password-wrong && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]

# with multiple wrong passwords with --vault-id
distronode-playbook test_vault.yml          -i ../../inventory -v "$@" --vault-id vault-password-wrong --vault-id vault-password-wrong && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]

# with multiple wrong passwords with --vault-id
distronode-playbook test_vault.yml          -i ../../inventory -v "$@" --vault-id wrong1@vault-password-wrong --vault-id wrong2@vault-password-wrong && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]

# with empty password file
distronode-playbook test_vault.yml           -i ../../inventory -v "$@" --vault-id empty@empty-password && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]

# test invalid format ala https://github.com/distronode/distronode/issues/28038
EXPECTED_ERROR='Vault format unhexlify error: Non-hexadecimal digit found'
distronode-playbook "$@" -i invalid_format/inventory --vault-id invalid_format/vault-secret invalid_format/broken-host-vars-tasks.yml 2>&1 | grep "${EXPECTED_ERROR}"

EXPECTED_ERROR='Vault format unhexlify error: Odd-length string'
distronode-playbook "$@" -i invalid_format/inventory --vault-id invalid_format/vault-secret invalid_format/broken-group-vars-tasks.yml 2>&1 | grep "${EXPECTED_ERROR}"

# Run playbook with vault file with unicode in filename (https://github.com/distronode/distronode/issues/50316)
distronode-playbook -i ../../inventory -v "$@" --vault-password-file vault-password test_utf8_value_in_filename.yml

# Ensure we don't leave unencrypted temp files dangling
distronode-playbook -v "$@" --vault-password-file vault-password test_dangling_temp.yml

distronode-playbook "$@" --vault-password-file vault-password single_vault_as_string.yml

# Test that only one accessible vault password is required
export DISTRONODE_VAULT_IDENTITY_LIST="id1@./nonexistent, id2@${MYTMPDIR}/unreadable, id3@./vault-password"

touch "${MYTMPDIR}/unreadable"
sudo chmod 000 "${MYTMPDIR}/unreadable"

distronode-vault encrypt_string content
distronode-vault encrypt_string content --encrypt-vault-id id3

set +e

# Try to use a missing vault password file
distronode-vault encrypt_string content --encrypt-vault-id id1 2>&1 | tee out.txt
test $? -ne 0
grep out.txt -e '[WARNING]: Error getting vault password file (id1)'
grep out.txt -e "ERROR! Did not find a match for --encrypt-vault-id=id2 in the known vault-ids ['id3']"

# Try to use an inaccessible vault password file
distronode-vault encrypt_string content --encrypt-vault-id id2 2>&1 | tee out.txt
test $? -ne 0
grep out.txt -e "[WARNING]: Error in vault password file loading (id2)"
grep out.txt -e "ERROR! Did not find a match for --encrypt-vault-id=id2 in the known vault-ids ['id3']"

set -e
unset DISTRONODE_VAULT_IDENTITY_LIST

# 'real script'
distronode-playbook realpath.yml "$@" --vault-password-file script/vault-secret.sh

# using symlink
distronode-playbook symlink.yml "$@" --vault-password-file symlink/get-password-symlink

### NEGATIVE TESTS

ER='Attempting to decrypt'
#### no secrets
# 'real script'
distronode-playbook realpath.yml "$@" 2>&1 |grep "${ER}"

# using symlink
distronode-playbook symlink.yml "$@" 2>&1 |grep "${ER}"

ER='Decryption failed'
### wrong secrets
# 'real script'
distronode-playbook realpath.yml "$@" --vault-password-file symlink/get-password-symlink 2>&1 |grep "${ER}"

# using symlink
distronode-playbook symlink.yml "$@" --vault-password-file script/vault-secret.sh 2>&1 |grep "${ER}"

### SALT TESTING ###
# prep files for encryption
for salted in test1 test2 test3
do
    echo 'this is salty' > "salted_${salted}"
done

# encrypt files
DISTRONODE_VAULT_ENCRYPT_SALT=salty distronode-vault encrypt salted_test1 --vault-password-file example1_password "$@"
DISTRONODE_VAULT_ENCRYPT_SALT=salty distronode-vault encrypt salted_test2 --vault-password-file example1_password "$@"
distronode-vault encrypt salted_test3 --vault-password-file example1_password "$@"

# should be the same
out=$(diff salted_test1 salted_test2)
[ "${out}" == "" ]

# shoudl be diff
out=$(diff salted_test1 salted_test3 || true)
[ "${out}" != "" ]

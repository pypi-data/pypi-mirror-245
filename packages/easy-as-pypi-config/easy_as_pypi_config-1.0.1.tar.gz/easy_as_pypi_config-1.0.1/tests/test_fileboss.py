# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-config#🍐
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
# License: MIT

import os
import pathlib  # noqa: F401
import re
from unittest import mock

import pytest
from easy_as_pypi_appdirs import register_application

from easy_as_pypi_config import defaults
from easy_as_pypi_config.fileboss import (  # noqa: F401
    create_configobj,
    default_config_path,
    default_config_path_abbrev,
    echo_config_obj,
    load_config_obj,
    warn_user_config_errors,
    write_config_obj,
)


class TestGetConfigInstance(object):
    @pytest.fixture(autouse=True)
    def register_application(self, app_name):
        register_application(app_name)

    # ***

    def test_default_config_path(self, tmp_appdirs):
        # Note that tmp_appdirs included so default_config_path uses /tmp.
        cfgpath = default_config_path()
        expect = os.path.join(tmp_appdirs.user_config_dir, defaults.conf_filename)
        assert cfgpath == expect

    def test_default_config_path_abbrev(self, mocker, tmpdir, tmp_appdirs):
        mocker.patch("pathlib.Path.home", return_value=tmpdir)
        tmpdir_with_final_sep = os.path.join(tmpdir, "")
        # Escape input in case Windows path, e.g., "^C:\Users\runneradmin\...\".
        match_leading_path = r"^{}".format(re.escape(tmpdir_with_final_sep))
        app_dir_file = re.sub(match_leading_path, "", tmp_appdirs.user_config_dir)
        abbreved = default_config_path_abbrev()
        assert abbreved == os.path.join("~", app_dir_file, defaults.conf_filename)

    # ***

    def test_create_configobj_okay(self, filepath):
        configobj = create_configobj(filepath, errname="test")
        assert configobj.dict() == {}

    def test_create_configobj_fail_duplicate_keys(self, conf_file_dup_keys, capsys):
        conf_path = conf_file_dup_keys
        configobj = create_configobj(conf_path, errname="test")
        assert configobj is None
        out, err = capsys.readouterr()
        assert not out
        assert err.startswith("Failed to load test config at")

    def test_create_configobj_fail_duplicate_secs(self, conf_file_dup_secs, capsys):
        conf_path = conf_file_dup_secs
        configobj = create_configobj(conf_path, errname="test")
        assert configobj is None
        out, err = capsys.readouterr()
        assert not out
        assert err.startswith("Failed to load test config at")

    # ***

    def test_echo_config_obj(self, simple_config_obj, capsys):
        echo_config_obj(simple_config_obj)
        out, err = capsys.readouterr()
        assert out.startswith("[sectionA]\n")
        assert not err

    # ***

    def test_load_config_obj_okay(self, simple_config_obj, simple_config_dict):
        config_obj = load_config_obj(simple_config_obj.filename)
        assert config_obj.dict() == simple_config_dict

    def test_load_config_obj_fail_duplicate_error(self, conf_file_dup_secs, capsys):
        with pytest.raises(SystemExit):
            load_config_obj(conf_file_dup_secs)
        # Read output, else goes to dev's test console.
        out, err = capsys.readouterr()
        assert not out and err

    def test_load_config_obj_fail_parse_error(self, conf_file_imparseable, capsys):
        with pytest.raises(SystemExit):
            load_config_obj(conf_file_imparseable)
        out, err = capsys.readouterr()
        assert not out and err

    # ***

    def test_write_config_obj_okay(self, simple_config_obj, filepath):
        assert os.path.isfile(simple_config_obj.filename)
        simple_config_obj.filename = filepath
        write_config_obj(simple_config_obj)
        assert os.path.isfile(filepath)

    def test_write_config_obj_fail_no_filename(self, simple_config_obj):
        assert os.path.isfile(simple_config_obj.filename)
        simple_config_obj.filename = None
        with pytest.raises(AttributeError):
            write_config_obj(simple_config_obj)

    def test_write_config_obj_fail_no_cannot_mkdir_p(
        self,
        simple_config_obj,
        filename,
        capsys,
    ):
        assert os.path.isfile(simple_config_obj.filename)
        invalid_filename = os.path.join(simple_config_obj.filename, filename)
        simple_config_obj.filename = invalid_filename
        with pytest.raises(SystemExit):
            write_config_obj(simple_config_obj)
        out, err = capsys.readouterr()
        assert not out and err

    def test_write_config_obj_fail_unicode_encode_error(
        self,
        filepath,
        capsys,
    ):
        if os.name != "nt":
            config_obj = invalid_config_obj(filepath)
            with pytest.raises(SystemExit):
                write_config_obj(config_obj)
            out, err = capsys.readouterr()
            assert not out and err
        else:
            # DUNNO/2023-11-13: The Windows CI runner follows this path.
            # It seems like Windows handles UTF-8 gibberish differently
            # than Linux or macOS, or maybe something else is afoot. It's
            # not really worth anyone's time to dig in deeper, though.
            # (And it's prob. not configobj, which is legacy/stable.)
            with pytest.raises(UnicodeEncodeError):
                config_obj = invalid_config_obj(filepath)
            out, err = capsys.readouterr()
            assert not out and not err

    def test_write_config_obj_fail_unknown_forced_error(
        self,
        simple_config_obj,
        mocker,
        capsys,
    ):
        # I'm not sure what else would make ConfigObj.write() throw besides
        # UnicodeEncodeError, but that doesn't mean we can't test it.
        arbitrary_error_mock = mock.Mock()
        arbitrary_error_mock.side_effect = Exception
        mocker.patch.object(simple_config_obj, "write", arbitrary_error_mock)
        with pytest.raises(SystemExit):
            write_config_obj(simple_config_obj)
        out, err = capsys.readouterr()
        assert not out and err

    # ***

    def test_warn_user_config_errors(self, capsys):
        errs = {
            "foo": {
                "bar": "baz",
            },
            "bat": None,
        }
        warn_user_config_errors(errs)
        out, err = capsys.readouterr()
        assert not out and err

    # ***


# ***


@pytest.fixture()
def conf_file_dup_keys(filepath):
    with open(filepath, "w") as conf_file:
        conf_file.write(
            """
[section]
dup_key = 123
dup_key = 456
""".lstrip()
        )
    return filepath


@pytest.fixture()
def conf_file_dup_secs(filepath):
    with open(filepath, "w") as conf_file:
        conf_file.write(
            """
[section]
foo = 123

[section]
bar = 456
""".lstrip()
        )
    return filepath


@pytest.fixture()
def conf_file_imparseable(filepath):
    with open(filepath, "w") as conf_file:
        conf_file.write(
            """
[section]
foo
""".lstrip()
        )
    return filepath


# ***


@pytest.fixture()
def simple_config_obj(filepath):
    with open(filepath, "w") as conf_file:
        conf_file.write(
            """
[sectionA]
foo = 123

[sectionB]
bar = 456
baz = 'bat'
""".lstrip()
        )
    configobj = create_configobj(filepath, errname="test")
    return configobj


@pytest.fixture()
def simple_config_dict():
    return {
        "sectionA": {
            "foo": "123",
        },
        "sectionB": {
            "bar": "456",
            "baz": "bat",
        },
    }


# ***

# DUNNO/2023-11-13: This fcn had been a fixture, but on Windows (py3.12) CI
# runner, it throws UnicodeEncodeError from the conf_file.write. But if you
# "repair" the string, then write_config_obj(configobj) works, though callers
# expect it to raise. So I'll document what I saw, but callers know to expect
# different behavior on Windows.
#
# - The first issue was
#
#       ERROR at setup of
#       TestGetConfigInstance.test_write_config_obj_fail_unicode_encode_error
#         tests\test_fileboss.py:252: in invalid_config_obj
#
#   - (It's during "setup of" because @pytest.fixture invalid_config_obj is
#      called before the test runs.)
#
#     It reported the error:
#
#       conf_file.write(
#         C:\hostedtoolcache\windows\Python\3.12.0\x64\Lib\encodings\cp1252.py:19:
#       in encode
#         return codecs.charmap_encode(input,self.errors,encoding_table)[0]
#       UnicodeEncodeError: 'charmap' codec can't encode characters in
#                            position 8-11: character maps to <undefined>
#
#   - Indeed position 8-11 is the first user name:
#
#       users = вася, петя
#
#     And if we change it to:
#
#       users = user, петя
#
#     Then the error message shifts accordingly:
#
#       'charmap' codec can't encode characters in position 14-17
#
#   - So then we replace both user names:
#
#       users = user, user
#
#     And now the conf_file.write() works, but then create_configobj() fails.
#
#     The error is now UnicodeDecodeError (the prev. were UnicodeEncodeError),
#     and it's due to the last line of the input:
#
#       'utf-8' codec can't decode byte 0x91 in position 7: invalid start byte
#
#     But if you replace the final Unicode character:
#
#       foo = '\u2018'
#
#     E.g., to this:
#
#       foo = 'bar'
#
#     then create_configobj() works, but the config object is *valid*
#     (there are no fishy characters), and the caller's test will fail.
#
# - This behavior is only observed on Windows, but it seems weird that one
#   OS throws UnicodeEncodeError during config_obj = configobj.ConfigObj(),
#   while the other OSes happily create the object, but then throw
#   UnicodeEncodeError on config_obj.write().


def invalid_config_obj(filepath):
    # REFER/2020-12-14: What looks like Russian characters (I'd guess) from:
    #   https://stackoverflow.com/questions/32208421/
    #     ascii-codec-error-when-writing-configobj
    # - The \u2018 is just a fancy curly ‘.
    with open(filepath, "w") as conf_file:
        conf_file.write(
            """
users = вася, петя

[sectionA]
foo = '\u2018'
""".lstrip()
        )
    configobj = create_configobj(filepath, errname="test")
    # Generally this is 'UTF8' and config_obj.write() won't ever throw.
    configobj.encoding = None
    return configobj


# ***

# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-config#🍐
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
# License: MIT

import os
import pathlib
from unittest.mock import MagicMock

import pytest
from config_decorator import KeyChainedValue
from easy_as_pypi_appdirs import register_application

from easy_as_pypi_config.defaults import register_conf_filename
from easy_as_pypi_config.fileboss import write_config_obj
from easy_as_pypi_config.urable import ConfigUrable


class TestWriteConfigFile(object):
    def test_file_is_written(self, filepath, config_instance):
        """Ensure file is written. Content not checked; that's ConfigObj's job."""
        config_obj = config_instance()
        write_config_obj(config_obj)
        # E.g., '/tmp/pytest-of-user/pytest-188/test_file_is_written0/{}.conf'
        assert os.path.lexists(config_obj.filename)

    def test_non_existing_path(self, filepath, filename, config_instance):
        """Make sure that the path-parents are created if not present."""
        deeppath = os.path.join(filepath, filename)
        assert not os.path.lexists(deeppath)
        config_obj = config_instance()
        config_obj.filename = deeppath
        write_config_obj(config_obj)
        assert os.path.lexists(deeppath)


# ***


class TestGetConfigInstance(object):
    EASY_AS_PYPI_CONFIG_CONFIGFILE_ENVKEY = "EAPPCONF_CONFIGFILE"

    EASY_AS_PYPI_CONFIG_CONFIGFILE_BASENAME = "easy-as-pypi-tests.conf"

    @pytest.fixture(autouse=True)
    def register_application(self, app_name):
        register_application(app_name)

    @pytest.fixture(autouse=True)
    def register_conf_filename(self):
        conf_filename = self.EASY_AS_PYPI_CONFIG_CONFIGFILE_BASENAME
        register_conf_filename(conf_filename)

    @pytest.fixture(autouse=True)
    def register_envvar_prefix(self, app_name):
        KeyChainedValue._envvar_prefix = self.EASY_AS_PYPI_CONFIG_CONFIGFILE_ENVKEY

    @pytest.fixture(autouse=True)
    def set_config_root(self, basic_config_root):
        self.config_root = basic_config_root

    # ***

    # MAYBE/2020-12-21: Should this be a @fixture?
    def get_configurable(self, **kwargs):
        return ConfigUrable(
            config_root=self.config_root,
            configfile_envkey=self.EASY_AS_PYPI_CONFIG_CONFIGFILE_ENVKEY,
            **kwargs,
        )

    # ***

    def test_no_file_present(self, tmp_appdirs):
        # Note that tmp_appdirs included so default_config_path uses /tmp.
        configurable = self.get_configurable()
        configurable.load_config(configfile_path=None)
        assert len(list(configurable.config_root.items())) > 0
        assert configurable.cfgfile_exists is False

    def test_file_present(self, config_instance):
        """Make sure we try parsing a found config file."""
        # Write the config to /tmp/…/{}.conf
        config_obj = config_instance()
        config_obj.write()
        # Setup the ConfigUrable.
        configurable = self.get_configurable()
        configurable.load_config(configfile_path=config_obj.filename)
        # Assert that the written config was read.
        cfg_val = configurable.config_root["foo"]["bar"]
        assert cfg_val == config_obj["foo"]["bar"]
        assert config_obj is not configurable.config_root

    # ***

    def test_config_path_getter(self, tmp_appdirs, mocker):
        """Make sure the config target path is constructed to our expectations."""
        # Note that tmp_appdirs included so default_config_path uses /tmp.

        # DUNNO/2023-11-13: Works in Python 3.8-3.11:
        #     mocker.patch("easy_as_pypi_config.fileboss.load_config_obj")
        #     ...
        #     assert fileboss.load_config_obj.called_with(expectation)
        # - Python 3.12 changes called_with to assert_called_with.
        # - But also in Python 3.12 the mock no longer works, and rightfully
        #   so: urable.py imports load_config_obj at file-level, so by the
        #   time this test tries to patch fileboss, urable.py already has a
        #   direct reference to the function, so the mock doesn't get used.
        # - Whatever. We'll just mock the ConfigUrable object... which feels
        #   a little sloppy, but now 3.12 tests pass, so, profit.

        configurable = self.get_configurable()
        configurable._load_config_obj = MagicMock()
        configurable.load_config(configfile_path=None)
        expectation = os.path.join(
            tmp_appdirs.user_config_dir,
            self.EASY_AS_PYPI_CONFIG_CONFIGFILE_BASENAME,
        )

        configurable._load_config_obj.assert_called_with(expectation)

    # ***

    def test_property_config_root(self):
        configurable = self.get_configurable()
        assert configurable.config_root is self.config_root

    def test_property_latest_errs(self):
        configurable = self.get_configurable()
        assert configurable.latest_errs == {}

    def test_property_unstructured(self):
        configurable = self.get_configurable()
        assert configurable.unstructured == {}

    # ***

    def test_find_all_okay(self):
        configurable = self.get_configurable()
        all_found = configurable.find_all(["foo"])
        assert all_found[0] is configurable.config_root["foo"]

    def test_find_all_fail(self):
        configurable = self.get_configurable()
        with pytest.raises(KeyError):
            configurable.find_all(["foo2"])

    # ***

    def test_create_config_fail_config_path_missing(self):
        configurable = self.get_configurable()
        with pytest.raises(AttributeError):
            configurable.create_config(force=False)

    def test_create_config_fail_config_path_exists(self, filepath):
        pathlib.Path(filepath).touch()
        configurable = self.get_configurable()
        # This is somewhat of a hack: nothing else accesses configfile_path.
        # Usually, the class itself sets it based on default_config_path,
        # unless path passed via CLI args or environ.
        configurable.configfile_path = filepath
        with pytest.raises(SystemExit):
            configurable.create_config(force=False)

    def test_create_config_okay(self, filepath, capsys):
        configurable = self.get_configurable()
        configurable.configfile_path = filepath
        configurable.create_config(force=False)
        out, err = capsys.readouterr()
        assert out and not err

    # ***

    def test_load_config_via_cli_arg(self, basic_config_file):
        configfile_path = basic_config_file
        commandline_value = configfile_path
        configurable = self.get_configurable()
        configurable.load_config(configfile_path=commandline_value)
        assert configurable.cfgfile_exists

    def test_load_config_via_environ(self, basic_config_file, mocker):
        configfile_path = basic_config_file
        mocker.patch.dict(
            os.environ,
            {
                self.EASY_AS_PYPI_CONFIG_CONFIGFILE_ENVKEY: configfile_path,
            },
        )
        configurable = self.get_configurable()
        configurable.load_config(configfile_path=None)
        assert configurable.cfgfile_exists

    def test_load_config_unrestricted(self, basic_config_file):
        configfile_path = basic_config_file
        commandline_value = configfile_path
        configurable = self.get_configurable(unrestricted=True)
        configurable.load_config(configfile_path=commandline_value)
        assert configurable.cfgfile_exists

    # ***

    def test_inject_from_cli_okay(self):
        configurable = self.get_configurable()
        configurable.inject_from_cli("foo.bar=123")
        assert configurable.config_root["foo"]["bar"] == "123"

    def test_inject_from_cli_fail(self, capsys):
        configurable = self.get_configurable()
        with pytest.raises(SystemExit):
            configurable.inject_from_cli("foo.bar=123", "quux.qiix=foo")
        out, err = capsys.readouterr()
        assert not out and err

    # ***

    def test_round_out_config(self, filepath):
        configurable = self.get_configurable()
        configurable.configfile_path = filepath
        configurable.round_out_config()

    # ***

    def test_reset_config(self, filepath):
        configurable = self.get_configurable()
        configurable.configfile_path = filepath
        configurable.reset_config()

    # ***

    def test_write_config(self, filepath):
        configurable = self.get_configurable()
        configurable.configfile_path = filepath
        configurable.write_config()

    # ***


# ***

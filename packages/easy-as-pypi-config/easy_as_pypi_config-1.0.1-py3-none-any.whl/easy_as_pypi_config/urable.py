# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-config#🍐
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
# License: MIT

import os
from gettext import gettext as _

from easy_as_pypi_termio.echoes import click_echo, highlight_value
from easy_as_pypi_termio.errors import exit_warning

from .fileboss import (
    default_config_path,
    load_config_obj,
    warn_user_config_errors,
    write_config_obj,
)

__all__ = ("ConfigUrable",)


class ConfigUrable(object):
    """"""

    def __init__(self, config_root, configfile_envkey, unrestricted=False):
        super(ConfigUrable, self).__init__()
        # The config file path os.environ, e.g., {APPNAME}_CONFIGFILE.
        self.configfile_envkey = configfile_envkey
        self.configfile_path = None
        # The ConfigRoot is a module-level Singleton. Deal.
        self._config_root = config_root
        self._latest_errs = {}
        self._unrestricted = unrestricted
        self._unstructured = {}
        #
        self._load_config_obj = load_config_obj

    # ***

    @property
    def config_path(self):
        return self.configfile_path

    # ***

    @property
    def config_root(self):
        return self._config_root

    # ***

    @property
    def latest_errs(self):
        return self._latest_errs

    @property
    def unstructured(self):
        return self._unstructured

    # ***

    def find_all(self, parts):
        # Caller is responsible for catching KeyError on unrecognized part(s).
        return self.config_root.find_all(parts)

    # ***

    def create_config(self, force):
        if not self.config_path:
            # It's up to the DEV to ensure this.
            raise AttributeError("ConfigUrable missing ‘config_path’")

        cfgfile_exists = os.path.exists(self.config_path)
        if cfgfile_exists and not force:
            exit_warning(_("Config file exists"))

        self.reset_config()
        click_echo(
            _("Initialized default config file at {}").format(
                highlight_value(self.config_path),
            )
        )

    # ***

    def load_config(self, configfile_path):
        def _load_config():
            # The tests for downstream CLI apps can mock load_configfile when
            # going through CliRunner, to wire any store fixture (such as
            # Alchemy) and config fixture upon CLI invocation, and to skip
            # reading the config from a file here.
            cfgfile_exists = self.load_configfile(configfile_path)
            self.cfgfile_exists = cfgfile_exists

        _load_config()

    def load_configfile(self, configfile_path):
        def _load_configfile():
            self.configfile_path = _resolve_configfile_path(configfile_path)
            cfgfile_exists = os.path.exists(self.config_path)
            config_obj = self._load_config_obj(self.config_path)
            self.config_root.forget_config_values()
            errs = _consume_config_obj_and_warn_if_smelly(config_obj)
            warn_if_smelly_config(errs)

            return cfgfile_exists

        def _resolve_configfile_path(commandline_value):
            if commandline_value is not None:
                return commandline_value

            if self.configfile_envkey in os.environ:
                return os.environ[self.configfile_envkey]

            return default_config_path()

        def _consume_config_obj_and_warn_if_smelly(config_obj):
            if self._unrestricted:
                return _load_config_obj_consume_all_config(config_obj)

            return _load_config_obj_consume_recognized(config_obj)

        def _load_config_obj_consume_all_config(config_obj):
            errs = self.config_root.update_gross(config_obj, errors_ok=True)
            return errs

        def _load_config_obj_consume_recognized(config_obj):
            unconsumed, errs = self.config_root.update_known(config_obj, errors_ok=True)
            self._unstructured = unconsumed
            return errs

        def warn_if_smelly_config(errs):
            basename = os.path.basename(self.config_path)
            warn_user_config_errors(errs, which=basename)
            self._latest_errs = errs

        return _load_configfile()

    def inject_from_cli(self, *keyvals):
        def _inject_cli_settings():
            for keyval in keyvals:
                process_option(keyval)

        def process_option(keyval):
            key, value = keyval.split("=", 2)
            parts = key.split(".")
            try:
                setting = self.config_root.find_setting(parts)
            except KeyError:
                setting = None
            if setting is None:
                exit_warning(_("ERROR: Unknown config option: “{}”").format(key))
            setting.value_from_cliarg = value

        return _inject_cli_settings()

    # ***

    def round_out_config(self):
        self.write_config(skip_unset=False)

    # ***

    def reset_config(self):
        config_obj = self._load_config_obj(self.config_path)
        # Fill in dict object using Config defaults.
        self.config_root.forget_config_values()
        self.config_root.apply_items(config_obj, use_defaults=True)
        write_config_obj(config_obj)
        self.cfgfile_exists = True  # If anything, we just created it!

    # ***

    def write_config(self, skip_unset=False):
        config_obj = self._load_config_obj(self.config_path)
        # - (lb): If we did not want to use skip_unset, which won't pollute
        #   the config_obj that was just read from the user's config, we
        #   could similarly delete entries from the config, e.g.,
        #       if skip_unset:
        #           # Remove settings that are no different than their default
        #           # (to not save them to the config, potentially cluttering it).
        #           self.config_root.del_not_persisted(config_obj)
        #   but sticking with apply_items(skip_unset=True) means self.config_root
        #   will still be usable after this method returns. I.e., no side effects.
        # Fill in dict object using values previously set from config or newly set.
        self.config_root.apply_items(config_obj, skip_unset=skip_unset)
        write_config_obj(config_obj)
        self.cfgfile_exists = True

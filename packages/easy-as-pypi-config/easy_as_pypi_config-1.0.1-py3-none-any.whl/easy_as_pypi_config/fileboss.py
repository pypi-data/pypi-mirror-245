# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-config#🍐
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
# License: MIT

import os
import re
import tempfile
from gettext import gettext as _
from pathlib import Path

from configobj import ConfigObj, ConfigObjError, DuplicateError, ParseError
from easy_as_pypi_appdirs import AppDirs
from easy_as_pypi_appdirs.exists_or_mkdirs import must_ensure_file_path_dirred
from easy_as_pypi_termio.echoes import click_echo
from easy_as_pypi_termio.errors import echo_warning, exit_warning

from . import defaults

__all__ = (
    "create_configobj",
    "default_config_path",
    "default_config_path_abbrev",
    "echo_config_obj",
    "load_config_obj",
    "warn_user_config_errors",
    "write_config_obj",
)


# ***


def default_config_path():
    # (Weird) Side-effect: Directory might be created.
    config_dir = AppDirs().user_config_dir
    config_filename = defaults.conf_filename
    configfile_path = os.path.join(config_dir, config_filename)
    return configfile_path


def default_config_path_abbrev():
    # Path.home() is Python 3.5+. See os.path.expanduser('~') for older Python.
    user_home = str(Path.home())
    # Escape input in case Windows path, e.g., "^C:\Users\runneradmin\...\".
    sanitized = re.escape(user_home)
    abbrev_path = re.sub(r"^{}".format(sanitized), "~", default_config_path())
    return abbrev_path


# ***


def create_configobj(conf_path, errname=""):
    try:
        return ConfigObj(
            conf_path,
            encoding="UTF8",
            interpolation=False,
            write_empty_values=False,
        )
    except ConfigObjError as err:
        # Catches DuplicateError, and other errors, e.g.,
        #       Parsing failed with several errors.
        #       First error at line 55.
        msg = _("Failed to load {0} config at “{1}”: {2}").format(
            errname,
            conf_path,
            str(err),
        )
        echo_warning(msg)
        return None


# ***


def echo_config_obj(config_obj):
    def _echo_config_obj():
        temp_f = prepare_temp_file(config_obj)
        write_config_obj(config_obj)
        open_and_print_dump(temp_f)

    def prepare_temp_file(config_obj):
        # Not that easy:
        #   config_obj.filename = sys.stdout
        # (lb): My understanding is that for the TemporaryFile to be openable
        # on Windows, we should close it first (Linux can open an opened file
        # again, but not Windows).
        #   https://docs.python.org/3/library/tempfile.html#tempfile.NamedTemporaryFile
        temp_f = tempfile.NamedTemporaryFile(delete=False)
        temp_f.close()
        config_obj.filename = temp_f.name
        return temp_f

    def open_and_print_dump(temp_f):
        with open(temp_f.name, "r") as fobj:
            click_echo(fobj.read().strip())
        os.unlink(temp_f.name)

    return _echo_config_obj()


# ***


def load_config_obj(configfile_path):
    """"""

    def _empty_config_obj():
        try:
            config_obj = create_config_obj()
        except ParseError as err:
            # E.g., "configobj.ParseError: Invalid line ('<>') (...) at line <>."
            exit_parse_error(str(err))
        except DuplicateError as err:
            # (lb): The original (builtin) configparser would let you
            # choose to error or not on duplicates, but the ConfigObj
            # library (which is awesome in many ways) does not have
            # such a feature (it's got a raise_errors that does not
            # do the trick). Consequently, unless we code a way around
            # this, we gotta die on duplicates. Sorry, User! Seems
            # pretty lame. But also seems pretty unlikely.
            exit_duplicates(str(err))
        return config_obj

    def create_config_obj():
        config_obj = ConfigObj(
            configfile_path,
            encoding="UTF8",
            interpolation=False,
            write_empty_values=False,
            # Note that ConfigObj has a raise_errors param, but if False, it
            # just defers the error, if any; it'll still get raised, just at
            # the end. So what's the point? -(lb)
            #   raise_errors=False,
        )
        return config_obj

    def exit_parse_error(err):
        msg = _("ERROR: Your config file at “{}” has a syntax error: “{}”").format(
            configfile_path, str(err)
        )
        exit_warning(msg)

    def exit_duplicates(err):
        msg = _("ERROR: Your config file at “{}” has a duplicate setting: “{}”").format(
            configfile_path, str(err)
        )
        exit_warning(msg)

    return _empty_config_obj()


# ***


def write_config_obj(config_obj):
    def _write_config_obj():
        ensure_config_has_filename_or_exit()
        ensure_file_dirs_or_mkdirs_or_exit()
        ensure_config_obj_write_or_exit()

    def ensure_config_has_filename_or_exit():
        if not config_obj.filename:
            raise AttributeError("ConfigObj missing ‘filename’")

    def ensure_file_dirs_or_mkdirs_or_exit():
        try:
            must_ensure_file_path_dirred(config_obj.filename)
        except Exception as err:
            die_write_failed(config_obj, err)

    def ensure_config_obj_write_or_exit():
        try:
            config_obj.write()
        except UnicodeEncodeError as err:
            # If default ConfigObj.encoding = 'UTF8' left untouched,
            # this branch is unreachable. But one test disables it
            # (sets encoding to None), so not out of the question.
            die_write_failed(config_obj, err)
        except Exception as err:
            die_write_failed(config_obj, err)

    def die_write_failed(config_obj, err):
        hint = extract_hint(err)
        msg = _("{}: {} “{}”: “{}”{}").format(
            _("ERROR"),
            _("Failed to write file at"),
            config_obj.filename,
            str(err),
            " ({})".format(hint) if hint else "",
        )
        exit_warning(msg)

    def extract_hint(err):
        # E.g.,:
        #   UnicodeEncodeError: 'ascii' codec can't encode character
        #     '\u2018' in position 1135: ordinal not in range(128)
        try:
            unknowns = err.object[err.start : err.end]
        except Exception:
            return ""
        else:
            hint = "{}: {}".format(_("Perhaps unknown character(s)"), unknowns)
            return hint

    return _write_config_obj()


# ***


def warn_user_config_errors(errs, which=""):
    """"""

    def _warn_user_config_errors():
        # Don't actually care about unconsumed values (that user specified
        # in their file that do not match any defined config settings) for
        # a few reasons:
        # - First, because plugins. The first time setup_config() is called,
        #            it will not recognize plugin settings.
        # - # Two, there's no harm in unknown config.
        #   MAYBE: (lb): Well, unless it's a user typo, then perhaps
        #            a config-audit command/operation could be useful.
        #            Or just don't effup yerconfig.
        warned = warn_user_config_settings(errs, _("value errors"))
        return warned

    def warn_user_config_settings(lookup, what):
        if not lookup:
            return False
        lines = assemble_lines(lookup)
        msg = _("The {} contains {}:\n{}").format(which, what, "\n".join(lines))
        echo_warning(msg)
        return True

    def assemble_lines(node, keys="", lines=None):
        if lines is None:
            lines = []
        for key, item in node.items():
            if isinstance(item, dict):
                nkey = keys + "." if keys else ""
                assemble_lines(item, nkey + key, lines)
            elif not keys and not item:
                # Unrecognized section.
                lines.append("- [{}]".format(key))
            else:
                lines.append("- {}.{} → {}".format(keys, key, str(item)))
        return lines

    return _warn_user_config_errors()

# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-config#🍐
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
# License: MIT

from gettext import gettext as _

# FIXME/2020-12-14 04:07: Need table printer if this module gonna be useful!
#
#  from dob_bright.reports.render_results import render_results

__all__ = ("echo_config_decorator_table",)


def echo_config_decorator_table(
    cfg_decors,
    exclude_section=False,
    include_hidden=False,
    render_results=lambda results, headers, **kwargs: None,
    **kwargs,
):
    sec_key_vals = []

    def _echo_config_decorator_table():
        for condec in cfg_decors:
            condec.walk(visitor)

        echo_table()

    def visitor(condec, keyval):
        # MAYBE: Option to show hidden config.
        # MAYBE: Option to show generated config.
        if keyval.hidden and not include_hidden:
            return

        val_def = str(keyval.value)
        if val_def != str(keyval.default):
            val_def += val_def and " " or ""
            val_def += encode_default(str(keyval.default))

        val_row = [condec.section_path(sep=".")] if not exclude_section else []
        val_row += [
            keyval.name,
            val_def,
            keyval.doc,
        ]

        sec_key_vals.append(val_row)

    def echo_table():
        headers = [_("Section")] if not exclude_section else []
        headers += [
            _("Name"),
            _("Value {}").format(encode_default(_("Default"))),
            _("Help"),
        ]

        render_results(
            results=sec_key_vals,
            headers=headers,
            **kwargs,
        )

    def encode_default(text):
        # 2019-11-30: (lb): I switched from [square brackets] to <angle brackets>
        # to avoid JSON-encoded lists being [[double bracketed]] (which triggered
        # extra mental cycles upon sight).
        return "<{}>".format(text)

    _echo_config_decorator_table()

# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-config#🍐
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
# License: MIT

"""easy_as_pypi_config sub.package provides Carousel UX user configuration settings."""

from config_decorator.config_decorator import ConfigDecorator

from .fileboss import create_configobj

__all__ = ("decorate_and_wrap",)


def decorate_and_wrap(section_name, section_cdec, complete=False):
    def _decorate_and_wrap():
        # Sink the section once so we can get ConfigObj to print
        # the leading [section_name].
        condec = ConfigDecorator.create_root_for_section(section_name, section_cdec)
        return wrap_in_configobj(condec, complete=complete)

    def wrap_in_configobj(condec, complete=False):
        config_obj = create_configobj(conf_path=None)
        # Set skip_unset so none of the default values are spit out (keeps the
        # config more concise); and set keep_empties so empty sections are spit
        # out (so, e.g., `[default]` at least appears).
        config_obj.merge(
            condec.as_dict(
                skip_unset=not complete,
                keep_empties=not complete,
            )
        )
        return config_obj

    return _decorate_and_wrap()

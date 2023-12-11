# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-config#🍐
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
# License: MIT

import sys

__all__ = ("register_conf_filename",)


def register_conf_filename(conf_filename):
    """Registers default config filename for future package use."""
    this.conf_filename = conf_filename


this = sys.modules[__name__]
this.conf_filename = "app.conf"

# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-config#🍐
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
# License: MIT

from easy_as_pypi_config import defaults
from easy_as_pypi_config.defaults import register_conf_filename


def test_register_conf_filename(filename):
    register_conf_filename(filename)
    assert defaults.conf_filename == filename

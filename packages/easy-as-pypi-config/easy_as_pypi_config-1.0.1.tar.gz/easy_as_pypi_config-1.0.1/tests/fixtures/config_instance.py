# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-config#🍐
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
# License: MIT

import os

import pytest
from configobj import ConfigObj


@pytest.fixture
def config_instance(tmpdir):
    """Provide a (dynamicly generated) ConfigObj instance."""

    def generate_config(**kwargs):
        cfg_dict = generate_dict(**kwargs)
        # NOPE: You'd overwrite your user's file with the default path:
        #   from easy_as_pypi_config.fileboss import default_config_path
        #   configfile_path = default_config_path()
        configfile_path = os.path.join(tmpdir, "easy-as-pypi-config-test.conf")
        config = ConfigObj(configfile_path)
        config.merge(cfg_dict)
        return config

    # ***

    def generate_dict():
        cfg_dict = {
            "foo": {
                "bar": "baz",
            },
        }

        return cfg_dict

    # ***

    return generate_config

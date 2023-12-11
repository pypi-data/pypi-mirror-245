# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-config#🍐
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
# License: MIT

from easy_as_pypi_config.dec_wrap import decorate_and_wrap


def test_decorate_and_wrap_with_complete(basic_config_root):
    config_obj = decorate_and_wrap(
        section_name="a-test!",
        section_cdec=basic_config_root,
        complete=True,
    )
    assert config_obj.dict() == {"a-test!": {"foo": {"bar": ""}}}


def test_decorate_and_wrap_sans_complete(basic_config_root):
    config_obj = decorate_and_wrap(
        section_name="a-test!",
        section_cdec=basic_config_root,
        complete=False,
    )
    assert config_obj.dict() == {"a-test!": {}}

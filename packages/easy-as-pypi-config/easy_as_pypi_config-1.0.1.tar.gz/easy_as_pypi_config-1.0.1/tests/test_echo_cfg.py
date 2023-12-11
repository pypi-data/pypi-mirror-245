# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-config#🍐
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
# License: MIT

from easy_as_pypi_config.echo_cfg import echo_config_decorator_table


def test_echo_config_decorator_table(basic_config_root, capsys, mocker):
    render_results = mocker.MagicMock()
    basic_config_root["foo"]["bar"] = 123
    echo_config_decorator_table(
        cfg_decors=[basic_config_root],
        include_hidden=False,
        render_results=render_results,
    )
    assert render_results.called

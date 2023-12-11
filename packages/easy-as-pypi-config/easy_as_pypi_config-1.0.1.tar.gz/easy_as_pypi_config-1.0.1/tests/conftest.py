# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-config#🍐
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
# License: MIT

"""Provides CLI runner() test fixture, for interacting with Click app."""

import pytest

pytest_plugins = (
    # *** External fixtures.
    # Import tmp_appdirs fixture.
    "easy_as_pypi_appdirs.tests.appdirs_mock",
    # *** Published fixtures.
    # Import fixtures: filename, filepath.
    "easy_as_pypi_config.tests.file_fakes",
    # *** Internal fixtures.
    # Import config_instance fixture.
    "tests.fixtures.config_instance",
    # Import config_root fixture.
    "tests.fixtures.config_root",
)


@pytest.fixture
def app_name():
    return "easy-as-pypi-config-tests"

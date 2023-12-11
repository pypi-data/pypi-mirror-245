# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-config#🍐
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
# License: MIT

import pytest
from config_decorator import section


@pytest.fixture
def basic_config_root():
    @section(None)
    class ConfigRoot(object):
        pass

    @ConfigRoot.section("foo")
    class ConfigurableFoo(object):
        @property
        @ConfigRoot.setting("foo.bar option")
        def bar(self):
            return ""

        @property
        @ConfigRoot.setting("hidden option", hidden=True)
        def boo(self):
            return ""

    @ConfigRoot.section("baz")
    class ConfigurableBaz(object):
        pass

    return ConfigRoot


@pytest.fixture()
def basic_config_file(filepath):
    with open(filepath, "w") as conf_file:
        conf_file.write(
            """
[foo]
bar = 'baz'
bat = 123

[quux]
qiix = 'foo'
""".lstrip()
        )
    return filepath

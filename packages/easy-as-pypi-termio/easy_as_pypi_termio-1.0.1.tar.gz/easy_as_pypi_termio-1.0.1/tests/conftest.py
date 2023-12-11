# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-termio#🍉
# License: MIT

# Copyright (c) © 2018-2023 Landon Bouma. All Rights Reserved.

"""Provides CLI runner() test fixture, for interacting with Click app."""

import pytest

from easy_as_pypi_termio.style import set_coloring


@pytest.fixture
def enable_coloring():
    set_coloring(True)
    yield
    set_coloring(False)

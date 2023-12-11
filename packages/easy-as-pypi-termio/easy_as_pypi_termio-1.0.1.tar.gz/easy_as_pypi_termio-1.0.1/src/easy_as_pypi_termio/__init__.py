# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-termio#🍉
# License: MIT

# Copyright (c) © 2018-2023 Landon Bouma. All Rights Reserved.

"""Top-level package for this CLI-based application."""

# Convenience imports.
#
# - Usage: Lets you simplify imports, e.g., these as equivalent:
#
#     from easy_as_pypi_termio.echoes import click_echo
#
#     from easy_as_pypi_termio import click_echo
#
# - Note: Disable the imported-but-not-used linter rule:
#
#     noqa: F401: Disable: 'foo.bar' imported but unused.

from .echoes import echo_block_header, highlight_value  # noqa: F401
from .errors import (  # noqa: F401
    echo_exit,
    echo_warning,
    exit_warning,
    exit_warning_crude,
)
from .paging import ClickEchoPager, click_echo  # noqa: F401
from .style import attr, bg, coloring, fg, stylize  # noqa: F401

# This version is substituted on poetry-build by poetry-dynamic-versioning.
# - Consequently, __version__ remains empty when installed in 'editable' mode.
__version__ = "1.0.1"

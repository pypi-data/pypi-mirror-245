# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-termio#🍉
# License: MIT

# Copyright (c) © 2018-2023 Landon Bouma. All Rights Reserved.

"""Methods for common terminal echo operations."""

import shutil

from .paging import click_echo
from .style import attr, fg

__all__ = (
    "echo_block_header",
    "highlight_value",
    # PRIVATE:
    #  '__format_block_header',
    # EXTERNAL:
    #  Callers might want to import click_echo from this module, because it
    #  feels more natural here (but it's in paging module because pager-aware).
    "click_echo",
)


# ***


def echo_block_header(title, **kwargs):
    click_echo()
    click_echo(__format_block_header(title, **kwargs))


def __format_block_header(title, sep="━", full_width=False):
    """"""

    def _fact_block_header():
        header = []
        append_highlighted(header, title)
        append_highlighted(header, hr_rule())
        return "\n".join(header)

    def append_highlighted(header, text):
        highlight_col = "red_1"
        header.append(
            "{}{}{}".format(
                fg(highlight_col),
                text,
                attr("reset"),
            )
        )

    def hr_rule():
        if not full_width:
            horiz_rule = sep * len(title)
        else:
            # NOTE: When piping (i.e., no tty), width defaults to 80.
            term_width = shutil.get_terminal_size().columns
            horiz_rule = "─" * term_width
        return horiz_rule

    return _fact_block_header()


# ***


def highlight_value(msg):
    # FIXME: (lb): Replace hardcoding. Assign from styles.conf. #styling
    highlight_color = "medium_spring_green"
    return "{}{}{}".format(fg(highlight_color), msg, attr("reset"))

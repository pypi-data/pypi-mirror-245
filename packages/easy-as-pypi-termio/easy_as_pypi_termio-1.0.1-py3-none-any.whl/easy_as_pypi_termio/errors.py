# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-termio#🍉
# License: MIT

# Copyright (c) © 2018-2023 Landon Bouma. All Rights Reserved.

"""Hamter CLI Nonbusiness Helper modules."""

import sys

import click_hotoffthehamster as click

# MAYBE/2020-12-14 03:25: Remove/replace these hamster-specific alert graphics...
from .ascii_art import infection_notice, lifeless
from .paging import click_echo, flush_pager
from .style import stylize

__all__ = (
    "echo_exit",
    "echo_warning",
    "echoed_warnings_reset",
    "exit_warning",
    "exit_warning_crude",
)


# ***


def exit_warning_crude(msg, crude=True):
    # (lb): I made two similar error-and-exit funcs. See also: exit_warning.
    if crude:
        click_echo()
        click_echo(lifeless().rstrip())
        click_echo(infection_notice().rstrip())
        # click.pause(info='')
    click_echo()
    # FIXME: (lb): Replace hardcoded styles. Assign from styles.conf. #styling
    click_echo(stylize(msg, "yellow_1"))
    sys.exit(1)


# ***


def exit_warning(msg):
    # (lb): I made two similar error-and-exit funcs. See also: exit_warning_crude.
    echo_warning(msg)
    sys.exit(1)


# ***

# In lieu of a module static, e.g.,
#   BEEN_WARNED = [False, ]
# use the slightly less weird looking
# module object instance.
this = sys.modules[__name__]
this.BEEN_WARNED = False


def echo_warning(msg):
    # FIXME: (lb): Replace hardcoded styles. Assign from styles.conf. #styling
    # A lighter red works for white-on-black.
    # - FIXME: Add to 'light'.
    #  click.echo(stylize(msg, 'red_1'), err=True)  # 196
    # Yellow pops and at least says caution. Works for dark.
    # - FIXME: Add to 'night'.
    click.echo(stylize(msg, "yellow_1"), err=True)  # 226
    this.BEEN_WARNED = True


def echoed_warnings_reset():
    been_warned = this.BEEN_WARNED
    this.BEEN_WARNED = False
    return been_warned


# ***


def echo_exit(ctx, message, exitcode=0):
    def _echo_exit(message):
        click_echo(message)
        _flush_pager()
        ctx.exit(exitcode)

    def _flush_pager():
        # To get at the PAGER_CACHE, gotta go through the decorator.
        # So this is quite roundabout.
        @flush_pager
        def __flush_pager():
            pass

        __flush_pager()

    _echo_exit(message)

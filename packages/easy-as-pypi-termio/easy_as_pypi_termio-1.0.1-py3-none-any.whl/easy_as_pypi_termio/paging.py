# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-termio#🍉
# License: MIT

# Copyright (c) © 2018-2023 Landon Bouma. All Rights Reserved.

"""Methods to control paging and manage (accumulate) pager output."""

from functools import update_wrapper

import click_hotoffthehamster as click

from .style import coloring

__all__ = (
    "ClickEchoPager",
    "click_echo",
    "flush_pager",
)


# ***


class ClickEchoPager(object):
    PAGER_ON = False

    PAGER_CACHE = []

    @classmethod
    def disable_paging(cls):
        cls.PAGER_ON = False

    @classmethod
    def enable_paging(cls):
        cls.PAGER_ON = True

    @classmethod
    def paging(cls):
        return cls.PAGER_ON

    @classmethod
    def set_paging(cls, new_paging):
        was_paging = cls.PAGER_ON
        cls.PAGER_ON = new_paging
        return was_paging

    @classmethod
    def flush_pager(cls):
        if cls.paging() and cls.PAGER_CACHE:
            click.echo_via_pager("\n".join(cls.PAGER_CACHE))
        cls.PAGER_CACHE = []

    @classmethod
    def write(cls, message=None, **kwargs):
        if not cls.paging():
            if coloring():
                kwargs["color"] = True
            if "nl" not in kwargs:
                kwargs["nl"] = False
            click.echo(message, **kwargs)
        else:
            # Collect echoes and show at end, otherwise every call
            # to echo_via_pager results in one pager session, and
            # user has to click 'q' to see each line of output!
            cls.PAGER_CACHE.append(message or "")


# ***


def click_echo(message=None, **kwargs):
    if "nl" not in kwargs:
        kwargs["nl"] = True
    ClickEchoPager.write(message, **kwargs)


# ***


def flush_pager(func):
    def flush_echo(*args, **kwargs):
        func(*args, **kwargs)
        ClickEchoPager.flush_pager()

    return update_wrapper(flush_echo, func)

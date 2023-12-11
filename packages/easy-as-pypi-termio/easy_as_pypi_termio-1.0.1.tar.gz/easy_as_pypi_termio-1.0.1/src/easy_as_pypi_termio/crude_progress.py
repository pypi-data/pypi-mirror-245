# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-termio#🍉
# License: MIT

# Copyright (c) © 2018-2023 Landon Bouma. All Rights Reserved.

"""Hamter CLI Nonbusiness Helper modules."""

import shutil

from .paging import click_echo

__all__ = ("CrudeProgress",)


class CrudeProgress(object):
    """"""

    def __init__(self, enabled):
        self.enabled = enabled

    # (lb): This is a very crude progress indicator.
    #   I should just Google and find one.
    #   But this does in a pinch. And really how useful is it?
    #   I'm working on a 400-factoid import file, and the only
    #   function that's noticeably slow is must_not_conflict_existing.
    def click_echo_current_task(self, task, no_clear=False):
        if not self.enabled:
            return

        def _click_echo_current_task():
            term_width = shutil.get_terminal_size().columns
            cursor_to_leftmost_column()
            if not no_clear:
                click_echo(" " * term_width, nl=False)  # "Clear" cursor line.
                cursor_to_leftmost_column()
            click_echo(task, nl=False)
            cursor_to_leftmost_column()
            # Move cursor past text.
            cursor_to_column_at(len(task) + 1)

        def cursor_to_leftmost_column():
            # FIXME: (lb): Can we use PPT to do cursoring? So that it detects terminal.
            #   Like, this'll work for me in my terminal, but what about, e.g., Windows?
            # MAGIC_CONTROL_CODE: Move cursor all the way left.
            click_echo("\u001b[1000D", nl=False)

        def cursor_to_column_at(col_num):
            # FIXME: (lb): Should be a PPT call or otherwise terminal-agnostic,
            #        and not specify a control code directly.
            click_echo("\u001b[" + str(col_num) + "C", nl=False)

        _click_echo_current_task()

    def start_crude_progressor(self, task_descrip):
        if not self.enabled:
            return

        self.click_echo_current_task(task_descrip)
        term_width = shutil.get_terminal_size().columns - len(task_descrip) - 1
        dot_count = 0
        fact_sep = "."
        return term_width, dot_count, fact_sep

    def step_crude_progressor(self, task_descrip, term_width, dot_count, fact_sep):
        if not self.enabled:
            return

        dot_count += 1
        if dot_count >= term_width:
            self.click_echo_current_task(task_descrip, no_clear=True)
            dot_count = 1
            fact_sep = ";" if fact_sep == "." else "."
        click_echo(fact_sep, nl=False)
        return term_width, dot_count, fact_sep

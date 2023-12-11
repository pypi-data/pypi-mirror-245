# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-termio#🍉
# License: MIT

# Copyright (c) © 2018-2023 Landon Bouma. All Rights Reserved.

from unittest import mock

import click_hotoffthehamster as click

from easy_as_pypi_termio.crude_progress import CrudeProgress


class TestCrudeProgress:
    @mock.patch.object(click, "echo")
    def test_enabled_off(self, click_echo_mock):
        progger = CrudeProgress(enabled=False)
        progger.click_echo_current_task(task="testing-disabled")
        progger.start_crude_progressor(task_descrip="testing-start")
        progger.step_crude_progressor("it", "just", "doesn't", "matter")
        assert not click_echo_mock.called

    @mock.patch.object(click, "echo")
    def test_enabled_on(self, click_echo_mock):
        progger = CrudeProgress(enabled=True)

        progger.click_echo_current_task(task="testing-echo")
        assert click_echo_mock.called
        click_echo_mock.reset_mock

        term_width, dot_count, fact_sep = progger.start_crude_progressor(
            task_descrip="testing-start",
        )
        assert click_echo_mock.called
        click_echo_mock.reset_mock

        # Set dot_count >= term_width to cover the if-branch in the function
        # (that has no else-branch). (And luckily this isn't JS coverage, or
        # we'd have to  hit the else branch, too, which doesn't exist.)
        term_width, dot_count, fact_sep = progger.step_crude_progressor(
            "testing-step",
            term_width,
            dot_count=term_width,
            fact_sep=fact_sep,
        )
        assert click_echo_mock.called

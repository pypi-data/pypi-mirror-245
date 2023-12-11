# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-termio#🍉
# License: MIT

# Copyright (c) © 2018-2023 Landon Bouma. All Rights Reserved.

from unittest import mock

import click_hotoffthehamster as click
import pytest

from easy_as_pypi_termio.echoes import echo_block_header, highlight_value


@mock.patch.object(click, "echo")
def test_echo_block_header_basic(click_echo_mock):
    echo_block_header("foo")
    assert click_echo_mock.called


@pytest.mark.parametrize(("full_width",), ((True,), (False,)))
def test_echo_block_header_full_width(full_width, mocker):
    # @parametrize and @patch don't mix, apparently.
    click_echo_mock = mocker.patch.object(click, "echo")
    echo_block_header("foo", full_width=full_width)
    assert click_echo_mock.called


def test_highlight_value(enable_coloring):
    highlight_color = highlight_value("foo")
    assert highlight_color == "\x1b[38;5;49mfoo\x1b[0m"

# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-termio#🍉
# License: MIT

# Copyright (c) © 2018-2023 Landon Bouma. All Rights Reserved.

from unittest import mock

import click_hotoffthehamster as click
import pytest

from easy_as_pypi_termio.errors import (
    echo_exit,
    echo_warning,
    echoed_warnings_reset,
    exit_warning,
    exit_warning_crude,
)


@mock.patch.object(click, "echo")
def test_exit_warning_crude(click_echo_mock):
    with pytest.raises(SystemExit):
        exit_warning_crude("foo")
    assert click_echo_mock.called


@mock.patch.object(click, "echo")
def test_exit_warning(click_echo_mock):
    with pytest.raises(SystemExit):
        exit_warning("foo")
    assert click_echo_mock.called


@mock.patch.object(click, "echo")
def test_echo_warning(click_echo_mock):
    echo_warning("foo")
    assert click_echo_mock.called


@mock.patch.object(click, "echo")
def test_echoed_warnings_reset(click_echo_mock):
    echo_warning("foo")
    been_warned = echoed_warnings_reset()
    assert been_warned
    been_warned = echoed_warnings_reset()
    assert not been_warned


@mock.patch.object(click, "echo")
def test_echo_exit(click_echo_mock, mocker):
    ctx = mocker.MagicMock()
    echo_exit(ctx, "foo")
    assert click_echo_mock.called
    assert ctx.exit.called

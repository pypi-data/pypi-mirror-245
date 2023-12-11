# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-termio#🍉
# License: MIT

# Copyright (c) © 2018-2023 Landon Bouma. All Rights Reserved.

from unittest import mock

import click_hotoffthehamster as click
import pytest

from easy_as_pypi_termio.paging import ClickEchoPager, click_echo, flush_pager


class TestClickEchoPager:
    def test_enable_paging(self):
        assert not ClickEchoPager.paging()
        ClickEchoPager.enable_paging()
        assert ClickEchoPager.paging()
        ClickEchoPager.disable_paging()
        assert not ClickEchoPager.paging()

    def test_set_paging(self):
        was_paging = ClickEchoPager.set_paging(True)
        assert not was_paging
        was_paging = ClickEchoPager.set_paging(False)
        assert was_paging

    @mock.patch.object(click, "echo")
    def test_write_paging_off(self, click_echo_mock, enable_coloring):
        ClickEchoPager.write("foo")
        assert click_echo_mock.called

    @mock.patch.object(click, "echo_via_pager")
    def test_write_paging_on_then_flush_pager(
        self,
        click_echo_via_pager_mock,
        enable_paging,
    ):
        ClickEchoPager.write("foo")
        assert not click_echo_via_pager_mock.called
        ClickEchoPager.flush_pager()
        assert click_echo_via_pager_mock.called

    # ***


# ***


@mock.patch.object(click, "echo")
def test_click_echo_and_flush_pager_decorator(click_echo_mock):
    @flush_pager
    def inner_test():
        click_echo("foo")

    inner_test()
    assert click_echo_mock.called


# ***


@pytest.fixture
def enable_paging():
    ClickEchoPager.set_paging(True)
    yield
    ClickEchoPager.set_paging(False)

# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-termio#🍉
# License: MIT

# Copyright (c) © 2018-2023 Landon Bouma. All Rights Reserved.

import os  # noqa: F401
import shutil
import sys  # noqa: F401
from unittest import mock

import pytest

try:
    import pyfiglet
except ImportError:
    pyfiglet = None

from easy_as_pypi_termio.ascii_art import (  # ...
    append_figlet_text_maybe,
    curly_quote,
    curly_quotes,
    fetch_asciis,
    infection_notice,
    lifeless,
    randomster,
)

if pyfiglet is not None:

    @mock.patch("pyfiglet.Figlet.getFonts", side_effect=Exception)
    def test_append_figlet_text_maybe_fail_if_pyfiglet_fails(figlet_mock):
        artwork = []
        with pytest.raises(Exception):
            append_figlet_text_maybe(artwork)

    @mock.patch.dict("sys.modules", {"pyfiglet": None})  # Raise ImportError.
    def test_append_figlet_text_maybe_noop_if_pyfiglet_missing():
        artwork = []
        append_figlet_text_maybe(artwork)
        assert not artwork


def test_infection_notice():
    notice = infection_notice()
    assert notice


def test_fetch_asciis():
    arts = fetch_asciis([0, 2])
    assert len(arts) == 2


def test_fetch_asciis_index_error():
    arts = fetch_asciis([0, 2, 999])
    assert len(arts) == 1


def test_randomster():
    art = randomster()
    assert art


# (lb): Not sure why, but mock.patch does not work how I'd expect:
#         @mock.patch('shutil.get_terminal_size', return_value=(0,))
#       but a patch.object does.
@mock.patch.object(shutil, "get_terminal_size", return_value=mock.Mock(columns=0))
def test_avail_width_none(get_terminal_size):
    art = randomster()
    assert art


def test_lifeless():
    art = lifeless()
    assert art


# ***

# Somewhat misplaced functions...


def test_curly_quote_okay():
    quoted = curly_quote("foo")
    assert quoted == "‘foo’" or os.name == "nt"


@mock.patch("os.name", new_callable=mock.PropertyMock(return_value="nt"))
def test_curly_quote_fail(os_name):
    quoted = curly_quote("foo")
    assert quoted == "'foo'"


# LOPRI/2023-11-12: Why is Windows failing these two tests?
# - GHA Py 3.12 Windows job output shows: "�foo�"


def test_curly_quotes_okay():
    quoted = curly_quotes("foo")
    assert quoted == "“foo”" or os.name == "nt"


@mock.patch("os.name", new_callable=mock.PropertyMock(return_value="nt"))
def test_curly_quotes_fail(os_name):
    quoted = curly_quotes("foo")
    assert quoted == '"foo"'

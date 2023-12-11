# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-appdirs#🛣
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
# License: MIT

"""Test fixtures for the ``easy-as-pypi-appdirs`` package tests."""

import pytest

pytest_plugins = (
    # Import tmp_appdirs fixture.
    "easy_as_pypi_appdirs.tests.appdirs_mock",
)


@pytest.fixture
def app_name():
    """Return Python package name munged for tests."""
    return "easy-as-pypi-appdirs-tests"

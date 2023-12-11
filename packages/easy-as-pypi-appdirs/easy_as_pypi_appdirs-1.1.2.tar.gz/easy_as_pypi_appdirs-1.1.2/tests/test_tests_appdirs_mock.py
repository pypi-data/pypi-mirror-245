# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-appdirs#🛣
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
# License: MIT

"""Tests the tests subpackage appdirs_mock module."""

import os

import pytest

from easy_as_pypi_appdirs import register_application


class TestTestsAppdirsMock:
    @pytest.fixture(autouse=True)
    def register_application(self, app_name):
        register_application(app_name)

    def test_tests_tmp_appdirs_mock_side_effect(self, tmp_appdirs):
        adir_path = tmp_appdirs.user_cache_dir
        assert os.path.exists(adir_path)

    def test_tests_tmp_appdirs_mock_safe_effect(self, tmp_appdirs):
        adir_path = tmp_appdirs.safe.user_cache_dir
        assert not os.path.exists(adir_path)

    def test_tests_xdg_appdirs_mock_side_effect(self, xdg_appdirs):
        # 2022-10-04: Testing on macOS via GitHub Actions now, and the
        # `assert not os.path.exists(adir_path)` in the next test,
        # test_tests_xdg_appdirs_mock_safe_effect, fails. So we'll remove
        # that directory at the end of this function. And we'll assert
        # that the directory does not exist at the start of this test.
        adir_path = xdg_appdirs.safe.user_cache_dir
        assert not os.path.exists(adir_path)

        adir_path = xdg_appdirs.user_cache_dir
        assert os.path.exists(adir_path)

        # Not sure why, but next text fails in macOS (via GitHub actions)
        # because directory exists. So remove the directory. This os.rmdir
        # is not necessary when I test locally on Ubuntu (I have not tried
        # locally on macOS).
        os.rmdir(adir_path)

    def test_tests_xdg_appdirs_mock_safe_effect(self, xdg_appdirs):
        adir_path = xdg_appdirs.safe.user_cache_dir
        assert not os.path.exists(adir_path)

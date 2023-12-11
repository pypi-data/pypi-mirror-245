# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-appdirs#🛣
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
# License: MIT

"""Tests the expand_and_mkdirs.py module."""

import os
from unittest import mock

import pytest

from easy_as_pypi_appdirs import AppDirs, must_ensure_appdirs_path, register_application


class TestMustGetAppDirsSubDirFilePath:
    @pytest.fixture(autouse=True)
    def register_application(self, app_name):
        register_application(app_name)

    def _test_must_ensure_appdirs_path(self, appd_base):
        path_base = "foo"
        path_file = "bar.bat"
        backup_fullpath = must_ensure_appdirs_path(
            file_basename=path_file,
            dir_dirname=path_base,
            appdirs_dir=appd_base,
        )

        if not appd_base:
            appd_base = AppDirs.user_cache_dir
        assert backup_fullpath == os.path.join(appd_base, path_base, path_file)

        return backup_fullpath

    def test_with_appdirs_dir(self, tmpdir):
        self._test_must_ensure_appdirs_path(tmpdir)

    def test_sans_appdirs_dir(self):
        with mock.patch(
            "os.makedirs",
            new_callable=mock.PropertyMock,
        ) as mock_os_makedirs:
            appd_base = AppDirs().user_cache_dir
            self._test_must_ensure_appdirs_path(appd_base)
            assert mock_os_makedirs.called

    def test_fallsback_on_user_cache_dir(self, tmp_appdirs):
        self._test_must_ensure_appdirs_path(appd_base=None)

    def test_raises_if_user_cache_dir_cannot_be_created(self, tmp_appdirs):
        with mock.patch(
            "easy_as_pypi_appdirs.AppDirs.user_cache_dir",
            new_callable=mock.PropertyMock,
        ) as mock_user_cache_dir:
            mock_user_cache_dir.side_effect = Exception("forced test failure")
            with pytest.raises(Exception):
                self._test_must_ensure_appdirs_path(appd_base=None)

    def test_raises_if_file_path_exists_but_not_a_file(self, tmp_appdirs):
        file_path = self._test_must_ensure_appdirs_path(appd_base=None)
        # Create not a file, e.g., not pathlib.Path(file_path).touch():
        os.makedirs(file_path)
        with pytest.raises(Exception):
            self._test_must_ensure_appdirs_path(appd_base=None)

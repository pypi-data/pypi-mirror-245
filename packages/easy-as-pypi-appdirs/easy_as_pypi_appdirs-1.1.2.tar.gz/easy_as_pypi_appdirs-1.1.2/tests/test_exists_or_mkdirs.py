# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-appdirs#🛣
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
# License: MIT

"""Tests the exists_or_mkdirs.py module."""

import os

from easy_as_pypi_appdirs import (
    must_ensure_directory_exists,
    must_ensure_file_path_dirred,
)


class TestMustEnsureDirectoryExists(object):
    """must_ensure_directory_exists test(s)."""

    def test_must_ensure_directory_exists(self, tmpdir):
        ensure_this_path = os.path.join(tmpdir, "foo")
        assert not os.path.exists(ensure_this_path)
        must_ensure_directory_exists(ensure_this_path)
        assert os.path.exists(ensure_this_path)


class TestMustEnsureFilePathDirred(object):
    """must_ensure_file_path_dirred test(s)."""

    def test_must_ensure_file_path_dirred(self, tmpdir):
        ensure_this_path = os.path.join(tmpdir, "foo")
        ensure_this_file = os.path.join(ensure_this_path, "bar.bat")
        assert not os.path.exists(ensure_this_path)
        must_ensure_file_path_dirred(ensure_this_file)
        assert os.path.exists(ensure_this_path)

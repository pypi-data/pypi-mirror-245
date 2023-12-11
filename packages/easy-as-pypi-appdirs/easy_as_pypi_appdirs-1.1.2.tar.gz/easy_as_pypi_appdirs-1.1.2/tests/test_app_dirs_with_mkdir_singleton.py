# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-appdirs#🛣
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
# License: MIT

"""Tests the AppDirsWithMkdir class init branches."""

import pytest

from easy_as_pypi_appdirs import AppDirs
from easy_as_pypi_appdirs.singleton import Singleton


class FooAppDirs(AppDirs, metaclass=Singleton):
    pass


class BarAppDirs(AppDirs, metaclass=Singleton):
    pass


class TestAppDirsWithMkdirSingleton(object):
    @pytest.fixture(autouse=True)
    def resets_instances(self):
        yield  # run the test_().
        Singleton._reset_instances()

    def test_raises_on_instantiation_without_initialization(self):
        # Because other tests call register_application, must reset.
        Singleton._reset_instances()

        with pytest.raises(Exception):
            AppDirs()

    def test_raises_on_instantiation_twice_with_different_appnames(self):
        AppDirs("foo")
        with pytest.raises(Exception):
            AppDirs("bar")

    def test_returns_separate_instances_with_different_classes(self):
        foo = FooAppDirs("baz")
        bar = BarAppDirs("baz")
        assert foo is not bar

    def test_returns_same_instance_after_being_initialized(self):
        foo = AppDirs("baz")
        bar = AppDirs()
        baz = AppDirs()
        assert foo is bar
        assert bar is baz

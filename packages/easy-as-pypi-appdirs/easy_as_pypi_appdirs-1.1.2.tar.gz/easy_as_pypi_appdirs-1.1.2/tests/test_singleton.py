# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-appdirs#🛣
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
# License: MIT

"""Tests the singleton.py module."""

from easy_as_pypi_appdirs.singleton import Singleton


class FooSingleton(object, metaclass=Singleton):
    pass


class BarSingleton(object, metaclass=Singleton):
    pass


class TestSingleton:
    def test_singleton_returns_same_object_same_classes(self):
        foo1 = FooSingleton()
        foo2 = FooSingleton()
        assert foo1 is foo2

    def test_singleton_returns_different_object_different_classes(self):
        foo = FooSingleton()
        bar = BarSingleton()
        assert foo is not bar

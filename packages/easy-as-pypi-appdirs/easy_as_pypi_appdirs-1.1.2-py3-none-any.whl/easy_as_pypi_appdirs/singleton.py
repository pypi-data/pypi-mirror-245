# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-appdirs#🛣
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
# License: MIT

"""Singleton metaclass."""

__all__ = ("Singleton",)


class Singleton(type):
    """A Singleton metaclass.

    For a healthy discussion on ways to implement Singleton in Python,
    and whether or not they're a good tool to use, read the long-standing
    and still-rolling *Creating a singleton in Python* article:

        https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Return Singleton for specified class and optional arguments.

        Creates Singleton if necessary, or verifies specified arguments
        match previously-created Singleton for the same arguments.
        """
        fresh_cls = cls not in cls._instances
        if fresh_cls or args or kwargs:
            new_instance = super(Singleton, cls).__call__(*args, **kwargs)

        if fresh_cls:
            cls_instance = new_instance
            cls._instances[cls] = cls_instance
        else:
            cls_instance = cls._instances[cls]

        if (args or kwargs) and (new_instance != cls_instance):
            raise Exception("DEV: Singleton initialized again but differently")

        return cls_instance

    @classmethod
    def _reset_instances(cls):
        cls._instances = {}

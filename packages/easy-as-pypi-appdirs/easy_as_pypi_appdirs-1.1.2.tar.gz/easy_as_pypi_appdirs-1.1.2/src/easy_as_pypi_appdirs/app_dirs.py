# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-appdirs#🛣
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
# License: MIT

"""Register an application and receive a handle to the singleton."""

from .app_dirs_with_mkdir import AppDirsWithMkdir

__all__ = ("register_application",)


def register_application(package_name):
    """Register appname for future uses of AppDirsWithMkdir."""
    # This should be the first time this class is instantiated,
    # because it's a singleton. Otherwise, the constructor will
    # raise on it having already been called.
    new_singleton = AppDirsWithMkdir(appname=package_name)
    return new_singleton

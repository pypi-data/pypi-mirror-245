# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-appdirs#🛣
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
# License: MIT

"""AppDirs subclass adds mkdir side effect."""

from functools import update_wrapper

import appdirs

from .exists_or_mkdirs import must_ensure_directory_exists
from .singleton import Singleton

__all__ = (
    "AppDirsWithMkdir",
    # PRIVATE:
    #  'mkdir_side_effect',
)


def mkdir_side_effect(func):
    def _mkdir_side_effect(app_dirs, *args, **kwargs):
        app_dir_path = func(app_dirs, *args, **kwargs)
        if app_dirs.create:
            # Ensure path exists, which might raise, most likely one of:
            #   PermissionError, FileExistsError, or NotADirectoryError.
            must_ensure_directory_exists(app_dir_path)
        return app_dir_path

    return update_wrapper(_mkdir_side_effect, func)


# aka AppDirsWithMkdirSideEffect
class AppDirsWithMkdir(appdirs.AppDirs, metaclass=Singleton):
    """Singleton AppDirs with ``mkdir`` side effect.

    - As a Singleton, this class can be instantiated and used without
      knowing the appname, provided some bootstrap code registers it.

      E.g., when the app is first loaded, have it call::

        first_instance = AppDirsWithMkdir(appname='my-awesome-app')

      and then, later, access the same instance by instantiating anew:

        user_data_dir = AppDirsWithMkdir().user_data_dir

    - Has a Side effect, which is that, just by querying a directory
      path, this class creates that path, or ensures it exists.

      The author (lb) isn't super jazzed by this "feature", but it
      was useful to get a downstream app up and running more easily
      without having to manage mkdir'ing application directories...
      and now it's been baked in so long I don't want to spend the
      time changing it... it's just something of which to be aware:

      - Asking for an application directory path may create that path.

    - Regarding Singleton (again), which is not the most respected
      pattern (some might say it's always a smell), consider this
      classic discussion on ways to implement Singleton in Python,
      and whether or not they're a good idea:

      - *Creating a singleton in Python*:

        https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    """

    # Although the class is a Singleton, a user may need to access the class
    # without actually creating it or before it's actually created. So here's
    # a (hacky) class member to indicate when the singleton instance is ready.
    is_ready = None

    def __init__(self, *args, **kwargs):
        """Add create flag value to instance."""
        # The appdirs.AppDirs base class takes a number of parameters:
        #   appname=None,
        #   appauthor=None,
        #   version=None,
        #   roaming=False,
        #   multipath=False,
        # but we only care about appname.
        super(AppDirsWithMkdir, self).__init__(*args, **kwargs)
        self._raise_if_appname_not_specified()
        AppDirsWithMkdir.is_ready = True
        self._default_ensure_dirs_on_query()

    def __eq__(self, other):
        """Compare two AppDirsWithMkdir using the ``appname`` for each object."""
        return self.appname == other.appname

    def _raise_if_appname_not_specified(self):
        if self.appname:
            return

        msg = "DEV: Call register_application before using AppDirs or AppDirsWithMkdir."
        raise Exception(msg)

    def _default_ensure_dirs_on_query(self):
        # FIXME: (lb): I'm not super cool with this side-effect:
        #          Calling any property herein will cause its
        #          directory path to be created! Creating paths
        #          should be a deliberate action and not a side effect
        #          of just asking for a path. In any case, it currently
        #          works this way, so just rolling with the flow, for now.
        #        See Click: it has concept of lazy-creating paths, i.e.,
        #          only create path when a file therein opened for write.
        self.create = True

    # ***

    @property
    def safe(self):
        """Return parent object, without `mkdirs -p` side effect."""
        return super(AppDirsWithMkdir, self)

    # ***

    @property
    @mkdir_side_effect
    def user_data_dir(self):
        """Return ``user_data_dir``."""
        return appdirs.AppDirs.user_data_dir.fget(self)

    @property
    @mkdir_side_effect
    def site_data_dir(self):
        """Return ``site_data_dir``."""
        return appdirs.AppDirs.site_data_dir.fget(self)

    @property
    @mkdir_side_effect
    def user_config_dir(self):
        """Return ``user_config_dir``."""
        return appdirs.AppDirs.user_config_dir.fget(self)

    @property
    @mkdir_side_effect
    def site_config_dir(self):
        """Return ``site_config_dir``."""
        return appdirs.AppDirs.site_config_dir.fget(self)

    @property
    @mkdir_side_effect
    def user_cache_dir(self):
        """Return ``user_cache_dir``."""
        return appdirs.AppDirs.user_cache_dir.fget(self)

    @property
    @mkdir_side_effect
    def user_state_dir(self):
        """Return ``user_state_dir``."""
        return appdirs.AppDirs.user_state_dir.fget(self)

    @property
    @mkdir_side_effect
    def user_log_dir(self):
        """Return ``user_log_dir``."""
        return appdirs.AppDirs.user_log_dir.fget(self)

    # ***


# ***

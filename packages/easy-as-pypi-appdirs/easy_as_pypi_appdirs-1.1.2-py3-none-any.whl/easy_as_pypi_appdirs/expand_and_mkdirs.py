# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-appdirs#🛣
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
# License: MIT

"""Helper function tries to make AppDirs path directories, if necessary, or raises."""

import os
from gettext import gettext as _

from .app_dirs_with_mkdir import AppDirsWithMkdir
from .exists_or_mkdirs import must_ensure_directory_exists

__all__ = ("must_ensure_appdirs_path",)

DEFAULT_APPDIRS_FILE_BASENAME_FMT = "{}"


def must_ensure_appdirs_path(
    file_basename,
    dir_dirname,
    appdirs_dir=None,
    basename_fmt=DEFAULT_APPDIRS_FILE_BASENAME_FMT,
):
    """Return the path to a file stored in a subdirectory of an AppDirs directory."""

    def _must_ensure_appdirs_path():
        app_dir_path = must_use_user_cache_dir_unless_appdirs_dir()
        full_path = expand_path_and_ensure_parents_exist(app_dir_path)
        must_verify_path_does_not_exist_or_is_a_file(full_path)
        return full_path

    def must_use_user_cache_dir_unless_appdirs_dir():
        # Returns the app_dir caller specified, or AppDirs.user_cache_dir.
        if appdirs_dir:
            return appdirs_dir

        return must_use_user_cache_dir()

    def must_use_user_cache_dir():
        # Repackages mkdir side effect exception if raises, and re-raises;
        # otherwise returns fallback app. dir. for path, `user_cache_dir`.
        try:
            return AppDirsWithMkdir().user_cache_dir
        except Exception as err:
            exceptional_path = AppDirsWithMkdir().safe.user_cache_dir
            msg = _(
                "{}: {} ‘{}’ {} “{}” ({})",
            ).format(
                _("ERROR"),
                _("Failed to create"),
                "user_cache_dir",
                _("path at"),
                exceptional_path,
                str(err),
            )
            raise Exception(msg)

    def expand_path_and_ensure_parents_exist(app_dir_path):
        subdir_path = os.path.join(app_dir_path, dir_dirname)
        # This must() raises, e.g., PermissionError, if os.makedirs fails.
        must_ensure_directory_exists(subdir_path)
        full_path = os.path.join(subdir_path, basename_fmt.format(file_basename))
        return full_path

    def must_verify_path_does_not_exist_or_is_a_file(full_path):
        if not os.path.exists(full_path) or os.path.isfile(full_path):
            return

        msg = _(
            "{}: {} ‘{}’ {} “{}”",
        ).format(
            _("ERROR"),
            _("Path exists for"),
            "user_cache_dir",
            _("but it‘s not a file"),
            full_path,
        )
        raise Exception(msg)

    return _must_ensure_appdirs_path()

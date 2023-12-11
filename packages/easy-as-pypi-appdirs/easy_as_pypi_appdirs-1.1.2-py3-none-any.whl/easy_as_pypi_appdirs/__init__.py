# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-appdirs#🛣
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
# License: MIT

"""Top-level package for this CLI-based application."""

# Convenience import(s).

import appdirs  # noqa: F401

from .app_dirs import register_application  # noqa: F401
from .app_dirs_with_mkdir import AppDirsWithMkdir as AppDirs  # noqa: F401
from .exists_or_mkdirs import (  # noqa: F401
    must_ensure_directory_exists,
    must_ensure_file_path_dirred,
)
from .expand_and_mkdirs import must_ensure_appdirs_path  # noqa: F401

# This version value is substituted on poetry-build. See pyproject.toml:
#   [tool.poetry-dynamic-versioning.substitution]
# - So when installed in 'editable' mode, the substitution does not happen,
#   and __version__ remains "".
#   - But we only use __version__ for .github/workflows/release-smoke-test.yml
#     and not for anything else (otherwise we could check Git tags when
#     __version__ == "", if we assume an 'editable' mode install only happens
#     on a dev machine).
__version__ = "1.1.2"

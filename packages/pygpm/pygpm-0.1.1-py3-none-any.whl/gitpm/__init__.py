# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

"""
gitpm - A git repository manager
"""

from pygpm.core import __version__
from pygpm.logging import init_logging

__all__ = ["__version__"]

init_logging()

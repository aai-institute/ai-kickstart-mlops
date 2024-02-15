"""Utilities."""

import os
from typing import List

from ames_housing.constants import LAKEFS_BRANCH, LAKEFS_REPOSITORY


def get_key_prefix() -> List[str]:
    if os.environ.get("ENV") == "production":
        return [LAKEFS_REPOSITORY, LAKEFS_BRANCH]
    return []

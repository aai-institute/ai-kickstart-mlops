"""Pickle file object in lakeFS IO manager."""

from typing import Any

import joblib
from lakefs.object import LakeFSIOBase

from ames_housing.io_managers.base_lakefs_io_manager import BaseLakeFSIOManager


class PickleLakeFSIOManager(BaseLakeFSIOManager):
    """Pickle file object in lakeFS IO manager.

    This IO manager serializes Python objects to Pickle files in a lakeFS repository
    using joblib.
    """

    extension: str = ".pkl"

    def write_output(self, f: LakeFSIOBase, obj: Any) -> None:
        """Write the Python object to a pickle file in lakeFS."""
        joblib.dump(obj, f)

    def read_input(self, f: LakeFSIOBase) -> Any:
        """Load pickle file from lakeFS into Python object."""
        return joblib.load(f)

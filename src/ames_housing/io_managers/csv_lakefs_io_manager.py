"""CSV lakeFS IO manager."""

import pandas as pd
from lakefs.object import LakeFSIOBase

from ames_housing.io_managers.base_lakefs_io_manager import BaseLakeFSIOManager


class CSVLakeFSIOManager(BaseLakeFSIOManager):
    """CSV lakeFS IO manager.

    This IO manager serializes data frames to CSV file objects in a lakeFS repository.
    """

    extension: str = ".csv"

    def write_output(self, f: LakeFSIOBase, obj: pd.DataFrame) -> None:
        """Write the data frame to a CSV file on lakeFS."""
        obj.to_csv(f)

    def read_input(self, f: LakeFSIOBase) -> pd.DataFrame:
        """Load the CSV file from lakeFS into a data frame."""
        return pd.read_csv(f)

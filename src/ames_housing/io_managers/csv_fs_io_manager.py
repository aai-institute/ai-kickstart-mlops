""""CSV file system IO manager"""

import os

import pandas as pd
from dagster import InputContext, OutputContext

from ames_housing.io_managers.base_fs_io_manager import BaseFileSystemIOManager


class CSVFileSystemIOManager(BaseFileSystemIOManager):
    """CSV file system IO manager.

    This IO manager serializes Pandas data frames to CSV files on the local file system.

    Attributes
    ----------
    extension : str
        File extension, by default ".csv".
    """

    extension: str = ".csv"

    def handle_output(self, context: OutputContext, obj: pd.DataFrame) -> None:
        """Write the data frame to a CSV file.

        Parameters
        ----------
        context : OutputContext
            Dagster context.
        obj : pd.DataFrame
            Data frame that will be written to a CSV file.
        """
        path = self._get_path(context)
        os.makedirs(os.path.dirname(path), exist_ok=True)

        context.log.debug(f"Writing file at: {path}")
        obj.to_csv(path)

    def load_input(self, context: InputContext) -> pd.DataFrame:
        """Load CSV file into a data frame.

        Parameters
        ----------
        context : InputContext
            Dagster context.

        Returns
        -------
        pd.DataFrame
            Data frame with the contents of the CSV file.
        """
        path = self._get_path(context)

        context.log.debug(f"Loading file from: {path}")
        return pd.read_csv(self._get_path(context))

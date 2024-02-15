"""CSV lakeFS IO manager."""

import pandas as pd
from dagster import InputContext, OutputContext

from ames_housing.io_managers.base_lakefs_io_manager import BaseLakeFSIOManager


class CSVLakeFSIOManager(BaseLakeFSIOManager):
    """CSV lakeFS IO manager.

    This IO manager serializes data frames to CSV file objects in a lakeFS repository.
    """

    extension: str = ".csv"

    def handle_output(self, context: OutputContext, obj: pd.DataFrame) -> None:
        """Write the data frame to a CSV file on lakeFS.

        Parameters
        ----------
        context : OutputContext
            Dagster context.
        obj : pd.DataFrame
            Data frame that will be serialized to a CSV file in lakeFS.
        """
        with self.transaction(context) as tx:
            with self.open(self.get_path(context, transaction=tx), "w") as f:
                context.log.debug(f"Writing file at: {self.get_path(context)}")
                obj.to_csv(f)

            asset_without_repo_branch = "/".join(context.asset_key.path[2:])
            tx.commit(message=f"Add asset {asset_without_repo_branch}")

    def load_input(self, context: InputContext) -> pd.DataFrame:
        """Load CSV file from lakeFS into a data frame.

        Parameters
        ----------
        context : InputContext
            Dagster context.

        Returns
        -------
        pd.DataFrame
            Data frame with the contents of the CSV file.
        """
        path = self.get_path(context)
        with self.open(path, "r") as f:
            result = pd.read_csv(f)
        return result

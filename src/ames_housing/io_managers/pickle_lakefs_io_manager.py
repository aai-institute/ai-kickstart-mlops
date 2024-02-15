"""Pickle file object in lakeFS IO manager."""

from typing import Any

import joblib
from dagster import InputContext, OutputContext

from ames_housing.io_managers.base_lakefs_io_manager import BaseLakeFSIOManager


class PickleLakeFSIOManager(BaseLakeFSIOManager):
    """Pickle file object in lakeFS IO manager.

    This IO manager serializes Python objects to Pickle files in a lakeFS repository
    using joblib.
    """

    extension: str = ".pkl"

    def handle_output(self, context: OutputContext, obj: Any) -> None:
        """Write Python object to a pickle file in lakeFS.

        Parameters
        ----------
        context : OutputContext
            Dagster context.
        obj : Any
            Python object that will be serialized to a pickle file.
        """
        with self.transaction(context) as tx:
            with self.open(self.get_path(context, transaction=tx), "wb") as f:
                context.log.debug(f"Writing file at: {self.get_path(context)}")
                joblib.dump(obj, f)

            asset_without_repo_branch = "/".join(context.asset_key.path[2:])
            tx.commit(message=f"Add asset {asset_without_repo_branch}")

    def load_input(self, context: InputContext) -> Any:
        """Load pickle file from lakeFS into Python object.

        Parameters
        ----------
        context : InputContext
            Dagster context.

        Returns
        -------
        Any
            Python object deserialized from the pickle file.
        """
        path = self.get_path(context)
        with self.open(path, "rb") as f:
            context.log.debug(f"Loading file from: {path}")
            return joblib.load(f)

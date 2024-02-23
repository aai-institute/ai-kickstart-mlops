"""Pickle file system IO manager."""

import os
from typing import Any

import joblib
from dagster import InputContext, OutputContext

from ames_housing.io_managers.base_fs_io_manager import BaseFileSystemIOManager


class PickleFileSystemIOManager(BaseFileSystemIOManager):
    """Pickle file system IO manager.

    This IO manager serializes Python objects to pickle files using joblib.

    Attributes
    ----------
    extension : str
        File extension, be default ".pkl".
    """

    extension: str = ".pkl"

    def handle_output(self, context: OutputContext, obj: Any) -> None:
        """Write Python objext to a pickle file.

        Parameters
        ----------
        context : OutputContext
            Dagster context.
        obj : Any
            Python object that will be serialized to a pickle file.
        """
        path = self._get_path(context)
        os.makedirs(os.path.dirname(path), exist_ok=True)

        context.log.debug(f"Writing file at: {path}")
        joblib.dump(obj, path)

    def load_input(self, context: InputContext) -> Any:
        """Load pickle file into Python object.

        Parameters
        ----------
        context : InputContext
            Dagster context.

        Returns
        -------
        Any
            Python object deserialized from the pickle file.
        """
        path = self._get_path(context)

        context.log.debug(f"Loading file from: {path}")
        return joblib.load(path)

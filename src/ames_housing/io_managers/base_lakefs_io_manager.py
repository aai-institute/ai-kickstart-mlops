"""Base lakeFS IO manager."""

from typing import Optional, Union

from dagster import ConfigurableIOManager, InputContext, OutputContext
from lakefs_spec import LakeFSFileSystem
from lakefs_spec.transaction import LakeFSTransaction


class BaseLakeFSIOManager(ConfigurableIOManager):
    """Base lakeFS IO manager.

    This this IO manager as a basis for creating specialized IO managers that serialize
    objects to a lakeFS versioned data lake.

    Attributes
    ----------
    extension : str
        File extension.
    """

    extension: str

    def get_path(
        self,
        context: Union[OutputContext, InputContext],
        transaction: Optional[LakeFSTransaction] = None,
    ) -> str:
        """Get path in lakeFS based on the asset key.

        By convention, the asset key contains the repository and branch name as the
        first two elements.

        If a transaction is provided, the temporary branch created for the transaction
        will be used instead of the branch name provided as part of the asset key.

        Parameters
        ----------
        context : Union[OutputContext, InputContext]
            Dagster context
        transaction : Optional[LakeFSTransaction]
            lakeFS-spec transaction, by default None

        Returns
        -------
        str
            Path to the object in lakeFS.
        """
        if transaction is None:
            return "lakefs://" + "/".join(context.asset_key.path) + self.extension
        else:
            repository = context.asset_key.path[0]
            branch = transaction.branch.id
            path = "/".join(context.asset_key.path[2:])

            return f"lakefs://{repository}/{branch}/{path}{self.extension}"

    def transaction(
        self, context: Union[OutputContext, InputContext]
    ) -> LakeFSTransaction:
        """Start new lakeFS-spec transaction.

        The repository and branch are determined by the first two elements in the
        asset key.

        The resulting transaction can be used as context manager.

        Parameters
        ----------
        context : Union[OutputContext, InputContext]
            Dagster context

        Returns
        -------
        LakeFSTransaction
            lakeFS-spec transaction context.
        """
        fs = LakeFSFileSystem()

        # By convention, the asset key starts with the repository, followed by the
        # branch, followed by the path to the object.
        repository = context.asset_key.path[0]
        branch = context.asset_key.path[1]

        return fs.transaction(repository=repository, base_branch=branch)

    def open(self, path: str, mode: str):
        """Open a new file object for reading and writing objects from/to lakeFS.

        The resulting file object is similar to the build-in Python file objects.

        Parameters
        ----------
        path : str
            Path to file in lakeFS, following the "lakefs://" URI format.
        mode : str
            Mode in which the file is opened.

        Returns
        -------
        LakeFSIOBase
            File object that is ready for reading/writing.
        """
        fs = LakeFSFileSystem()
        return fs.open(path, mode)

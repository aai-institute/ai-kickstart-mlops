"""Base lakeFS IO manager."""

from typing import Any, Optional, Union

from dagster import ConfigurableIOManager, InputContext, OutputContext
from lakefs.object import LakeFSIOBase
from lakefs_spec import LakeFSFileSystem
from lakefs_spec.transaction import LakeFSTransaction
from sklearn.utils.metaestimators import abstractmethod


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
        commit_id: Optional[str] = None,
    ) -> str:
        """Get path in lakeFS based on the asset key.

        By convention, the asset key contains the repository and branch name as the
        first two elements.

        If a transaction is provided, the temporary branch created for the transaction
        will be used instead of the branch name provided as part of the asset key.


        If a commit identifier is provided, the branch name will be replaced with the
        commit id.

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
        if transaction is not None:
            repository = context.asset_key.path[0]
            branch = transaction.branch.id
            path = "/".join(context.asset_key.path[2:])

            return f"lakefs://{repository}/{branch}/{path}{self.extension}"
        elif commit_id is not None:
            repository = context.asset_key.path[0]
            path = "/".join(context.asset_key.path[2:])

            return f"lakefs://{repository}/{commit_id}/{path}{self.extension}"
        else:
            return "lakefs://" + "/".join(context.asset_key.path) + self.extension

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

    def open(self, path: str, mode: str) -> LakeFSIOBase:
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

    def handle_output(self, context: OutputContext, obj: Any) -> None:
        """Serialize the Python object to an object in lakeFS.

        Parameters
        ----------
        context : OutputContext
            Dagster context.
        obj : Any
            Python objec that will be serialized to an object in lakeFS.
        """

        with self.transaction(context) as tx:
            with self.open(self.get_path(context, transaction=tx), "wb") as f:
                context.log.debug(f"Writing file at: {self.get_path(context)}")
                self.write_output(f, obj)

            asset_without_repo_branch = "/".join(context.asset_key.path[2:])
            commit = tx.commit(message=f"Add asset {asset_without_repo_branch}")

        context.add_output_metadata(
            {
                "lakefs_commit": commit.id,
                "lakefs_url": self.get_path(context),
                "lakefs_permalink": self.get_path(context, commit_id=commit.id),
            }
        )

    def load_input(self, context: InputContext) -> Any:
        """Load file contects into Python object.

        Parameters
        ----------
        context : InputContext
            Dagster context.

        Returns
        -------
        Object with the contents of the file in lakeFS.
        """
        path = self.get_path(context)
        with self.open(path, "r") as f:
            result = self.read_input(f)
        return result

    @abstractmethod
    def write_output(self, f: LakeFSIOBase, obj: Any) -> None:
        """Write the Python object to an object in lakeFS."""
        raise NotImplementedError()

    @abstractmethod
    def read_input(self, f: LakeFSIOBase) -> Any:
        """Read the object from lakeFS."""
        raise NotImplementedError()

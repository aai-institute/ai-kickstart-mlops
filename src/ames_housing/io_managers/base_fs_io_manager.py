"""Base file system IO manager."""

from typing import Union

from dagster import ConfigurableIOManager, InputContext, OutputContext


class BaseFileSystemIOManager(ConfigurableIOManager):
    """Base file system IO manager.

    Use this IO manager as a basis for creating specialized IO managers that serialize
    objects to the local file system.

    Attributes
    ----------
    base_dir : str
        Base directory where assets will be written to.
    extension : str
        File extension.
    """

    base_dir: str
    extension: str

    def _get_path(self, context: Union[OutputContext, InputContext]) -> str:
        """Get the path to the asset file based on the base directory, asset key, and
        file extension.

        Parameters
        ----------
        context : Union[OutputContext, InputContext]
            Dagster context.
        """
        return self.base_dir + "/" + "/".join(context.asset_key.path) + self.extension

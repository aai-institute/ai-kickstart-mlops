"""CSV data set loader."""

import pandas as pd
from dagster import ConfigurableResource


class CSVDataSetLoader(ConfigurableResource):
    """CSV data set loader.

    Attributes
    ----------
    path_or_url : str
        Path on the file system or URL where the data set will be loaded from.
    separator : str
        Character or regex pattern to treat as the delimiter. See
        https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html#pandas-read-csv
        for more information. By default ",".
    """

    path_or_url: str
    separator: str = ","

    def load(self) -> pd.DataFrame:
        """Load the data set into a data frame.

        Returns
        -------
        DataFrame
            Loaded data set.
        """
        return pd.read_csv(self.path_or_url, sep=self.separator)

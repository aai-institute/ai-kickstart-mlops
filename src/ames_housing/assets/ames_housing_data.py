"""Ames housing data set."""

import pandas as pd
from caseconverter import snakecase
from dagster import asset

from ames_housing.resources.csv_data_set_loader import CSVDataSetLoader
from ames_housing.utils import get_key_prefix


@asset(io_manager_key="csv_io_manager", key_prefix=get_key_prefix())
def ames_housing_data(
    ames_housing_data_set_downloader: CSVDataSetLoader,
) -> pd.DataFrame:
    """Ames housing data set.

    Parameters
    ----------
    ames_housing_data_set_loader : CSVDataSetLoader
        Raw data set loader.

    Returns
    -------
    pd.DataFrame
        Raw Ames housing data set."""
    raw_data_df = ames_housing_data_set_downloader.load()

    # Re-format column names to snake case. The original data set uses several
    # different formats for its column names.
    raw_data_df = raw_data_df.rename(mapper=snakecase, axis=1)

    return raw_data_df

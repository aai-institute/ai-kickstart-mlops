"""Ames housing features."""

import pandas as pd
from dagster import asset

from ames_housing.constants import SELECTED_FEATURES, TARGET
from ames_housing.utils import get_key_prefix


@asset(io_manager_key="csv_io_manager", key_prefix=get_key_prefix())
def ames_housing_features(ames_housing_data: pd.DataFrame):
    """Ames housing features.

    Filter the Ames housing data set for the selected features and target.

    Parameters
    ----------
    ames_housing_data : pd.DataFrame
        Raw Ames housing data set.

    Returns
    -------
    pd.DataFrame
        Data set with selected features and target.
    """
    selected_columns = (
        SELECTED_FEATURES["nominal"]
        + SELECTED_FEATURES["ordinal"]
        + SELECTED_FEATURES["numerical"]
        + [TARGET]
    )

    return ames_housing_data[selected_columns]

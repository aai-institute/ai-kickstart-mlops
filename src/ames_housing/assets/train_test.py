"""Train and test data sets."""

from typing import Tuple

import pandas as pd
from dagster import AssetOut, multi_asset
from sklearn.model_selection import train_test_split

from ames_housing.constants import (
    LAKEFS_BRANCH,
    LAKEFS_DATA_PATH,
    LAKEFS_REPOSITORY,
    RANDOM_STATE,
)


@multi_asset(
    outs={
        "train_data": AssetOut(
            io_manager_key="csv_io_manager",
            metadata={
                "repository": LAKEFS_REPOSITORY,
                "branch": LAKEFS_BRANCH,
                "path": LAKEFS_DATA_PATH,
            },
        ),
        "test_data": AssetOut(
            io_manager_key="csv_io_manager",
            metadata={
                "repository": LAKEFS_REPOSITORY,
                "branch": LAKEFS_BRANCH,
                "path": LAKEFS_DATA_PATH,
            },
        ),
    }
)
def train_test_data(
    ames_housing_features: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Split the data set into a train and test data set.

    Parameters
    ----------
    ames_housing_features : pd.DataFrame
        Ames housing data features and target

    Returns
    -------
    pd.DataFrame
        Training data set
    pd.DataFrame
        Test data set
    """
    train_data: pd.DataFrame
    test_data: pd.DataFrame

    train_data, test_data = train_test_split(
        ames_housing_features,
        random_state=RANDOM_STATE,
    )  # type: ignore
    return train_data, test_data

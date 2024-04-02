"""Ames Housing price prediction model."""

import os

from dagster import Definitions, repository

from ames_housing.assets.ames_housing_data import ames_housing_data
from ames_housing.assets.ames_housing_features import ames_housing_features
from ames_housing.assets.price_prediction_models import (
    price_prediction_gradient_boosting_model,
    price_prediction_linear_regression_model,
    price_prediction_random_forest_model,
)
from ames_housing.assets.train_test import train_test_data
from ames_housing.constants import (
    AMES_HOUSING_DATA_SET_SEPARATOR,
    AMES_HOUSING_DATA_SET_URL,
    DATA_BASE_DIR,
    LAKEFS_BRANCH,
    LAKEFS_REPOSITORY,
    MLFLOW_EXPERIMENT,
    MLFLOW_PASSWORD,
    MLFLOW_TRACKING_URL,
    MLFLOW_USERNAME,
    MODEL_BASE_DIR,
)
from ames_housing.io_managers.csv_fs_io_manager import CSVFileSystemIOManager
from ames_housing.io_managers.csv_lakefs_io_manager import CSVLakeFSIOManager
from ames_housing.io_managers.pickle_fs_io_manager import PickleFileSystemIOManager
from ames_housing.io_managers.pickle_lakefs_io_manager import PickleLakeFSIOManager
from ames_housing.resources.csv_data_set_loader import CSVDataSetLoader
from ames_housing.resources.mlflow_session import MlflowSession

# Depending on the environment, serialize assets to the local file system or to lakeFS.
if os.environ.get("ENV") == "production":
    csv_io_manager = CSVLakeFSIOManager(
        repository=LAKEFS_REPOSITORY, branch=LAKEFS_BRANCH
    )
    pickle_io_manager = PickleLakeFSIOManager(
        repository=LAKEFS_REPOSITORY, branch=LAKEFS_BRANCH
    )
else:
    csv_io_manager = CSVFileSystemIOManager(base_dir=DATA_BASE_DIR)
    pickle_io_manager = PickleFileSystemIOManager(base_dir=MODEL_BASE_DIR)


definitions = Definitions(
    assets=[
        ames_housing_data,
        ames_housing_features,
        train_test_data,
        price_prediction_linear_regression_model,
        price_prediction_random_forest_model,
        price_prediction_gradient_boosting_model,
    ],
    resources={
        "ames_housing_data_set_downloader": CSVDataSetLoader(
            path_or_url=AMES_HOUSING_DATA_SET_URL,
            separator=AMES_HOUSING_DATA_SET_SEPARATOR,
        ),
        "mlflow_session": MlflowSession(
            tracking_url=MLFLOW_TRACKING_URL,
            username=MLFLOW_USERNAME,
            password=MLFLOW_PASSWORD,
            experiment=MLFLOW_EXPERIMENT,
        ),
        "csv_io_manager": csv_io_manager,
        "pickle_io_manager": pickle_io_manager,
    },
)

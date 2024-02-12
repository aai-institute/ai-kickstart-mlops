"""Price prediction model."""

import pandas as pd
from dagster import AssetExecutionContext, asset
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler

from ames_housing.constants import SELECTED_FEATURES, TARGET


@asset(io_manager_key="picke_fs_io_manager")
def price_prediction_model(
    context: AssetExecutionContext, train_data: pd.DataFrame, test_data: pd.DataFrame
):
    """Price prediction model."""

    ordinal_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OrdinalEncoder()),
        ]
    )

    nominal_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    numerical_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="mean")),
            ("encoder", StandardScaler()),
        ]
    )

    preprocessing_pipeline = ColumnTransformer(
        [
            (
                "ordinal_preprocessor",
                ordinal_pipeline,
                SELECTED_FEATURES["ordinal"],
            ),
            (
                "nominal_preprocessor",
                nominal_pipeline,
                SELECTED_FEATURES["nominal"],
            ),
            (
                "numerical_preprocessor",
                numerical_pipeline,
                SELECTED_FEATURES["numerical"],
            ),
        ]
    )

    pipeline = Pipeline(
        [
            ("preprocessor", preprocessing_pipeline),
            ("estimator", LinearRegression()),
        ]
    )

    pipeline.fit(train_data.drop([TARGET], axis=1), train_data[TARGET])

    score = pipeline.score(test_data, test_data[TARGET])
    context.log.info(f"Score: {score}")

    return pipeline

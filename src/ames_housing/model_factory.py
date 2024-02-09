"""Housing price predictor model factory."""

from typing import Any

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler

from ames_housing.constants import SELECTED_FEATURES


class ModelFactory:
    @classmethod
    def _create_preprocessing_pipeline(cls) -> ColumnTransformer:
        """Create the preprocessing pipeline."""

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

        return preprocessing_pipeline

    @classmethod
    def _create_pipeline(cls, estimator: Any) -> Pipeline:
        """Create pipeline using the specified estimator."""

        pipeline = Pipeline(
            [
                ("preprocessor", cls._create_preprocessing_pipeline()),
                ("estimator", estimator()),
            ]
        )

        return pipeline

    @classmethod
    def create_linear_regression_pipeline(cls) -> Pipeline:
        """Create linear regression pipeline."""
        return cls._create_pipeline(LinearRegression)

    @classmethod
    def create_random_forest_pipeline(cls) -> Pipeline:
        """Create random forest pipeline."""
        return cls._create_pipeline(RandomForestRegressor)

    @classmethod
    def create_gradient_boosting_regressor_pipeline(cls) -> Pipeline:
        """Create gradient boosting regressor pipeline."""
        return cls._create_pipeline(GradientBoostingRegressor)

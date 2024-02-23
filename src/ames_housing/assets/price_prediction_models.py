"""Price prediction models."""

import mlflow
import pandas as pd
from dagster import AssetExecutionContext, asset
from sklearn.pipeline import Pipeline
from src.ames_housing.model_factory import ModelFactory

from ames_housing.constants import TARGET
from ames_housing.resources.mlflow_session import MlflowSession
from ames_housing.utils import get_key_prefix


def _fit_and_score_pipeline(
    context: AssetExecutionContext,
    mlflow_session: MlflowSession,
    pipeline: Pipeline,
    train_data: pd.DataFrame,
    test_data: pd.DataFrame,
) -> Pipeline:
    """Fit and score specified pipeline.

    Parameters
    ----------
    context : AssetExecutionContext
        Dagster context.
    mlflow_session : MlflowSession
        MLflow session/run resource.
    pipeline : Pipeline
        Pipeline definition.
    train_data : pd.DataFrame
        Training data set.
    test_data : pd.DataFrame
        Testing data set.

    Returns
    -------
    Pipeline
        The fitted pipeline.
    """
    with mlflow_session.get_run(context):
        mlflow.sklearn.autolog()


        pipeline.fit(train_data.drop([TARGET], axis=1), train_data[TARGET])

        score = pipeline.score(test_data, test_data[TARGET])
        context.log.info(f"Score: {score}")

    return pipeline


@asset(io_manager_key="pickle_io_manager", key_prefix=get_key_prefix())
def price_prediction_linear_regression_model(
    context: AssetExecutionContext,
    mlflow_session: MlflowSession,
    train_data: pd.DataFrame,
    test_data: pd.DataFrame,
) -> Pipeline:
    """Price prediction linear regression model."""
    return _fit_and_score_pipeline(
        context,
        mlflow_session,
        ModelFactory.create_linear_regression_pipeline(),
        train_data,
        test_data,
    )


@asset(io_manager_key="pickle_io_manager", key_prefix=get_key_prefix())
def price_prediction_random_forest_model(
    context: AssetExecutionContext,
    mlflow_session: MlflowSession,
    train_data: pd.DataFrame,
    test_data: pd.DataFrame,
) -> Pipeline:
    """Price prediction random forest regressor model."""
    return _fit_and_score_pipeline(
        context,
        mlflow_session,
        ModelFactory.create_random_forest_pipeline(),
        train_data,
        test_data,
    )


@asset(io_manager_key="pickle_io_manager", key_prefix=get_key_prefix())
def price_prediction_gradient_boosting_model(
    context: AssetExecutionContext,
    mlflow_session: MlflowSession,
    train_data: pd.DataFrame,
    test_data: pd.DataFrame,
) -> Pipeline:
    """Price prediction gradient boosting regressor model."""
    return _fit_and_score_pipeline(
        context,
        mlflow_session,
        ModelFactory.create_gradient_boosting_regressor_pipeline(),
        train_data,
        test_data,
    )

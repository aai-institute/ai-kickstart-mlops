"""MLflow session resource."""

import os

import mlflow
from dagster import AssetExecutionContext, ConfigurableResource, InitResourceContext


class MlflowSession(ConfigurableResource):
    """MLflow session resource.

    Notes
    -----
    Since MLflow uses global state (Python globals / environment variables)
    to store its tracking configuration (endpoint URL, credentials), this
    resource can effectively only be parameterized with a single configuration
    per Dagster process."""

    tracking_url: str
    username: str | None
    password: str | None
    experiment: str

    def setup_for_execution(self, context: InitResourceContext) -> None:
        mlflow.set_tracking_uri(self.tracking_url)
        # MLflow expects credentials in environment variables
        if self.username:
            os.environ["MLFLOW_TRACKING_USERNAME"] = self.username
        if self.password:
            os.environ["MLFLOW_TRACKING_PASSWORD"] = self.password
        mlflow.set_experiment(self.experiment)

    def get_run(self, context: AssetExecutionContext) -> mlflow.ActiveRun:
        dagster_run_id = context.run.run_id
        dagster_asset_key = context.asset_key.to_user_string()

        run_name = f"{dagster_asset_key}-{dagster_run_id}"

        active_run = mlflow.active_run()
        if active_run is None:
            current_runs = mlflow.search_runs(
                filter_string=f"attributes.`run_name`='{run_name}'",
                output_format="list",
            )

            if current_runs:
                run_id = current_runs[0].info.run_id
                return mlflow.start_run(run_id=run_id, run_name=run_name)
            else:
                tags = {"dagster.run_id": dagster_run_id}
                return mlflow.start_run(run_name=run_name, tags=tags)

        return active_run

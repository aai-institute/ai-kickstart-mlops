"""MLflow session resource."""

import os

import mlflow
from dagster import AssetExecutionContext, ConfigurableResource


class MlflowSession(ConfigurableResource):
    """MLflow session resource."""

    tracking_url: str
    username: str | None
    password: str | None
    experiment: str

    def get_run(self, context: AssetExecutionContext) -> mlflow.ActiveRun:
        mlflow.set_tracking_uri(self.tracking_url)
        if self.username:
            os.environ["MLFLOW_TRACKING_USERNAME"] = self.username
        if self.password:
            os.environ["MLFLOW_TRACKING_PASSWORD"] = self.password
        mlflow.set_experiment(self.experiment)

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

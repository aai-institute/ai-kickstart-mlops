# AI Career Kickstart MLOps example

## Quickstart

The example requires Python 3.9 or later installed.
If you want to host the MLOps tool stack (MLflow & lakeFS) on your local machine, Docker (and Docker Compose) is required.

Follow these steps in a local clone of the repository to reproduce the example Dagster workflow:

- Create a Python virtual environment and install dependencies (macOS/Linux): `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt -e .`
- Optionally (not required when running locally with Docker Compose): Set MLFlow tracking URL and credentials and lakeFS repository information in `src/ames_housing/constants.py`
- Start MLOps tool stack in Docker (in a separate shell): `docker compose -f stack/docker-compose.yml up`
- Run Dagster: `dagster dev -m ames_housing`
- Access Dagster web UI: http://localhost:3000
- Click the _Materialize all_ button to run the model training pipeline
- Observe the tracked experiment in MLflow: http://localhost:5000 (if using Docker Compose)

### Using the lakeFS I/O Managers

By default, data and models created by the workflow are persisted in the file system (under the `data/` and `model/` directories).
If you want to persist these assets in lakeFS instead, set the `ENV` environment variable to `production` when running Dagster:

```
ENV=production dagster dev -m ames_housing
```

Make sure to create a repository named `ai-kickstart` in the [lakeFS web UI](http://localhost:8000) before materializing the assets in Dagster (the Docker Compose setup uses the default [lakeFS quickstart](https://docs.lakefs.io/quickstart/) credentials for login: Access key ID `AKIAIOSFOLQUICKSTART`, secret access key `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`).

Then, add your lakeFS credentials to the [`.lakectl.yaml` config file](https://docs.lakefs.io/reference/cli.html) in your home directory to allow the Dagster I/O managers to automatically discover the lakeFS server URL and credentials (this step is only necessary once):

```yaml
credentials:
  access_key_id: AKIAIOSFOLQUICKSTART
  secret_access_key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
server:
  endpoint_url: http://127.0.0.1:8000
```

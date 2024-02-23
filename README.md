# AI Career Kickstart MLOps example

## Quickstart

- Create a virtual environment and install dependencies (macOS/Linux): `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt -e .`
- Set MLFlow tracking URL and credentials in `src/ames_housing/constants.py`
- Run Dagster: `dagster dev -f src/ames_housing/__init__.py`
- Access Dagster web UI: http://localhost:3000
- Click the _Materialize all_ button to run the model training pipeline

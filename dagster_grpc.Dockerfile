FROM python:3.10-slim

# Checkout and install dagster libraries needed to run the gRPC server
# exposing your repository to dagster-webserver and dagster-daemon, and to load the DagsterInstance

RUN pip install \
    dagster \
    dagster-postgres \
    dagster-docker

# Add repository code
COPY . /opt/dagster/app/
ENV PYTHONPATH "${PYTHONPATH}:/opt/dagster/app/:/opt/dagster/app/src/"
RUN python -m pip install /opt/dagster/app/

WORKDIR /opt/dagster/app

# CMD allows this to be overridden from run launchers or executors that want
# to run other commands against your repository
CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "5432", "-m", "ames_housing"]
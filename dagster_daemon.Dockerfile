FROM python:3.10-slim


RUN mkdir -p /opt/dagster/dagster_home /opt/dagster/app

RUN pip install dagster-webserver dagster-postgres dagster-aws dagster-docker

# Copy your code and workspace to /opt/dagster/app
COPY workspace.yaml /opt/dagster/app/
#
#ENV PYTHONPATH "${PYTHONPATH}:/opt/dagster/app/:/opt/dagster/app/src/"
#
#RUN python -m pip install /opt/dagster/app/

ENV DAGSTER_HOME=/opt/dagster/dagster_home/

# Copy dagster instance YAML to $DAGSTER_HOME
COPY dagster.yaml workspace.yaml src/ames_housing/__init__.py /opt/dagster/dagster_home/

WORKDIR /opt/dagster/app

EXPOSE 3000

ENTRYPOINT ["dagster-webserver", "-h", "0.0.0.0", "-p", "3000", "-w", "workspace.yaml"]
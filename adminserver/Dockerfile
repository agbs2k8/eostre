FROM python:3.13-slim as base
# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True
# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS py-deps
# Install pipenv dependencies
RUN pip install pipenv
# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base AS runtime
# Copy virtual env from py-deps stage
COPY --from=py-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"
# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
# Ensure that the app can find the config file
ENV PYTHONPATH "${PYTHONPATH}:${APP_HOME}/src"
# Run the API on container startup
CMD exec hypercorn --bind :8080 --access-logfile - src.api.main:app
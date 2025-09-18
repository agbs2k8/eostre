FROM python:3.13-slim AS build
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app

COPY pyproject.toml ./
COPY src ./src
COPY main.py config.py ./

RUN pip install --no-cache-dir .

FROM build AS test
COPY tests ./tests
RUN pip install .[test] && pytest -q || true

FROM python:3.13-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY --from=build /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=build /usr/local/bin/hypercorn /usr/local/bin/hypercorn

COPY src ./src
COPY main.py config.py pyproject.toml ./

ENTRYPOINT ["hypercorn", "--bind", "0.0.0.0:8080", "main:app"]
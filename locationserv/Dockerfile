FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install build essentials only if you have binary deps (uncomment if needed)
# RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# Copy Pipenv files first for caching
COPY Pipfile Pipfile.lock ./

# Install pipenv and project deps into system site-packages
RUN pip install --no-cache-dir pipenv && \
    pipenv install --system --deploy --ignore-pipfile

# Copy source code
COPY src ./src

# (Optional) copy any ancillary modules/config if needed
# COPY config ./config

EXPOSE 8000

# Dev auto-reload; remove --reload for production
CMD ["uvicorn", "src.app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000", "--reload"]
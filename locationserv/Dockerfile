# FastAPI location service
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only necessary source (adjust if you have other resource dirs)
COPY src ./src

# If you need a keys dir baked in (runtime mount overrides) uncomment:
# COPY ../adminserver/keys ./keys

EXPOSE 8000

# Using app factory create_app in src/app.py
CMD ["uvicorn", "src.app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000", "--reload"]
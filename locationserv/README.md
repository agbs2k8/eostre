source ../export_locals.sh

python3 -m venv .venv

python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload

pytest --cov=src --cov-report=term-missing
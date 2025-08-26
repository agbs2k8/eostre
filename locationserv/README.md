source ../export_locals.sh

/.venv/Scripts/activate

source D:/Projects/eostre/locationserv/.venv/Scripts/activate

python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload

pytest --cov=src --cov-report=term-missing
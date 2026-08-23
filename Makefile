.PHONY: test run setup

test:
	cd backend && PYTHONPATH=. pytest -q

setup:
	cd backend && python3.14 -m venv .venv314 && .venv314/bin/python -m pip install --upgrade pip && .venv314/bin/python -m pip install -r requirements.txt

run:
	cd backend && PYTHONPATH=. .venv314/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

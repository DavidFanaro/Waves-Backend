setup: export FLASK_APP=run.py

release: flask db upgrade

web: gunicorn run:app
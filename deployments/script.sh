#!/bin/sh

mkdir -p logs
export PYTHONPATH=/app:$PYTHONPATH

echo "Initializing database"
python -m source.db.init_db
echo "Database initialized"
alembic upgrade head
echo "Database upgraded"
python -m source.main & streamlit run source/web/app.py --server.port=8501 --server.address=0.0.0.0
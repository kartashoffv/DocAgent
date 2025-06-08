FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY source /app/source
COPY alembic.ini /app/alembic.ini
COPY alembic /app/alembic
COPY deployments/script.sh /app/script.sh
RUN chmod +x /app/script.sh

CMD ["/app/script.sh"]

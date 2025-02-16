FROM python:3.12-slim

WORKDIR /app

COPY api/v1/blockchain/requirements.txt ./api/v1/blockchain/requirements.txt
RUN pip install --no-cache-dir -r api/v1/blockchain/requirements.txt

COPY . .

CMD ["sh", "-c", "PYTHONPATH=/app uvicorn api.v1.blockchain.app:app --host 0.0.0.0 --port 8003"]

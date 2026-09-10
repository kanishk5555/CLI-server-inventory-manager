FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .
COPY database.py .
COPY main.py .
COPY server.json .

CMD ["python", "main.py"]

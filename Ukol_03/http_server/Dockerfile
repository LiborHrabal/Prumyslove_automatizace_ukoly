FROM python:3.12-slim

WORKDIR /app

# Kopíruj závislosti a nainstaluj
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopíruj kód
COPY src/ .

# Environmentální proměnné pro server a MongoDB
ENV HOST=0.0.0.0
ENV PORT=8000
ENV MONGO_HOST=mongodb://mongo:27017/
ENV DB_NAME=ukol03_mongodb
ENV COLLECTION_NAME=machine_data

# Otevření portu
EXPOSE 8000

CMD ["python", "http_server.py"]

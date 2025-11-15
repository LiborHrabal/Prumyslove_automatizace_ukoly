# Používáme oficiální Python 3.12 slim image jako základ
FROM python:3.12-slim

# Nastavení pracovního adresáře uvnitř kontejneru
# Všechny příkazy RUN, COPY, CMD se budou provádět z /app
WORKDIR /app

# Zkopíruj soubor requirements.txt z tvého projektu do kontejneru
# Tímto krokem se vyhýbáme opakované instalaci všech závislostí při každé změně zdrojového kódu
COPY src/requirements.txt .

# Instalace Python závislostí uvnitř kontejneru
# --no-cache-dir zajistí, že pip neukládá cache a image zůstane menší
RUN pip install --no-cache-dir -r requirements.txt

# Zkopíruj zbytek zdrojového kódu do kontejneru
COPY src/ .

# Nastavení environmentální proměnné, kterou může aplikace využívat
ENV MONGO_HOST=mongodb://localhost:27017/
ENV DB_NAME=ukol03_mongodb

# Definuje výchozí příkaz, který se spustí, když kontejner startuje
# Spustí Python skript data_transform.py
CMD ["python", "data_transform.py"]

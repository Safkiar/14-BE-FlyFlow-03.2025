# Użyj oficjalnego obrazu Pythona
FROM python:3.12

# Zainstaluj wymagane pakiety systemowe (w tym Chrome i chromedriver)
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Ustaw ścieżkę do przeglądarki Chrome
ENV CHROMIUM_PATH=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Ustaw katalog pracy w kontenerze
WORKDIR /app

# Skopiuj pliki projektu do kontenera
COPY . .

# Instalacja zależności
RUN pip install --no-cache-dir -r requirements.txt

# Uruchom Django przy starcie kontenera
CMD gunicorn webapp.wsgi:application --bind 0.0.0.0:$PORT
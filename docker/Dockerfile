FROM python:3.12-slim

WORKDIR /app

ENV http_proxy=http://172.25.25.250:2002/
ENV https_proxy=http://172.25.25.250:2002/
ENV ftp_proxy=http://172.25.25.250:2002/

RUN apt-get update && apt-get install -y \
    libpq-dev \
    python3-dev \
    gcc \
    --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY ../requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY .. .

CMD ["python", "main.py"]

FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements-dev.txt ./

RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

EXPOSE 8000

CMD ["python3", "-m", "fastapi", "dev", "main.py", "--host", "0.0.0.0"]

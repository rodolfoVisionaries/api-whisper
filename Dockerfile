# --- Dockerfile ---

FROM python:3.12-slim

# Env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8

# Workdir
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    curl \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Launch
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
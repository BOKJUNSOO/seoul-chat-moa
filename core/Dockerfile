# embedding container builder file
FROM python:3.12-slim

WORKDIR /app/core

# psycopg2 빌드를 위해 필요한 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python 패키지 설치
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir \
        langchain \
        langchain-openai \
        langchain-community \
        langchain-chroma \
        chromadb \
        openai \
        pandas \
        geopy \
        tiktoken \
        psycopg2 

COPY . .

# run embedder script
CMD ["python", "embedding.py"]
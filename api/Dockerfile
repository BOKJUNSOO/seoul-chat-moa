# Fast api server builder file
FROM python:3.12-slim

WORKDIR /app/api

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# python 패키지
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir \
        fastapi \
        uvicorn \
        langchain \
        langchain-openai \
        langchain-community \
        langchain-chroma\
        chromadb \
        openai \
        pandas \
        sqlalchemy \
        psycopg2
        
COPY . .

# run server
CMD ["uvicorn", "api.moa:app", "--host", "0.0.0.0", "--port", "8001"]
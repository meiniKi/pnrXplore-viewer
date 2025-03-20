FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -e .

EXPOSE 8501
ENV NAME=pnrxplore-viewer

CMD ["streamlit", "run", "/app/pnrXplore_viewer/pnrXplore.py", "--server.maxUploadSize", "2048"]
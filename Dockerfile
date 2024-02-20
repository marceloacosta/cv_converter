# app/Dockerfile

FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip3 install -r requirements.txt
RUN pip3 install pdfkit

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:80/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

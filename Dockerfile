# Python 3.12 slim sebagai base
FROM python:3.12-slim

LABEL maintainer="Alfito Afdhan Nugraha <202310370311415>"
LABEL description="Tugas 1 Analisis Big Data - BMKG Weather Forecast Analysis"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    JUPYTER_ENABLE_LAB=yes

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dan install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy seluruh project
COPY . .

# Buat direktori yang diperlukan
RUN mkdir -p data/raw output/figures

# Expose port JupyterLab
EXPOSE 8888

# Default command: JupyterLab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", \
     "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''", \
     "--notebook-dir=/app"]

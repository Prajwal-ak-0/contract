# Use Python 3.11 slim as base image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    OPENAI_API_KEY=""

# Install system dependencies and clean up in one layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        && apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p contract_file

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all backend Python files (excluding frontend directory)
COPY batch_embedding.py .
COPY chunking.py .
COPY config.py .
COPY database_handler.py .
COPY database_schema.py .
COPY main.py .
COPY rag_chatbot.py .
COPY rag_schemas.py .
COPY result_database.py .
COPY schemas.py .
COPY sqlite_rag.py .
COPY csv_writer.py .
# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

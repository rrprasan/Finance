# 🧊 Iceberg Table Creator - Docker Image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY Iceberg_Table_Creator.py .
COPY docs/ docs/
COPY README.md .
COPY LICENSE .

# Create directories for mounted credentials
RUN mkdir -p /root/.aws /root/.snowflake

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run the application
CMD ["streamlit", "run", "Iceberg_Table_Creator.py", "--server.address", "0.0.0.0", "--server.port", "8501"]

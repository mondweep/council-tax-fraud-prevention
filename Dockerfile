# Council Tax Fraud Prevention System - Docker Configuration
FROM python:3.11-slim

# Set metadata
LABEL maintainer="Council Development Team <dev-team@council.gov.uk>"
LABEL description="AI-powered council tax fraud detection and prevention system"
LABEL version="1.0.0"

# Set environment variables
ENV PYTHONPATH=/app/src
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Create non-root user for security
RUN groupadd -r fraud-detection && useradd -r -g fraud-detection fraud-user

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements first for better Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY tests/ ./tests/
COPY docs/ ./docs/
COPY scripts/ ./scripts/
COPY Makefile .
COPY setup.py .

# Create necessary directories
RUN mkdir -p data/sample logs reports models backup \
    && touch data/.gitkeep data/sample/.gitkeep logs/.gitkeep \
            reports/.gitkeep models/.gitkeep backup/.gitkeep

# Change ownership to non-root user
RUN chown -R fraud-user:fraud-detection /app

# Switch to non-root user
USER fraud-user

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Expose port
EXPOSE 8501

# Default command - run dashboard
CMD ["streamlit", "run", "src/dashboard.py", "--server.address", "0.0.0.0", "--server.port", "8501"]

# Alternative commands available:
# CLI demo: docker run <image> python src/cli_demo.py
# Tests: docker run <image> python -m pytest tests/
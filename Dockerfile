FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for image processing
RUN apt-get update && apt-get install -y \
    libopenjp2-7 \
    libtiff6 \
    libwebp7 \
    libjpeg62-turbo \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .
COPY config.py .
COPY database.py .
COPY image_processor.py .
COPY keyboards.py .
COPY messages.py .
COPY handlers.py .

# Create necessary directories
RUN mkdir -p user_data/logos user_data/settings user_data/temp

# Set environment to production
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Run the bot
CMD ["python", "main.py"]

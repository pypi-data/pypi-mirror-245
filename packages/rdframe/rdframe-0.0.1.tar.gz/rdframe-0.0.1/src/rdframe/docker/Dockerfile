# Start from the Python 3.11 slim image
FROM python:3.11-slim

# Set the working directory in the Docker image
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ../../.. /app

# Install build dependencies for C-extensions and Poetry
# Then, use poetry to install the Python dependencies without creating a virtualenv
# After that, remove build dependencies to keep the image clean and small
RUN apt-get update && apt-get install -y --no-install-recommends gcc libc6-dev && \
    pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev && \
    apt-get remove -y gcc libc6-dev && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Command to run the application
ENTRYPOINT uvicorn src.app:app --host=${HOST:-0.0.0.0} --port=${PORT:-8000} --proxy-headers
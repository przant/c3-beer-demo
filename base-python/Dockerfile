FROM python:3.11-slim-bookworm

# Install PostgreSQL client for database connections
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install common Python libraries used across algorithms
RUN pip install --no-cache-dir \
    psycopg2-binary==2.9.9 \
    pandas==2.1.3

# Set working directory
WORKDIR /app

# This is our base image - algorithm containers will build FROM this
# This way we don't reinstall Python, PostgreSQL client, or common libraries every time

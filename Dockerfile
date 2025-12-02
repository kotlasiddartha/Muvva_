FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies required to build and run pycairo and PDF libs
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       pkg-config \
       libcairo2-dev \
       libpango1.0-dev \
       libgirepository1.0-dev \
       libffi-dev \
       libssl-dev \
       libxml2-dev \
       libxslt1-dev \
       git \
       curl \
       libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt /app/

# Upgrade pip and install wheel to prefer binary wheels where available
RUN python -m pip install --upgrade pip wheel
RUN pip install -r requirements.txt

# Copy the project
COPY . /app/

# Create a user to avoid running as root (optional)
RUN useradd --create-home appuser || true
RUN chown -R appuser:appuser /app
USER appuser

ENV PORT=8000

# Use shell form so $PORT expands
CMD gunicorn Muvva_.wsgi --bind 0.0.0.0:$PORT

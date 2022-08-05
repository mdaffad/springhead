# syntax = docker/dockerfile:1.2
FROM python:3.9 AS builder

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Make virtualenv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install requirements
COPY requirements.txt /app/
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt




FROM python:3.9-slim-buster as base

ENV VIRTUAL_ENV=/opt/venv

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /code
WORKDIR /code

# Copy code into Docker container
COPY /src ./src
# Activate virtual env
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Use Pip-Compile to create environment
COPY requirements.in ./requirements.in
RUN pip install --upgrade pip && \
    pip install pip-tools && \
    pip-compile requirements.in && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf requirements.txt

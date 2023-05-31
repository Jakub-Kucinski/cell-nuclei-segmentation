FROM nvidia/cuda:11.7.1-devel-ubuntu22.04

# Install git
RUN apt-get -y update && apt-get install -y git \
    python3.10 pip

#Install poetry
RUN pip install poetry

# Disable virtualenv creation
ENV POETRY_VIRTUALENVS_CREATE=false

# Install dependencies
COPY pyproject.toml .
RUN poetry install --no-interaction
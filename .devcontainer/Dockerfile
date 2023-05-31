FROM python:3.10-slim-bullseye

# Install git
RUN apt-get -y update && apt-get install -y git

#Install poetry
RUN pip install poetry

# Disable virtualenv creation
ENV POETRY_VIRTUALENVS_CREATE=false

# Install dependencies
COPY pyproject.toml .
RUN poetry install --no-interaction
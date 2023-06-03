FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

# Install git
RUN apt-get -y update && apt-get install -y git

#Install poetry
RUN pip install poetry

# Disable virtualenv creation
ENV POETRY_VIRTUALENVS_CREATE=false

# Install dependencies
COPY pyproject.toml .
RUN poetry install --with test,lint,dev --no-interaction
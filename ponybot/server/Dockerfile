FROM python:3.8-slim-buster

EXPOSE 8000

# Defining variables
ENV PONYBOT_SERVER_SERVICE_NAME=server
ENV PONYBOT_SERVER_SERVICE_ENVIRONMENT=dev
ENV PONYBOT_SERVER_SERVICE_ROOT=/ponybot/${PONYBOT_SERVER_SERVICE_NAME}/${PONYBOT_SERVER_SERVICE_ENVIRONMENT}
ENV PONYBOT_SERVER_SERVICE_WORKERS_COUNT=4

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Switching to service root directory
WORKDIR ${PONYBOT_SERVER_SERVICE_ROOT}

## Install poetry
RUN pip install --upgrade pip && pip --no-cache-dir install poetry

# Copying env file
COPY .env-${PONYBOT_SERVER_SERVICE_ENVIRONMENT} ${PONYBOT_ROOT}/.env
# Copying service sources
COPY . ${PONYBOT_SERVER_SERVICE_ROOT}

# Setting rights to execute scripts in scripts folder
RUN chmod +x -R ${PONYBOT_SERVER_SERVICE_ROOT}/scripts/

# Install server requirements
RUN poetry install

# Creates a non-root user adds permission to access the app folder
RUN adduser --disabled-password --gecos "" server_user
USER server_user

# Switching to poetry venv
# RUN ./scripts/docker-poetry-activate.sh

ENTRYPOINT "./scripts/docker-entrypoint.sh"